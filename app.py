from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from dotenv import load_dotenv
import os
from pprint import pprint
from random import randint


load_dotenv('.env')
BOT_TOKEN = os.getenv('TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

user = {
    'in_game': False,
    'secret_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}


def generate_num_from_100() -> int:
    return randint(0, 100)


async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
        )


async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


async def process_stat_command(message: Message):
    await message.answer(
        f'Всего иго сыграно: {user["total_games"]}\n'
        f'Игр выиграно: {user["wins"]}'
    )


async def process_cancel_command(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Вы вышши из игры. Если захотите сыграть '
            'снова - пишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


async def process_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = generate_num_from_100()
        user['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


async def process_numbers_answer(message: Message):
    user_num = int(message.text)
    if user['in_game']:
        if user_num == user['secret_number']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer(
                'УРА! Вы угадали число!\n\n'
                'Может, сыграем ещё?'
            )
        elif user_num > user['secret_number']:
            user['attempts'] -= 1
            await message.reply(
                'Моё число меньше'
            )
        elif user_num > user['secret_number']:
            user['attempts'] -= 1
            await message.reply(
                'Моё число больше'
            )
        
        if not user['attempts']:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {user["secret_number"]}\n\nДавайте '
                f'сыграем ещё?'
            )
    else:
        await message.answer(
            'Мы ещё не играем. Хотите сыграть?'
        )


async def process_other_answer(message: Message):
    if user['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(process_stat_command, Command(commands=['stat']))
dp.message.register(process_cancel_command, Command(commands=['cancel']))
dp.message.register(process_positive_answer, F.text.lower().in_(['да', 'давай', 'сграем', 'игра', 'играть', 'хочу играть']))
dp.message.register(process_negative_answer, F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
dp.message.register(process_numbers_answer, lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.message.register(process_other_answer)


if __name__ == '__main__':
    dp.run_polling(bot)