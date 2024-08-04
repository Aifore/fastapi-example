"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
import logging

from fastapi import FastAPI
from loguru import logger

logging.basicConfig(level="DEBUG")

from config import openapi_config
from initializer import init


app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
)
logger.info("Starting application initialization...")
init(app)
logger.success("Successfully initialized!")
