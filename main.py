"""The given script is used to get a random film \
to watch via the `/film` command to a Telegram bot. 
The current database consists of 4985 films."""

import logging
import random
import pymysql
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from data import Answers, Bot, Chat, Database, Movies, User


# The issue to fix: it is needed create the logs storage
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


ANSWERS = Answers()
BOT = Bot()
CHAT = Chat()
DATABASE = Database()
MOVIES = Movies()
USER = User()


# Database functions
def find_random_film() -> str:
    """Returns a random film."""
    try:
        with pymysql.connect(
            user=DATABASE.database["user"],
            password=DATABASE.database["password"],
            host=DATABASE.database["host"],
            database=DATABASE.database["database"],
            port=DATABASE.database["port"]
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT film FROM mysql.`films` ORDER BY RAND() LIMIT 1;")
            result = cursor.fetchone()
            return result[0] if result else None
    except pymysql.Error as e:
        logger.error("Database error: %s", e)
        return None


def give_random_answer(answers: tuple[str]) -> str:
    """Returns a random answer."""
    return random.choice(answers)


def get_list_of_genres() -> str:
    """Returns a list of genres."""
    genres_list = []
    try:
        with pymysql.connect(
            user=DATABASE.database["user"],
            password=DATABASE.database["password"],
            host=DATABASE.database["host"],
            database=DATABASE.database["database"],
            port=DATABASE.database["port"]
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT genre FROM mysql.`films`;")
            genres = cursor.fetchall()
            for genre in genres:
                genres_list.append(*genre)
            result = '\n'.join(genres_list)
            return result if result else None
    except pymysql.Error as e:
        logger.error("Database error: %s", e)
    return None


def get_list_of_directors() -> str:
    """Returns a list of directors."""
    directors_list = []
    try:
        with pymysql.connect(
            user=DATABASE.database["user"],
            password=DATABASE.database["password"],
            host=DATABASE.database["host"],
            database=DATABASE.database["database"],
            port=DATABASE.database["port"]
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT director FROM mysql.`films` ORDER BY RAND() LIMIT 10;")
            directors = cursor.fetchall()
            for director in directors:
                directors_list.append(*director)
            result = '\n'.join(directors_list)
            return result if result else None
    except pymysql.Error as e:
        logger.error("Database error: %s", e)
    return None


# def get_films_by_director(directors: list) -> list:
#     """Returns SQL queries to choose all films by their director."""
#     films = []
#     for d in directors:
#         films.append(
#             f"SELECT film FROM mysql.`films` WHERE director = {d};"
#         )
#     return films


# Telegram bot functions
async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /movie command."""
    if not update.message:
        return None

    await update.message.reply_text(
        give_random_answer(MOVIES.GET_ONE_FROM_A_LIST_OF_MOVIES)
    )


async def get_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /genre command."""
    if not update.message:
        return None

    await update.message.reply_text(get_list_of_genres())


async def get_director(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /director command."""
    if not update.message:
        return None

    await update.message.reply_text(get_list_of_directors())


async def get_film(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /film command."""
    if not update.message:
        return None

    await update.message.reply_text(find_random_film())


async def answer_to_specific_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles a message from a specific user."""
    if not update.message:
        return None

    if update.message.from_user.id == USER.GET_USER_ID:
        await update.message.reply_text(
            give_random_answer(ANSWERS.GET_ONE_FROM_A_LIST_OF_ANSWERS),
            do_quote=True,
            disable_notification=True,
        )


async def get_any(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles any other command."""
    await update.message.reply_text(
        "Используйте команду /film, чтобы получить случайный фильм из списка.\n" \
        "\n" \
        "Используйте команду /genre, чтобы получить список жанров, " \
        "и команду /director, чтобы получить список режиссеров " \
        "(в ответе будут представлены 10 случайных режисеров, " \
        "т.к. режисеров в базе данных очень много, при этом "
        "в Telegram имееются ограничения на количество символов в сообщении): " \
        "в дальнейшем будет добавлена возможность искать фильмы по жанрам и режиссерам."
    )


# Main function
def main():
    """The main function of the script."""
    app = ApplicationBuilder().token(BOT.GET_BOT_TOKEN).build()
    # for usage
    app.add_handler(CommandHandler("director", get_director))
    app.add_handler(CommandHandler("genre", get_genre))
    app.add_handler(CommandHandler("film", get_film))
    app.add_handler(CommandHandler("movie", get_movie))
    # for debugging
    app.add_handler(CommandHandler("d", get_director))
    app.add_handler(CommandHandler("g", get_genre))
    app.add_handler(CommandHandler("f", get_film))
    app.add_handler(CommandHandler("m", get_movie))
    # for message handling
    app.add_handler(MessageHandler(filters.COMMAND, get_any))
    app.add_handler(
        MessageHandler(
            (
                filters.Chat(chat_id=CHAT.GET_CHAT_ID) |
                filters.User(user_id=USER.GET_USER_ID)
            )
            & filters.TEXT,
            answer_to_specific_user,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
