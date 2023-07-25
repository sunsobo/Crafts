import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot("YOU_TELE_BOT")
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, '''
        Добро пожаловь в мой телеграм бот!
        -> У нас вы можете произвести быстрый обмен по популярным направлениям
        -> Или можете произвести обмен интересующего вас направления
        -> Для работы в боте, используется понятный интерфейс!
        ''')
    bot.send_message(message.chat.id, 'Введите сумму:')
    bot.register_next_step_handler(message, target)

def target(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, введи занаво:')
        bot.register_next_step_handler(message, target)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn4 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
        btn5 = types.InlineKeyboardButton('Другое значение:', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Выберите направление обмена:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше нуля, введи занаво:')
        bot.register_next_step_handler(message, target)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Результат: {round(res, 2)}. Слейдующий обмен, введите сумму:")
        bot.register_next_step_handler(call.message, target)
    else:
        bot.send_message(call.message.chat.id, 'Введите паролу через "/", Пример: USD/GBP')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Результат: {round(res, 2)}. Слейдующий обмен, введите сумму:")
        bot.register_next_step_handler(message, target)
    except Exception:
        bot.send_message(message.chat.id, "Что-то пошло не по плану! Пробуй ещё раз, введи значение:")
        bot.register_next_step_handler(message, my_currency)




bot.polling(none_stop=True)
