import logging
import colorlog
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

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    logging.getLogger("uvicorn").setLevel(logging.WARNING)

    logging.info("Logger initialized successfully")

init_logger()

app = FastAPI()
app.include_router(question.router)
app.include_router(documents.router)
app.include_router(embedding.router)
