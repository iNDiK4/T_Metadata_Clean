import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ContentType, FSInputFile
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
import exiftool
import asyncio

TOKEN = 'YOUR_BOT_TOKEN'

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)

user_data = {}

@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне фотографию (как файл .jpg без сжатия), и я очищу метаданные и добавлю свои.")

@router.message(lambda message: message.content_type == ContentType.DOCUMENT)
async def handle_docs(message: types.Message):
    if message.document.mime_type == 'image/jpeg':
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = await bot.download_file(file_path)
        temp_path = f"temp_{message.from_user.id}.jpg"
        with open(temp_path, 'wb') as new_file:
            new_file.write(downloaded_file.get())
        user_data[message.from_user.id] = {'photo_path': temp_path}
        await process_image(message)

async def show_loading(message: types.Message):
    dots = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    msg = await message.reply("Обработка " + dots[0])
    last_text = "Обработка " + dots[0]
    
    for i in range(1, len(dots)):
        new_text = "Обработка " + dots[i]
        if new_text != last_text:
            try:
                await bot.edit_message_text(
                    text=new_text,
                    chat_id=message.chat.id,
                    message_id=msg.message_id
                )
                last_text = new_text
            except TelegramBadRequest:
                pass
        await asyncio.sleep(0.5)
    return msg

def update_metadata(file_path):
    with exiftool.ExifTool(executable='/usr/bin/exiftool') as et:
        et.execute(b"-all=", file_path.encode())
        et.execute(f"-Comment=This image was processed by the bot".encode(), file_path.encode())

async def process_image(message: types.Message):
    user_id = message.from_user.id
    photo_path = user_data[user_id]['photo_path']
    loading_msg = await show_loading(message)
    
    try:
        result_path = f"result_{os.path.basename(photo_path)}"
        with open(photo_path, 'rb') as src, open(result_path, 'wb') as dst:
            dst.write(src.read())
        update_metadata(result_path)
        await bot.send_document(message.chat.id, FSInputFile(result_path))
        os.remove(photo_path)
        os.remove(result_path)
    except Exception as e:
        await bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
    
    await bot.delete_message(message.chat.id, loading_msg.message_id)
    del user_data[user_id]

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())