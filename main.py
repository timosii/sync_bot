from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import F
from config import settings
import yadisk_async
import os
import pytz


BOT_TOKEN = settings.BOT_TOKEN
YA_TOKEN = settings.YA_TOKEN
YA_PATH_FILES = 'From_TG'
MESSAGES_PATH = 'home_pc/Obsidian_Vault/Notes'


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
y = yadisk_async.YaDisk(token=YA_TOKEN)
moscow_timezone = pytz.timezone('Europe/Moscow')


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer("Привет! Cинхронизируемся?")

@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer("Присылай сообщение, файл или фото - я отправлю это в яндекс диск")

@dp.message(F.content_type.in_({'photo', 'document'}))
async def process_save_files(message: Message, bot: Bot):
    if message.photo:
        photo_id = message.photo[-1].file_id
        await bot.download(message.photo[-1], destination=f"tmp/{photo_id}.jpg")
        await y.upload(f"tmp/{photo_id}.jpg", f"{YA_PATH_FILES}/photos/{photo_id}.jpg")
        await message.answer(text=f"Фото сохранено")
    else:
        doc_id = message.document.file_id
        await bot.download(message.document, destination=f"tmp/{doc_id}")
        await y.upload(f"tmp/{doc_id}", f"{YA_PATH_FILES}/docs/{doc_id}")
        await message.answer("Документ сохранен")
    await y.close()
    for f in os.listdir('tmp'):
        os.remove(os.path.join('tmp', f))  

@dp.message()
async def process_save_text(message: Message):
    if message.text.lower() in ["да", "давай"]:
        await message.answer("Присылай сообщение, фото или видео")
    else:
        with open("tmp.txt", "w+") as file:
            file.write(message.text)
        file_name = message.date.astimezone(moscow_timezone).ctime()
        await y.upload("tmp.txt", f"home_pc/Obsidian_Vault/Notes/{file_name}.md")
        os.remove('tmp.txt')
        await message.answer(f"Сохранил в файл {file_name}")
        await y.close()
    
if __name__ == '__main__':
    dp.run_polling(bot)
