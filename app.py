from dotenv import dotenv_values

from src.news_crawler.applications import Application

Application(db_config=dotenv_values("./env/db_config.env")).pipeline()  # type: ignore
