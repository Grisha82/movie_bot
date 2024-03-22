from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard(genres):
    keybourd = []
    index_of_lines = 0
    for genre in genres:
        if index_of_lines % 2 == 0:
            keybourd.append(
                [InlineKeyboardButton(genre, callback_data=genres[genre])]
            )
        else:
            keybourd[index_of_lines // 2].append(
                InlineKeyboardButton(genre, callback_data=genres[genre])
            )
        index_of_lines += 1
    reply_markup = InlineKeyboardMarkup(keybourd)
    return reply_markup


def set_genre(filename_of_selected_genre, dict_with_genres):
    for genre in dict_with_genres:
        if filename_of_selected_genre == dict_with_genres[genre]:
            return genre


def generate_message_with_list_of_movies(movies_list):
    movies = ''
    for movie in movies_list:
        movies += f'- <a href="{movie[1]}">{movie[0]}</a>\n'
    return movies
