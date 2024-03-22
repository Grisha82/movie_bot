import os

from dotenv import load_dotenv
from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from constants import COUNTS_MOVIES, GENRES
from db import get_movies_list
from utils import (generate_message_with_list_of_movies, inline_keyboard,
                   set_genre)

load_dotenv()

updater = Updater(token=os.getenv('TOKEN'))


def hello(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['выбрать фильм']], resize_keyboard=True)
    update.message.reply_text(
        f'Привет {chat.first_name}! Я помогу тебе выбрать фильм на вечер',
        reply_markup=button
    )


def find_out_genre_of_film(update, context):
    reply_markup = inline_keyboard(GENRES)
    update.message.reply_text('Выбери один из жанров:', reply_markup=reply_markup)


def send_list_of_movies(update, context):
    query = update.callback_query
    query.answer()
    filename_of_selected_genre = query.data
    movies_list = get_movies_list(
        filename_of_selected_genre, COUNTS_MOVIES
    )
    movies = generate_message_with_list_of_movies(movies_list)
    ganre = set_genre(filename_of_selected_genre, GENRES).lower()
    chat = update.effective_chat
    context.bot.send_message(
        chat.id,
        f'Вот {COUNTS_MOVIES} фильмов выбранного жанра - {ganre}:\n{movies}',
        parse_mode=ParseMode.HTML
    )


updater.dispatcher.add_handler(CommandHandler('start', hello))
updater.dispatcher.add_handler(
    MessageHandler(Filters.regex('^выбрать фильм$'), find_out_genre_of_film)
)
updater.dispatcher.add_handler(CallbackQueryHandler(send_list_of_movies))
updater.start_polling()
updater.idle()
