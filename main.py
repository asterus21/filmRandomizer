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


def find_random_film() -> str:
    """The function establishes the database connection to get a random film."""
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

    # try:
    #     with sqlite3.connect("films.db") as connection:
    #         cursor = connection.cursor()
    #         cursor.execute("SELECT film FROM films ORDER BY RANDOM() LIMIT 1")
    #         result = cursor.fetchone()
    #         return result[0] if result else None
    # except sqlite3.Error as e:
    #     logger.error("Database error: %s", e)
    #     return None
    # except NotImplementedError as e:
    #     logger.error("Unexpected error: %s", e)
    #     return None


def give_random_answer(answers: tuple[str]) -> str:
    """The function accepts a list of answers and returns a random answer."""
    return random.choice(answers)


def get_list_of_genres() -> str:
    """The function returns a list of genres."""
    try:
        with pymysql.connect(
            user=DATABASE.database["user"],
            password=DATABASE.database["password"],
            host=DATABASE.database["host"],
            database=DATABASE.database["database"],
            port=DATABASE.database["port"]
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT genre FROM mysql.`films` ORDER BY RAND() LIMIT 1;")
            # result = cursor.fetchone()
            # return result[0] if result else None

    except pymysql.Error as e:
        logger.error("Database error: %s", e)
    return None


def get_list_of_directors() -> str:
    """The function returns a list of directors."""
    try:
        with pymysql.connect(
            user=DATABASE.database["user"],
            password=DATABASE.database["password"],
            host=DATABASE.database["host"],
            database=DATABASE.database["database"],
            port=DATABASE.database["port"]
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT director FROM mysql.`films`;")
            # result = cursor.fetchall()
            # return result[0] if result else None
    except pymysql.Error as e:
        logger.error("Database error: %s", e)
    return None


async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """The function returns a film from the movies list (for internal use only)."""
    if not update.message:
        return None

    await update.message.reply_text(
        give_random_answer(MOVIES.GET_ONE_FROM_A_LIST_OF_MOVIES)
    )


async def get_film(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """The function returns a film from the films list."""
    if not update.message:
        return None

    await update.message.reply_text(find_random_film())


async def answer_to_specific_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """The function handles a user's message only from a specific user."""
    if not update.message:
        return None

    if update.message.from_user.id == USER.GET_USER_ID:
        await update.message.reply_text(
            give_random_answer(ANSWERS.GET_ONE_FROM_A_LIST_OF_ANSWERS),
            do_quote=True,
            disable_notification=True,
        )


async def get_any(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """The function handles any other command sent, 
    i.e. a command which is not registered as a handler."""
    await update.message.reply_text(
        "Используйте команду /film, чтобы получить случайный фильм из списка. " \
        "Используйте команду /genre, чтобы получить список жанров, " \
        "и команду /director, чтобы получить список режиссеров: " \
        "в дальнейшем будет добавлена возможность искать фильмы по жанрам и режиссерам."
    )


def main():
    """The main function of the script."""
    app = ApplicationBuilder().token(BOT.GET_BOT_TOKEN).build()
    app.add_handler(CommandHandler("movie", get_movie))
    app.add_handler(CommandHandler("film", get_film))
    app.add_handler(CommandHandler("genre", get_list_of_genres))
    app.add_handler(CommandHandler("director", get_list_of_directors))
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
