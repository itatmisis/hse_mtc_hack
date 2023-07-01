#!/usr/bin/env python3
import uvicorn
import asyncio
from functools import partial
from fastapi import FastAPI, HTTPException, status
import json

import config
from worker import parse_group
from db import DBManager
from config import log
from os import getenv

# Create FastAPI instance
api = FastAPI()

db = DBManager(getenv('POSTGRES_USER'), getenv('POSTGRES_PASSWORD'),
               getenv('POSTGRES_HOST'), getenv('POSTGRES_PORT'),
               getenv('POSTGRES_DB'))


# region Endpoints
@api.get("/", tags=["root"])
async def root():
    return {"message": "I am a worker. Say hi to my API!"}

# Worker occupation status
is_occupied = False
# Dictionary to track the status of parsing jobs
active_jobs: dict[str, asyncio.Task] = {}


@api.post("/parse")
async def parse_telegram_group(group_link: str,
                               messages_limit: int = 20,
                               comments_limit: int = 20):
    # Check if a parsing job is already active for this worker
    global is_occupied
    if is_occupied:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Worker is occupied")

    # Convert `link` to a channel name if contains t.me before the last / or starts with http
    try:
        link = (
            group_link.split("/")[-1] if group_link.startswith("http")
            or "t.me" in group_link.split("/")[-2]
            else group_link
            )
    except IndexError:
        link = group_link

    # Create a task for the parsing job
    job_task = asyncio.create_task(job_parse_group(link,
                                                   messages_limit,
                                                   comments_limit))
    active_jobs[link] = job_task
    is_occupied = True

    # Return the response immediately
    return {"status": "in_progress"}


async def job_parse_group(link: str, messages_limit: int, comments_limit: int):
    # Perform the parsing job here
    try:
        result = await parse_group(channel_link=link,
                                   messages_limit=messages_limit,
                                   comments_limit=comments_limit)
    except Exception as exc:
        log.debug(f"Error parsing channel {link}: {exc}")
    log.debug("Adding channel records to DB...")
    db.add_channel_records(result)

    # Once the parsing is complete, remove the job from active_jobs
    del active_jobs[link]
    global is_occupied
    is_occupied = False


# Cleanup task to cancel any active jobs when the application is shutdown
async def cleanup_active_jobs():
    for job_task in active_jobs.values():
        job_task.cancel()


@api.on_event("shutdown")
async def shutdown_event():
    await cleanup_active_jobs()
# endregion


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(cleanup_active_jobs())
    uvicorn.run(api, host="0.0.0.0", port=config.API_PORT)
