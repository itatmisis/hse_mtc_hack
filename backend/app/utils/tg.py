import requests

import asyncio

from app.config import log
from app.config import settings


async def parse_channel(link: str, counter: int = 0) -> bool:
    """Parse channel name from link"""
    if counter > 5:
        log.error('Parse channel error')
        return False

    params = {
        'link': link
    }

    r = requests.post(
        f'{settings.TG_SERVICE_HOST}:{settings.TG_SERVICE_PORT}/schedule',
        json=params,
    )

    if r.status_code == 200:
        pass
    elif r.status_code == 409:
        await asyncio.sleep(3)
        await parse_channel(link, counter + 1)

    return True
