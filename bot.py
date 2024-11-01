import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import init_db, add_user, get_points, update_points

API_TOKEN = '7211622201:AAH6uicWDk-pyBRpXdHa1oPDjX0pu6pnLaw'  # Замените на токен вашего бота

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация базы данных
init_db()

# Обработчик команды /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    add_user(user_id, username)
    await message.reply("Добро пожаловать! Вы зарегистрированы.")

# Обработчик команды /score
@dp.message(Command('score'))
async def score_command(message: types.Message):
    user_id = message.from_user.id
    points = get_points(user_id)
    if points is not None:
        await message.reply(f"Ваш текущий счет: {points} очков.")
    else:
        await message.reply("Вы не зарегистрированы. Используйте команду /start для регистрации.")

# Обработчик данных от Web App
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    user_id = message.from_user.id
    data = message.web_app_data.data  # Получение данных от Web App

    if data == 'level_completed':
        current_points = get_points(user_id)
        if current_points is not None:
            new_points = current_points + 100
            update_points(user_id, new_points)
            await message.reply("Поздравляем! Вы завершили уровень и получили 100 очков.")
        else:
            await message.reply("Вы не зарегистрированы. Используйте команду /start для регистрации.")

# Обработчик команды /play для отправки кнопки с Web App
@dp.message(Command('play'))
    
    router = Router()

@router.message(Command(commands=['play']))
async def play_command(message: Message):
    # Создаем кнопку с WebAppInfo
    web_app_button = InlineKeyboardButton(
        text="Играть",
        web_app=WebAppInfo(url="https://karos7777.github.io/chujoy/")  # Замените на URL вашего Web App
    )

    # Создаем разметку клавиатуры и добавляем в нее кнопку
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

    await message.answer("Нажмите кнопку ниже, чтобы начать игру.", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
