import os
from dotenv import load_dotenv
from unimate_logger import logger
load_dotenv(".env", override=True)

ENV_TYPE = os.getenv("ENV")
logger.info(f"ENVIRONMENT: {ENV_TYPE}")

PORT = os.getenv("PORT", 8080)
POSTGRES_DB_HOST = os.getenv("POSTGRES_DB_HOST")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_DB_USER = os.getenv("POSTGRES_DB_USER")
POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_DB_PASSWORD")
