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

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
y = yadisk_async.YaDisk(token=YA_TOKEN)
moscow_timezone = pytz.timezone('Europe/Moscow')

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer("Привет! Синхронизируемся?")

@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer("Присылай что хочешь - я отправлю это в яндекс диск")

@dp.message(F.photo)
async def process_save_photo(message: Message, bot: Bot):
    photo_id = message.photo[-1].file_id
    await bot.download(message.photo[-1], destination=f"tmp/{photo_id}.jpg")
    await y.upload(f"tmp/{photo_id}.jpg", f"test/photos/{photo_id}.jpg")
    for f in os.listdir('tmp'):
        os.remove(os.path.join('tmp', f))
    await message.answer("Фото сохранено")
    await y.close()

@dp.message(F.document)
async def process_answers(message: Message):
    doc_id = message.document.file_id
    await bot.download(message.document, destination=f"tmp/{doc_id}")
    await y.upload(f"tmp/{doc_id}", f"test/docs/{doc_id}")
    for f in os.listdir('tmp'):
        os.remove(os.path.join('tmp', f))

    await message.answer("Документ сохранен")
    await y.close()

@dp.message()
async def process_save_text(message: Message):
    with open("tmp.txt", "w+") as file:
        file.write(message.text)
    file_name = message.date.astimezone(moscow_timezone).ctime()
    await y.upload("tmp.txt", f"home_pc/Obsidian_Vault/Notes/{file_name}.md")
    os.remove('tmp.txt')
    await message.answer(f"Сохранил в файл {file_name}")
    await y.close()
    
if __name__ == '__main__':
    dp.run_polling(bot)