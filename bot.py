import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Message, WebAppData
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = '7211622201:AAH6uicWDk-pyBRpXdHa1oPDjX0pu6pnLaw'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
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
@dp.message(CommandStart())
async def start_command(message: Message):
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
@dp.message(commands=['score'])
async def score_command(message: Message):
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
@dp.message(lambda message: message.web_app_data is not None)
async def web_app_data_handler(message: Message):
    user_id = message.from_user.id
    data = message.web_app_data.data  # Получение данных от Web App

    # Обработка полученных данных
    if data == '{"action": "level_completed"}':
        # Начисляем очки за завершение уровня
        cursor.execute('UPDATE users SET points = points + 100 WHERE user_id = ?', (user_id,))
        conn.commit()
        await message.reply("Поздравляем! Вы завершили уровень и получили 100 очков.")

# Обработчик команды /play для отправки кнопки с Web App
@dp.message(commands=['play'])
async def play_command(message: Message):
    keyboard = InlineKeyboardBuilder()
    web_app_button = InlineKeyboardButton(
        text="Играть",
        web_app=WebAppInfo(url="https://karos7777.github.io/chujoy/")  # Замените на URL вашего Web App
    )
    keyboard.add(web_app_button)
    await message.reply("Нажмите кнопку ниже, чтобы начать игру.", reply_markup=keyboard.as_markup())

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
