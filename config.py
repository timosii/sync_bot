import os

# from dotenv import load_dotenv

# load_dotenv()

class Settings:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    YA_TOKEN = os.environ['YA_TOKEN']

settings = Settings()