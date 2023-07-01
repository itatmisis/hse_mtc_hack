import requests

import time

from app.config import log
from app.config import settings


def parse_channel(link: str, counter: int = 0) -> bool:
    """Parse channel name from link"""
    if counter > 5:
        log.error('Parse channel error')
        return False

    params = {
        'group_handle': link
    }

    r = requests.post(
        f'http://{settings.COORDINATOR_HOSTNAME}/schedule',
        params=params,
    )

    if r.status_code == 200:
        pass
    elif r.status_code == 409:
        time.sleep(4)
        parse_channel(link, counter + 1)

    return True
