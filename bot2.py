import telebot
import psycopg2
from telebot import types
import os

# Получите URL вашей базы данных PostgreSQL из переменной окружения на платформе Railway
DATABASE_URL = "postgresql://postgres:Rt3Pjsqg0hyocZArFw2Z@containers-us-west-86.railway.app:6042/railway"

# Инициализируем Telegram бота
bot = telebot.TeleBot('6509291140:AAFc9XmUUPzfo_h2jz_km22MX25Xjga9aWs')

try:
    # Подключаемся к базе данных PostgreSQL
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
        sticker_id = 'CAACAgIAAxkBAAEKbFRlGFifpx0Q0UbzLXpiLSd29qr0dAACIz4AAhAmwEhtUD59z9j9GzAE'  # Замените на реальную ссылку на ваш стикер
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

        # Запрос к базе данных PostgreSQL для получения списка учебников
        cursor.execute("SELECT id, name FROM textbooks")
        textbooks = cursor.fetchall()

        # Создаем InlineKeyboardMarkup с кнопками для выбора учебника
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for textbook in textbooks:
            textbook_id, textbook_name = textbook
            key = types.InlineKeyboardButton(text=textbook_name, callback_data=f'textbook_{textbook_id}')
            keyboard.add(key)

        bot.send_message(message.chat.id, text='Выберите учебник:', reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, "Сервер не ответил, попробуйте еще раз.")

# Обработчик нажатий на кнопки учебников
@bot.callback_query_handler(lambda call: call.data.startswith('textbook_'))
def handle_textbook_query(call):
    textbook_id = int(call.data.split('_')[1])

    # Запрос к базе данных PostgreSQL для получения списка задач для выбранного учебника
    cursor.execute("SELECT id, name FROM tasks WHERE textbook_id = %s", (textbook_id,))
    tasks = cursor.fetchall()

    # Создаем InlineKeyboardMarkup с кнопками для выбора задачи
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        task_id, task_name = task
        key = types.InlineKeyboardButton(text=task_name, callback_data=f'task_{task_id}')
        keyboard.add(key)

    bot.send_message(call.message.chat.id, text='Выберите задачу:', reply_markup=keyboard)

# Обработчик нажатий на кнопки задач
@bot.callback_query_handler(lambda call: call.data.startswith('task_'))
def handle_task_query(call):
    task_id = int(call.data.split('_')[1])

    # Запрос к базе данных PostgreSQL для получения информации о выбранной задаче
    cursor.execute("SELECT name, solution, image_url FROM tasks WHERE id = %s", (task_id,))
    task_data = cursor.fetchone()

    if task_data:
        task_name, solution_text, image_url = task_data
        bot.send_message(call.message.chat.id, text=f'Задача: {task_name}\nРешение:\n{solution_text}')
        
        if image_url:
            bot.send_photo(call.message.chat.id, photo=image_url)  # Отправляем изображение
    else:
        bot.send_message(call.message.chat.id, text='Решение задачи не найдено.')

# Запускаем бота
bot.polling()
