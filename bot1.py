import telebot
import random
import json
from telebot import types
 
# задаем текстовые файлы 
f = open('fact.txt', 'r', encoding='UTF-8')
facts = f.read().split('.')
f.close()

f = open('gencongratulation.txt', 'r', encoding='UTF-8')
cong  = f.read().split('***')
f.close()



# Создаем экземпляр бота
bot = telebot.TeleBot('')


DATABASE_FILE = "my_giftdata.json"

# Загружаем словарь из файла JSON или создаем пустой, если файла не существует
try:
    with open(DATABASE_FILE, 'r') as f:
        mygift = json.load(f)
except FileNotFoundError:
    mygift = {}

# Function to save the dictionary to the JSON file
def save_data():
    with open(DATABASE_FILE, 'w') as f:
        json.dump(mygift, f)

@bot.message_handler(commands=['add'])
def add_key(message):
    try:
        # Extract the key and value from the command arguments
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            bot.reply_to(message, "Please provide a key and a value. Example: /add my_key my_value")
            return

        key = parts[1].strip()
        value = parts[2].strip()

        mygift[key] = value
        save_data()  # Save the updated dictionary to the file
        bot.reply_to(message, f"Key '{key}' with value '{value}' added successfully.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

@bot.message_handler(commands=['show'])
def show_dictionary(message):
    if mygift:
        response = "Current dictionary:\n"
        for key, value in mygift.items():
            response += f"- {key}: {value}\n"
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "The dictionary is currently empty.")

@bot.message_handler(commands=['del'])
def delete_key(message):
    try:
        # Extract the key to delete from the command arguments
        key_to_delete = message.text.split(' ', 1)[1].strip()

        if key_to_delete in mygift:
            del mygift[key_to_delete]
            save_data()  # Save the updated dictionary to the file
            bot.reply_to(message, f"Key '{key_to_delete}' deleted successfully.")
        else:
            bot.reply_to(message, f"Key '{key_to_delete}' not found in the dictionary.")
    except IndexError:
        bot.reply_to(message, "Please provide a key to delete. Example: /delete my_key")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}") 

@bot.message_handler(commands=['gen'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
    btn1 = types.KeyboardButton('Сгенерировать поздравление')
    markup.add(btn1)
    answer = random.choice(cong)
    bot.send_message(message.from_user.id, "```" + answer + "```", parse_mode='MarkdownV2', reply_markup=markup)

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что дарить?")
    btn2 = types.KeyboardButton("Когда день рождения?")
    btn3 = types.KeyboardButton("Итересный факт")
    markup.add(btn1,btn3)
    markup.add(btn2)
    bot.send_message(message.from_user.id, "Здравствуй,\U0001F44B тебя приветствует бот дня рождения Степана.\U0001F423 Что бы ты хотел узнать?", reply_markup=markup)
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Что дарить?' or message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Подарю деньги')
        btn2 = types.KeyboardButton('Выбрать подарок')
        markup.add(btn1, btn2,)
        bot.send_message(message.from_user.id, 'Лучший подарок это деньги, но не самый приятный.', reply_markup=markup) #ответ бота
    elif message.text == 'Выбрать подарок' or message.text == 'Выбрать другой':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Все')
        btn2 = types.KeyboardButton('1000 - 2000')
        btn3 = types.KeyboardButton('500 - 1000')
        btn4 = types.KeyboardButton('2000 - 5000')
        btn5 = types.KeyboardButton('5000 <')
        btn6 = types.KeyboardButton('Назад')
        markup.add(btn1)
        markup.add(btn3, btn2)
        markup.add(btn4, btn5)
        markup.add(btn6)
        bot.send_message(message.from_user.id, 'Можно выбрать категории или посмотреть все варианты. \n Ссылки даны на "Озон", но не являются указанием к покупке именно на этом маркетплейсе.', reply_markup=markup)
    elif message.text == 'Когда день рождения?':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Что дарить?')
        btn2 = types.KeyboardButton('Итересный факт')
        markup.add(btn1, btn2,)
        bot.send_message(message.from_user.id, '1 марта 1994 года. \n31 год назад.', reply_markup=markup)
    elif message.text == 'Итересный факт':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Что дарить?')
        btn2 = types.KeyboardButton('Когда день рождения?')
        btn3 = types.KeyboardButton('Итересный факт')
        markup.add(btn1, btn2)
        markup.add(btn3)
        answer = random.choice(facts)
        bot.send_message(message.from_user.id, answer, reply_markup=markup)  
    elif message.text == 'Подарю деньги':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Сгенерировать поздравление')
        btn2 = types.KeyboardButton('Назад')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.from_user.id, "Отлично! \nЕще тут можно оставить приятное поздравление, которое именинник сможет прочесть в свой день рождения. \nЧто бы сгенирировать поздравление нажмите \U000025B6/gen \nВыбери из понравившихся вариантов, скопируй нажав на текст и вставь в строку написания сообщения или придумай свое.", reply_markup=markup) #ответ бота
    elif message.text == 'Сгенерировать поздравление':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Сгенерировать поздравление')
        markup.add(btn1)
        answer = random.choice(cong)
        bot.send_message(message.from_user.id, "```" + answer + "```", parse_mode='MarkdownV2', reply_markup=markup) #ответ бота
    elif message.text == 'Все':
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            mygift = json.load(f)
        for key, value in mygift.items():
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn2 = types.InlineKeyboardButton(text="Забронировать", callback_data = f'reserve_{key}')
            markup.add(btn2)
            bot.send_message(message.chat.id, key, reply_markup = markup)  
    elif message.text == '500 - 1000':
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            mygift = json.load(f)
            found_gift = False
        for key, value in mygift.items():
            if 500 <= int(value) <= 1000:
                found_gift = True
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn2 = types.InlineKeyboardButton(text="Забронировать", callback_data = f'reserve_{key}')
                markup.add(btn2)
                bot.send_message(message.chat.id, key, reply_markup = markup)
        if not found_gift:
            bot.send_message(message.chat.id, 'В этой категории не осталось подарков 😔')
    elif message.text == '1000 - 2000':
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            mygift = json.load(f)
            found_gift = False
        for key, value in mygift.items():
            if 1000 <= int(value) <= 2000:
                found_gift = True
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn2 = types.InlineKeyboardButton(text="Забронировать", callback_data = f'reserve_{key}')
                markup.add(btn2)
                bot.send_message(message.chat.id, key, reply_markup = markup)
        if not found_gift:
            bot.send_message(message.chat.id, 'В этой категории не осталось подарков 😔')
    elif message.text == '2000 - 5000':
        found_gift = False
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            mygift = json.load(f)
        for key, value in mygift.items():
            if 2000 <= int(value) <= 5000:
                found_gift = True
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn2 = types.InlineKeyboardButton(text="Забронировать", callback_data = f'reserve_{key}')
                markup.add(btn2)
                bot.send_message(message.chat.id, key, reply_markup = markup)
        if not found_gift:
            bot.send_message(message.chat.id, 'В этой категории не осталось подарков 😔')
    elif message.text == '5000 <':
        found_gift = False
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            mygift = json.load(f)
        for key, value in mygift.items():
            if int(value) >= 5000:
                found_gift = True
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn2 = types.InlineKeyboardButton(text="Забронировать", callback_data = f'reserve_{key}')
                markup.add(btn2)
                bot.send_message(message.chat.id, key, reply_markup = markup)
        if not found_gift:
            bot.send_message(message.chat.id, 'В этой категории не осталось подарков 😔')                       
    elif message.text != "Когда день рождения?":
        file_name = "congratulation.txt"
        f = open(file_name, 'a')
        f.write(message.from_user.first_name + ' | ' + message.text + '\n' + '------------------------------------------------------' + '\n')
        f.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Итересный факт')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Спасибо.\U0001F973 \nВсего хорошего', reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            mygift = json.load(f)
    key = call.data.split('_')[1]        
    if key in mygift.keys():
        if key in mygift:
            del mygift[key]
            save_data()
            file_name = "lockgift.txt"
            with open(file_name, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{user_id} | {key}\n")
            bot.answer_callback_query(call.id, show_alert=True, text="Вы забронировали подарок. \nТеперь он пропал из поиска у других пользователей. ")
            bot.send_message(call.message.chat.id, "Забронированный выми подарок\U00002935 \nДля того, чтобы отменить бронь, напишите в строке ввода: /add ссылка на товар и стоимость через пробел без указания валюты " + key)
        bot.send_message(call.message.chat.id, "Отлично! \nЕще тут можно оставить приятное поздравление, которое именинник сможет прочесть в свой день рождения. \nЧто бы сгенирировать поздравление нажмите \U000025B6/gen \nВыбери из понравившихся вариантов, скопируй нажав на текст и вставь в строку написания сообщения или придумай свое.'")
        with open(DATABASE_FILE, 'w') as f:
             json.dump(mygift, f)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
