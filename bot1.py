import telebot
import random
from telebot import types

f = open('telegrambot/fact.txt', 'r', encoding='UTF-8')
facts = f.read().split('.')
f.close()

f = open('telegrambot/gencongratulation.txt', 'r', encoding='UTF-8')
cong  = f.read().split('***')
f.close()

mygift = {'Складная туристическая газовая горелка с чехлом' : 'https://ozon.ru/t/6xdj2j0', 
'Рюкзак мужской, городской, вакуумный' : 'https://ozon.ru/t/4GvmeLN',
'Фонарь' : 'https://ozon.ru/t/KKzRQ9B',
'ZRCX Сумка спортивная' : 'https://ozon.ru/t/jzJ24a',
'Aqara Умная розетка Aqara, модель SP-EUC01' : 'https://ozon.ru/t/qjzojk6',
'Aqara Умная камера и центр умного дома Aqara G2H Pro CH-C01, умный дом, белый' : 'https://ozon.ru/t/47k9EXR',
'Xiaomi Умная лампочка Mijia Display Light Lamp (черный)' : 'https://ozon.ru/t/8xrbQJg',
'Бутылка для воды(любая, от литра)' : 'https://ozon.ru/t/R1b2YpB',
'Льюис Хэмилтон со шлемом' : 'https://funkopoprussia.com/serials/racing/lewis-hamilton-with-helmet-funko-pop.html'}

# Создаем экземпляр бота
bot = telebot.TeleBot('7877815828:AAGzxRbe_crUiyRBp2esLbFQbmaDYKhEfXY')

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что дарить?")
    btn2 = types.KeyboardButton("Когда день рождения?")
    btn3 = types.KeyboardButton("Итересный факт")
    markup.add(btn1,btn3)
    markup.add(btn2)
    bot.send_message(message.from_user.id, "Здравствуй, тебя приветствует бот дня рождения степана. Что бы ты хотел узнать?", reply_markup=markup)
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Что дарить?':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Подарю деньги')
        btn2 = types.KeyboardButton('Выбрать подарок')
        markup.add(btn1, btn2,)
        bot.send_message(message.from_user.id, 'Лучший подарок это деньги, но не самый приятный.', reply_markup=markup) #ответ бота
    elif message.text == 'Выбрать подарок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Все')
        btn2 = types.KeyboardButton('Хобби')
        btn3 = types.KeyboardButton('Спорт')
        btn4 = types.KeyboardButton('Путишествия')
        btn5 = types.KeyboardButton('Дом')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        markup.add(btn4)
        markup.add(btn5)
        bot.send_message(message.from_user.id, 'Можно выбрать категории или посмотреть все варианты. \n Сылки даны на "Озон", но не являются указанием к покупке именно на этом маркетплейсе.', reply_markup=markup)
    elif message.text == '':
        markup = types.InlineKeyboardMarkup()
        for i in mygift:
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
            markup.add(btn1)
            bot.send_message(message.from_user.id, i)
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
        btn2 = types.KeyboardButton('Что дарить?')
        markup.add(btn1,btn2)
        bot.send_message(message.from_user.id,  'Отлично! \nЕще тут можно оставить приятное поздравление, которое именинник сможет прочесть в свой день рождения.', reply_markup=markup) #ответ бота
    
    elif message.text == 'Сгенерировать поздравление':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Сгенерировать поздравление')
        markup.add(btn1)
        answer = random.choice(cong)
        bot.send_message(message.from_user.id, "```" + answer + "```", parse_mode='MarkdownV2', reply_markup=markup) #ответ бота
    elif message.text == 'Все':
        for i in mygift:
            markup = types.InlineKeyboardMarkup()
            btn_my_site= types.InlineKeyboardButton(text='Сылка на ОЗОН', url= mygift.get(i))
            markup.add(btn_my_site)
            bot.send_message(message.chat.id, i, reply_markup = markup)    
    elif message.text != "Когда день рождения?":
        file_name = "congratulation.txt"
        f = open(file_name, 'a')
        f.write(message.from_user.first_name + ' | ' + message.text + '\n' + '------------------------------------------------------' + '\n')
        f.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Итересный факт')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Спасибо. \nВсего хорошего', reply_markup=markup)     
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Все':
        markup = types.InlineKeyboardMarkup()
        btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='https://habrahabr.ru')
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup = markup)    
# Запускаем бота
bot.polling(none_stop=True, interval=0)