from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from traceback import format_exc
from telebot import TeleBot
from script import Checker

bot = TeleBot("5443313691:AAEHu9IIJ6BnTLuLmH6we4PEDizIE2Vksug")
socials = list(Checker.url.keys())
socials.remove('ethscan')
caller = lambda checker, *a, **kw: checker._check(*a, **kw)


def social_media_keyboard():
    markup = InlineKeyboardMarkup()
    markups = [InlineKeyboardButton(site, callback_data=site)
               for site in socials]
    markup.add(*markups)
    return markup


def keyboard():
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Contract Ara", callback_data='contract_ara')
    markup.add(button)
    return markup


def send_collects(site, collects):
    return ', '.join([Checker.url[site](collect) for collect in collects])


def get_contract(message):
    if Checker.ethscan(message.text):
        global checker
        checker = Checker(Checker.get_coin_informations())

        name = " ".join(checker.info["name"])
        symbol = "".join(checker.info["symbol"])

        dex = f'dexscreener.com/ethereum/{message.text}'
        symbol = f'{name}(${symbol})'
        contract = f'Kontrat: {message.text}'

        msg = "\n".join([symbol, dex, contract])

        bot.send_message(message.chat.id, msg,
                         reply_markup=social_media_keyboard())


def send_message(bot, chat_id, text):
    try:
        bot.send_message(chat_id, text)
    except Exception as e:
        if 'message is too long' in str(e):
            for i in range(0, len(text)+1, 4096):
                text_ = text[i:i+4096]
                if text_ != '':
                    bot.send_message(chat_id, text_)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "İşlemi Seçin", reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    match call.data:
        case 'contract_ara':
            bot.send_message(
                call.message.chat.id, 'Lütfen aramak istediğiniz tokenin contractını girin:')
            bot.register_next_step_handler(call.message, get_contract)
        case _:
            try:
                bot.send_message(call.message.chat.id,
                                 f'{call.data} kontrol edilmeye başlandı')
                collects = caller(checker, getattr(
                    checker, call.data), call.data)
                msg = f'{call.data.upper()}\n{send_collects(call.data, collects)}'
                send_message(bot, call.message.chat.id, msg)
            except Exception as e:
                bot.send_message(call.message.chat.id, format_exc())


bot.infinity_polling(timeout=500)
