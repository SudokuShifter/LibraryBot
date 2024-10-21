from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from dotenv import load_dotenv
import os
from pprint import pprint


load_dotenv('.env')
BOT_TOKEN = os.getenv('TOKEN')


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Ся!\nНапиши мне что-нибудь')


async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твоё сообщение'
    )


async def send_photo_echo(message: Message):
    pprint(message)
    await message.reply_photo(message.photo[0].file_id)


async def send_echo(message: Message):
    await message.reply(text=message.text)


dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)