import logging
import colorlog
import os
from fastapi import FastAPI
from agentic_rag.api import question, documents, embedding


def init_logger():
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)

    log_level_str = os.getenv("LOG_LEVEL", "DEBUG").upper()
    app_log_level = getattr(logging, log_level_str, logging.DEBUG)
    app_logger = logging.getLogger("agentic_rag")
    app_logger.setLevel(app_log_level)
    app_logger.addHandler(handler)
    app_logger.propagate = False

    logging.getLogger("uvicorn").setLevel(logging.WARNING)

    app_logger.info("Logger initialized successfully")

init_logger()

app = FastAPI()
app.include_router(question.router)
app.include_router(documents.router)
app.include_router(embedding.router)
