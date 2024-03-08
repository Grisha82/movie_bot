import sqlite3

from constants import GENRES

from random import sample

import os


def get_db_connection():
    conn = sqlite3.connect('movies.db')
    return conn


def create_db():
    conn = get_db_connection()
    for genre in GENRES:
        _genre = GENRES[genre][:-4]
        conn.execute(
        f'''CREATE TABLE IF NOT EXISTS {_genre}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                link TEXT
            );
        ''')
        conn.commit()
    conn.close()


def add_movies_in_db():
    conn = get_db_connection()
    for filename in os.listdir('movies'):
        if filename in GENRES.values():
            with open('movies/' + filename, encoding='utf-8') as file:
                genre = filename[:-4]
                movies = file.readlines()
                for movie in movies:
                    movie = movie.split(' - ')
                    if len(movie) > 2:
                        print(movie, filename)
                        continue
                    conn.execute(f'INSERT INTO {genre} (title, link) VALUES (?, ?);', movie)
                    conn.commit()
    conn.close()


def get_movies_list(tablename_of_selected_genre, counts_movies):
    tablename = tablename_of_selected_genre[:-4]
    conn = get_db_connection()
    movies = conn.execute(f'SELECT title, link FROM {tablename};').fetchall()
    select_movies = sample(movies, k=counts_movies)
    return select_movies


if __name__ == '__main__':
    create_db()
    add_movies_in_db()

