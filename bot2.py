import telebot
import psycopg2
from telebot import types
import os


DATABASE_URL = ""


bot = telebot.TeleBot('')

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    print("Connected to PostgreSQL")
except psycopg2.OperationalError as e:
    print(f"Failed to connect to PostgreSQL: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        # Отправляем гифку
        sticker_id = 'CAACAgIAAxkBAAEKbFRlGFifpx0Q0UbzLXpiLSd29qr0dAACIz4AAhAmwEhtUD59z9j9GzAE' 
        bot.send_sticker(message.chat.id, sticker_id)

        # Отправляем приветственное сообщение
        welcome_message = (
        "Добро пожаловать в MonkeyStudyCo!\n"
        "Постоянная необходимость обновлять и расширять набор навыков сотрудников ставит перед компаниями непростую задачу: "
        "создать максимально эффективную систему обучения. Проект «Monkey Study Co.» представляет собой инновационную образовательную платформу, "
        "ориентированную на развитие навыков и переподготовку персонала в условиях быстро меняющегося рынка труда.\n"
        "Выберите учебник:"
        )

        bot.reply_to(message, welcome_message, parse_mode='Markdown')

        cursor.execute("SELECT id, name FROM textbooks")
        textbooks = cursor.fetchall()

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for textbook in textbooks:
            textbook_id, textbook_name = textbook
            key = types.InlineKeyboardButton(text=textbook_name, callback_data=f'textbook_{textbook_id}')
            keyboard.add(key)

        bot.send_message(message.chat.id, text='Выберите учебник:', reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, "Сервер не ответил, попробуйте еще раз.")

@bot.callback_query_handler(lambda call: call.data.startswith('textbook_'))
def handle_textbook_query(call):
    textbook_id = int(call.data.split('_')[1])

    cursor.execute("SELECT id, name FROM tasks WHERE textbook_id = %s", (textbook_id,))
    tasks = cursor.fetchall()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        task_id, task_name = task
        key = types.InlineKeyboardButton(text=task_name, callback_data=f'task_{task_id}')
        keyboard.add(key)

    bot.send_message(call.message.chat.id, text='Выберите задачу:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    try:
        user_message = message.text.strip()

        cursor.execute("SELECT id, name FROM textbooks WHERE name ILIKE %s", (user_message,))
        textbook = cursor.fetchone()

        if textbook:
            textbook_id, textbook_name = textbook

            cursor.execute("SELECT id, name FROM tasks WHERE textbook_id = %s", (textbook_id,))
            tasks = cursor.fetchall()

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for task in tasks:
                task_id, task_name = task
                key = types.InlineKeyboardButton(text=task_name, callback_data=f'task_{task_id}')
                keyboard.add(key)

            bot.send_message(message.chat.id, text=f'Выберите задачу из учебника "{textbook_name}":', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Учебник не найден. Выберите учебник из списка.")

    except Exception as e:
        bot.send_message(message.chat.id, "Сервер не ответил, попробуйте еще раз.")



#Обработчик нажатий на кнопки задач
@bot.callback_query_handler(lambda call: call.data.startswith('task_'))
def handle_task_query(call):
    task_id = int(call.data.split('_')[1])

    cursor.execute("SELECT name, solution, image_url FROM tasks WHERE id = %s", (task_id,))
    task_data = cursor.fetchone()

    if task_data:
        task_name, solution_text, image_url = task_data
        message_text = f'Задача: {task_name}\nРешение:\n{solution_text}'

        while len(message_text) > 4000:
            part, message_text = message_text[:4000], message_text[4000:]
            bot.send_message(call.message.chat.id, part, parse_mode='HTML')

        bot.send_message(call.message.chat.id, message_text, parse_mode='HTML')

        if image_url:
            bot.send_photo(call.message.chat.id, photo=image_url)
    else:
        bot.send_message(call.message.chat.id, text='Решение задачи не найдено.')

bot.polling()
