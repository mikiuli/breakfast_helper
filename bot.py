from time import sleep

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message

from config import load_config
from database import get_a_breakfast

config = load_config()
BOT_TOKEN = config.tg_bot.token
ADMIN_IDS = list(config.tg_bot.admin_ids)


bot: Bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class Admin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет! Я помогу тебе выбрать завтрак! Напиши "/bf"')

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Я бот, который помогает выбирать завтраки, нажми "/bf"')

@dp.message(Command(commands=['bf']))
async def show_a_breakfast_recipe(message: Message):
    result = get_a_breakfast()
    await message.answer(result[0][1])
    breakfast_image = 'https://static.1000.menu/res/640/img/content' + result[0][9]
    try:
        await message.answer_photo(breakfast_image)
    except Exception:
        print(Exception)
    for ingridient in result[0][2].split(';'):
        sleep(0.1)
        await message.answer(ingridient)
    sleep(1)
    await message.answer('Для другого завтрака пальчиком сюда -> "/bf"')

@dp.message(Admin(ADMIN_IDS))
async def answer_to_admin(message: Message):
    await message.answer("Я знаю, что ты админ :)")

# @dp.message()


if __name__ == '__main__':
    dp.run_polling(bot)