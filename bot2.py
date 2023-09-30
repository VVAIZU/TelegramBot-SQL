#6372475462:AAHqvbkS5n-4p4J5oqXx0D9o9uAoWgomk8A
#accountant.db
import sqlite3
import telebot
from telebot import types

# Инициализируем Telegram бота
bot = telebot.TeleBot('6372475462:AAHqvbkS5n-4p4J5oqXx0D9o9uAoWgomk8A')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Выберите учебник:")

    # Создаем подключение к базе данных SQLite и объект cursor
    conn = sqlite3.connect('accountant.db')
    cursor = conn.cursor()

    # Получаем список учебников из базы данных
    cursor.execute("SELECT id, name FROM textbooks")
    textbooks = cursor.fetchall()

    # Создаем InlineKeyboardMarkup с кнопками для выбора учебника
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for textbook in textbooks:
        textbook_id, textbook_name = textbook
        key = types.InlineKeyboardButton(text=textbook_name, callback_data=f'textbook_{textbook_id}')
        keyboard.add(key)

    bot.send_message(message.chat.id, text='Выберите учебник:', reply_markup=keyboard)

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

# Другие обработчики сообщений и команд
# Обработчик нажатий на кнопки учебников
@bot.callback_query_handler(lambda call: call.data.startswith('textbook_'))
def handle_textbook_query(call):
    textbook_id = int(call.data.split('_')[1])

    # Создаем подключение к базе данных SQLite и объект cursor
    conn = sqlite3.connect('accountant.db')
    cursor = conn.cursor()

    # Получаем список задач для выбранного учебника
    cursor.execute("SELECT id, name FROM tasks WHERE textbook_id = ?", (textbook_id,))
    tasks = cursor.fetchall()

    # Создаем InlineKeyboardMarkup с кнопками для выбора задачи
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        task_id, task_name = task
        key = types.InlineKeyboardButton(text=task_name, callback_data=f'task_{task_id}')
        keyboard.add(key)

    bot.send_message(call.message.chat.id, text='Выберите задачу:', reply_markup=keyboard)

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

# Обработчик нажатий на кнопки задач
@bot.callback_query_handler(lambda call: call.data.startswith('task_'))
def handle_task_query(call):
    task_id = int(call.data.split('_')[1])

    # Создаем подключение к базе данных SQLite и объект cursor
    conn = sqlite3.connect('accountant.db')
    cursor = conn.cursor()

    # Получаем текст решения и URL изображения для выбранной задачи из базы данных
    cursor.execute("SELECT name, solution, image_url FROM tasks WHERE id = ?", (task_id,))
    task_data = cursor.fetchone()

    if task_data:
        task_name, solution_text, image_url = task_data
        bot.send_message(call.message.chat.id, text=f'Задача: {task_name}\nРешение:\n{solution_text}')
        
        if image_url:
            bot.send_photo(call.message.chat.id, photo=image_url)  # Отправляем изображение
    else:
        bot.send_message(call.message.chat.id, text='Решение задачи не найдено.')

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

# Запускаем бота
bot.polling()
