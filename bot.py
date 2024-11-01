import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '7211622201:AAH6uicWDk-pyBRpXdHa1oPDjX0pu6pnLaw'  # Замените на токен вашего бота

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера
dp = Dispatcher()

# Подключение к базе данных SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    points INTEGER DEFAULT 0
)
''')
conn.commit()

# Обработчик команды /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка, существует ли пользователь в базе данных
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user is None:
        # Если пользователя нет, добавляем его в базу данных
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
        await message.reply("Добро пожаловать! Вы зарегистрированы.")
    else:
        await message.reply("Вы уже зарегистрированы.")

# Обработчик команды /score
@dp.message(Command('score'))
async def score_command(message: types.Message):
    user_id = message.from_user.id

    # Получение текущего количества очков пользователя
    cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        points = result[0]
        await message.reply(f"Ваш текущий счет: {points} очков.")
    else:
        await message.reply("Вы не зарегистрированы. Используйте команду /start для регистрации.")

# Обработчик данных от Web App
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    user_id = message.from_user.id
    data = message.web_app_data.data  # Получение данных от Web App

    # Здесь вы можете обработать полученные данные
    # Например, если данные содержат информацию о завершении уровня:
    if data == 'level_completed':
        # Начисляем очки за завершение уровня
        cursor.execute('UPDATE users SET points = points + 100 WHERE user_id = ?', (user_id,))
        conn.commit()
        await message.reply("Поздравляем! Вы завершили уровень и получили 100 очков.")

# Обработчик команды /play для отправки кнопки с Web App
@dp.message(Command('play'))
async def play_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Играть",
            web_app=WebAppInfo(url="https://karos7777.github.io/chujoy/")  # Замените на URL вашего Web App
        )]
    ])
    await message.reply("Нажмите кнопку ниже, чтобы начать игру.", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
