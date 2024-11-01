import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Инициализация базы данных
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    points INTEGER DEFAULT 0
)
''')
conn.commit()

# Функция для добавления очков пользователю
def add_points(user_id, points):
    cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        current_points = result[0]
        cursor.execute('UPDATE users SET points = ? WHERE user_id = ?', (current_points + points, user_id))
    else:
        cursor.execute('INSERT INTO users (user_id, points) VALUES (?, ?)', (user_id, points))
    conn.commit()

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user.id, user.username))
    conn.commit()
    update.message.reply_text(f'Привет, {user.first_name}! Ваши очки: 0')

# Обработчик команды /score
def score(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        update.message.reply_text(f'Ваши очки: {result[0]}')
    else:
        update.message.reply_text('Вы еще не зарегистрированы. Используйте команду /start.')

# Обработчик текстовых сообщений
def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    add_points(user_id, 10)
    update.message.reply_text('Вы получили 10 очков!')

def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    updater = Updater('7211622201:AAH6uicWDk-pyBRpXdHa1oPDjX0pu6pnLaw', use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('score', score))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
