import telebot
from telebot import types
import json
import os

bot = telebot.TeleBot("8106995408:AAFY4DXMJMpANiBon9CfyvKZ0Kq4qJAwmt4")


@bot.message_handler(commands=["start"])
def _start_(massage):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("/help")
    btn2 = types.KeyboardButton("/cook_new_year")
    btn3 = types.KeyboardButton("/mandarin")
    markup.add(btn1, btn3, btn2)
    btn4 = types.KeyboardButton("/my_birthday")
    btn5 = types.KeyboardButton("/new_year")
    btn6 = types.KeyboardButton("/room_new_year")
    markup.add(btn5, btn4, btn6)
    bot.send_message(massage.chat.id, f"Приветствуем вас, {massage.from_user.first_name}"
                                      f"! \n🎅Вы запустили новогоднего бота, он вам поможет в приготовлениях к празднику "
                                      f"и развлечёт мини игрой.", reply_markup=markup)


@bot.message_handler(commands=["my_birthday"])
def _birthday_(massage):
    bot.send_message(massage.chat.id, "Поздраляем! Вот подарочек от разработчика:")
    markup = types.ReplyKeyboardMarkup()
    file = open("./birthday.mp4", "rb")
    bot.send_video(massage.chat.id, file, reply_markup=markup)


@bot.message_handler(commands=["cook_new_year"])
def _cook_new_year_(massage):
    bot.send_message(massage.chat.id,"интересуешься что накрыть на Новогодний стол?\n"
                                     "Мы поготовили парочку сайтов где собраны великолепные реценты разной сложности\n"
                                     "· https://1000.menu/catalog/novogodnie-retseptj\n"
                                     "· https://rg.ru/2024/11/22/novogodnij-stol-2025-chto-prigotovit-i-kak-ukrasit.html\n"
                                     "· https://www.mn.ru/smart/menyu-na-novogodniy-stol-2025\n")

@bot.message_handler(commands=["new_year"])
def _new_year_(massage):
    bot.send_message(massage.chat.id, "Поздраляем, с новым годом!")
    markup = types.ReplyKeyboardMarkup()
    file = open("./2697117634_preview_1514742107123228306.png", "rb")
    bot.send_photo(massage.chat.id, file, reply_markup=markup)


@bot.message_handler(commands=["room_new_year"])
def _room_new_year_(massage):
    bot.send_message(massage.chat.id,"Интересуешься как можно красить комнату к новому году? "
                                     "Мы подготовили несколько сайтов которые помогут решить вашу проблему.\n"
                                     "· https://lafoy.ru/kak-ukrasit-kvartiru-na-novyy-god-1253\n"
                                     "· https://dzen.ru/a/Z2ARvFH_sSiVV_XH\n"
                                     "· https://lavka-obitel.ru/blog/ukrashaem-dom-k-rozdestvu-y-novomu-hodu\n")

@bot.message_handler(commands=["help"])
def _help_f_(massage):
    bot.send_message(massage.chat.id, "· /start: начать общаться \n"
                                      "· /mandarin: счётчик мандаринов\n"
                                      "· /room_new_year: не знаешь как можно украсить команту? Мы подскажем!\n"
                                      "· /my_birthday: нажмите, если сейчас у вас день рожденье, что же мы вам приготовили?\n"
                                      "· /new_year: нажмите, если сейчас у вас скоро новый год\n"
                                      "· /cook_new_year: не знаешь что приготовить к Новому году? Подскажем!")


def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return {}


def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)


@bot.message_handler(commands=['mandarin'])
def start(message):
    user_id = str(message.from_user.id)
    users = load_users()

    if user_id not in users:
        users[user_id] = {'coins': 0}
        save_users(users)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_click = types.KeyboardButton('🍊 Съесть')
    btn_balance = types.KeyboardButton('💰🍊 Баланс')
    btn_top = types.KeyboardButton('🏆 Топ обжор')
    btn_exit = types.KeyboardButton('/start - выход из мини игры')
    markup.add(btn_click, btn_balance, btn_top)
    markup.add(btn_exit)
    bot.send_message(message.chat.id,
                     'Приветствую вас в разделе бота для счёта съеденных мандаринов! '
                     'Отмечайтесь как только съедите мандаринку:)🍊 ',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    users = load_users()

    if message.text == '🍊 Съесть':
        users[user_id]['coins'] += 1
        save_users(users)
        bot.reply_to(message, f'Вы съели мандарин! Всего съеденных: {users[user_id]["coins"]}')

    elif message.text == '💰🍊 Баланс':
        bot.reply_to(message, f'Ваше обжорство: {users[user_id]["coins"]} мандаринов')

    elif message.text == '🏆 Топ обжор':
        players = []
        for uid, data in users.items():
            try:
                user = bot.get_chat(uid)
                name = user.first_name
            except:
                name = "Без имени"
            players.append((name, data['coins']))

        players.sort(key=lambda x: x[1], reverse=True)

        top_message = "🏆 Топ-10 обжор:\n\n"
        for i, (name, coins) in enumerate(players[:10], 1):
            top_message += f"{i}. {name} {coins} мандаринов\n"

        bot.reply_to(message, top_message)


bot.polling(non_stop=True)
