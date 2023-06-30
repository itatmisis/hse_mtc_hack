#!/usr/bin/env python3
import uvicorn
import asyncio
import aiohttp
from asyncio import sleep as asleep
from fastapi import FastAPI
from urllib.parse import urljoin
from fastapi_utils.tasks import repeat_every

import config
from config import log

# Create FastAPI instance
api = FastAPI()


# region Endpoints
@api.get("/", tags=["root"])
async def root():
    return {"message": "I am a coordinator. Say hi to my API!"}

# Job FIFO queue
job_queue: dict = {}


@api.post("/schedule")
async def schedule_parse_job(group_handle: str,
                             messages_limit: int = 20,
                             comments_limit: int = 20):
    try:
        handle = (
            group_handle.split("/")[-1] if group_handle.startswith("http")
            or "t.me" in group_handle.split("/")[-2]
            else group_handle
            )
    except IndexError:
        handle = group_handle

    already_scheduled = handle in job_queue.keys()

    # Add the job to the queue
    if not already_scheduled:
        job_queue[handle] = {'messages_limit': messages_limit,
                             'comments_limit': comments_limit}
        # Trigger runner
        await run_scheduled_jobs()
        # Return the response immediately
        return {"status": "scheduled"}
    else:
        return {"status": "already_scheduled"}
# endregion


# region Scheduled tasks
@api.on_event("startup")
@repeat_every(seconds=35)
async def run_scheduled_jobs() -> None:
    log.debug(f"Running scheduled jobs ({job_queue.items()})...")
    # Delete the first job from the queue and schedule it
    if job_queue:
        job = job_queue.popitem()
    else:
        return
    retry_count = 3
    is_successful = False
    for counter in range(retry_count):
        log.debug(f"Trying to schedule job for {job}...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://" + config.worker_address + "/parse",
                                        params={'group_link': job[0]}) as response:
                    if response.status == 200:
                        log.info(f"Successfully scheduled job for {job}")
                        is_successful = True
                        break
                    elif response.status == 409:
                        if counter != retry_count - 1:
                            log.info(f"Current worker is busy; retrying {job} after cooldown")
                            await asleep(5)
                        else:
                            log.info(f"Current worker is busy; putting {job} in the last place of the queue")
                            job_queue[job] = {'messages_limit': job[1]['messages_limit'],
                                              'comments_limit': job[1]['comments_limit']}
        except Exception as exc:
            log.error(f"Failed to schedule job for {job}: {exc}")
            if not is_successful:
                if job[0] not in job_queue.keys():
                    job_queue[job] = {'messages_limit': job[1]['messages_limit'],
                                      'comments_limit': job[1]['comments_limit']}
            continue
# endregion


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8001)
