import random

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from data import Answers, Bot, Chat, Films, Movies, User

ANSWERS = Answers()
BOT = Bot()
CHAT = Chat()
FILMS = Films()
MOVIES = Movies()
USER = User()

def find_random_film(films: tuple[str]) -> str:

    """The function accepts a list with a list of films and returns a random film."""

    return random.choice(films)

def give_random_answer(answers: tuple[str]) -> str:

    """The function accepts a list with a list of answers and returns a random answer."""

    return random.choice(answers)

async def get_movie(update:Update, context:ContextTypes.DEFAULT_TYPE):

    """The function returns a film from the current list (for internal use only)."""

    if not update.message:
        return None

    await update.message.reply_text(find_random_film(MOVIES.GET_ONE_FROM_A_LIST_OF_MOVIES))

async def get_film(update:Update, context:ContextTypes.DEFAULT_TYPE):

    """The function returns a film from the main list of films."""

    if not update.message:
        return None

    await update.message.reply_text(find_random_film(FILMS.GET_ONE_FROM_A_LIST_OF_FILMS))

async def answer_to_specific_user(update:Update, context:ContextTypes.DEFAULT_TYPE):

    """The function handles a user's message only from a specific user."""

    if not update.message:
        return None

    if update.message.from_user.id == USER.GET_USER_ID:
        await update.message.reply_text(give_random_answer(ANSWERS.GET_ONE_FROM_A_LIST_OF_ANSWERS), do_quote=True, disable_notification=True)

async def get_any(update:Update, context:ContextTypes.DEFAULT_TYPE):

    """The function handles any other command sent, i.e. a command which is not registered as a handler."""

    await update.message.reply_text("Используйте команду /film, чтобы получить случайный фильм из списка.")

def main():

    app = ApplicationBuilder().token(BOT.GET_BOT_TOKEN).build()

    app.add_handler(CommandHandler('movie', get_movie))
    app.add_handler(CommandHandler('film', get_film))
    app.add_handler(MessageHandler((filters.Chat(chat_id=CHAT.GET_CHAT_ID) | filters.User(user_id=USER.GET_USER_ID)) & filters.TEXT, answer_to_specific_user))
    app.add_handler(MessageHandler(filters.COMMAND, get_any))

    app.run_polling()

if __name__ == '__main__':
    main()
