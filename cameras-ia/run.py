"""Sobe o servidor: python run.py"""
import logging

import uvicorn

from app.config import Settings
from app.main import create_app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings.from_env()
    uvicorn.run(create_app(settings), host=settings.host, port=settings.port)
