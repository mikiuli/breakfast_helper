from config import TOKEN, USER, HOST, PASSWORD, DATABASE

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from mysql.connector import connect, Error

from time import sleep

bot: Bot = Bot(token=TOKEN)
dp = Dispatcher()

async def process_start_command(message: Message):
    await message.answer('Привет! Я помогу тебе выбрать завтрак! Напиши "/bf"')

async def process_help_command(message: Message):
    await message.answer('Я бот, который помогает выбирать завтраки, нажми "/bf"')

async def get_a_breakfast(message: Message):
    try:
        with connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        ) as connection:
            get_a_breakfast_query = """
            SELECT *
            FROM breakfast
            ORDER BY RAND()
            LIMIT 1"""
            with connection.cursor() as cursor:
                cursor.execute(get_a_breakfast_query)
                result = cursor.fetchall()
                print(result)
    except Error:
        print(Error)
    await message.answer(result[0][1])
    breakfast_image = 'https://static.1000.menu/res/640/img/content' + result[0][9]
    try:
        await message.answer_photo(breakfast_image)
    except Error:
        print(Error)
    for ingridient in result[0][2].split(';'):
        sleep(0.1)
        await message.answer(ingridient)
    sleep(1)
    await message.answer('Для другого завтрака пальчиком сюда -> "/bf"')

dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(get_a_breakfast, Command(commands=['bf']))

if __name__ == '__main__':
    dp.run_polling(bot)