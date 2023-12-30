import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    YA_TOKEN = os.getenv('YA_TOKEN')

settings = Settings()