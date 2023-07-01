import uvicorn
from os import getenv

from app.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        use_colors=True,
        host="0.0.0.0",
        port=int(getenv("API_PORT", 80)),
    )
