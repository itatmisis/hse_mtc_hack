from typing import Any, Dict

import uvicorn
from fastapi import FastAPI

from core.settings import uvicorn_settings
from presentation.main import app


uvicorn_app = app

if __name__ == "__main__":
    uvicorn.run(
        "entrypoints:uvicorn_app",
        host=uvicorn_settings.host,
        port=uvicorn_settings.port,
    )
