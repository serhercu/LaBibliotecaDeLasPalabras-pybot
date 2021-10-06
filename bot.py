import os
import datetime

import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

class PalabraNueva:
    def __init__(self, word, user, date, description):
        self.word = word
        self.user = user
        self.date = date
        self.description = description

PALABRA, DESCRIPCION, FIN = range(3)

def start(update, context):

    reply_keyboard = [['Añadir', 'Consultar', 'Ayuda']]

    update.message.reply_text(
        'Elige una opción',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='¿Qué quieres hacer?'
        ),
    )

    return PALABRA


def palabra(update, context):

    palabraNueva.user = update.effective_user['first_name']

    update.message.reply_text(
        'Añade tu palabra',
        reply_markup=ReplyKeyboardRemove(),
    )

    return DESCRIPCION

def descripcion(update, context):

    update.message.reply_text(
        'Añade la descripción',
        reply_markup=ReplyKeyboardRemove(),
    )

    print(update.message.text)

    palabraNueva.word = update.message.text

    return FIN

def fin(update, context):

    palabraNueva.description = update.message.text

    update.message.reply_text(
        f'{palabraNueva.word}. {palabraNueva.user}. {palabraNueva.date}',
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END



if __name__ == '__main__':

    updater = Updater(token='1817799228:AAHYSwjvs1lH5CjTdBeP9z1W_biizou17N8', use_context=True)

    dp = updater.dispatcher

    palabraNueva = PalabraNueva("", "", datetime.datetime.today().strftime('%d/%m/%Y'), "")

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],

        states= {
            PALABRA: [MessageHandler(Filters.regex('^(Añadir)$'), palabra)],
            DESCRIPCION: [MessageHandler(Filters.regex('^^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$'), descripcion)],
            FIN: [MessageHandler(Filters.regex('^^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$'), fin)],
            #INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },

        fallbacks=[]
    ))
    updater.start_polling()

    updater.idle()