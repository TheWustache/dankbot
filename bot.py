from telegram.ext import Updater, CommandHandler
from telegram import Bot
import praw
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import logging
import subprocess

# set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def weekday_string():
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][datetime.today().weekday()]


def id_in_db(db, chat_id):
    c = db.cursor()
    c.execute("""SELECT count(1)
        FROM entry
        WHERE chat_id=?""",
              (chat_id,))
    return c.fetchone()[0] != 0


reddit = praw.Reddit(client_id='-q3d0f7M-QYVeA',
                     client_secret='xHBpdGsDOTTomRnUXeuEc3S2sHA',
                     user_agent='dank tele bot')

subreddit = reddit.subreddit('dankmemes')

# set up bot
token = '539321432:AAGzDOXVL_dYCA1CGg0mZolzMZEVN_QyjKc'
updater = Updater(token=token)
dispatcher = updater.dispatcher


def start_(bot, update):
    # url = next((submission.url for submission in subreddit.hot(limit=10) if submission.url.endswith('.jpg')), None)
    # text = "It is {} my dudes[.]({})".format(weekday_string(), url)
    # bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode="Markdown")
    print("start_")


def meme_(bot, update):
    db = sqlite3.connect('database.sqlite')
    chat_id = update.message.chat_id
    if not id_in_db(db, chat_id):
        db.execute("""INSERT INTO entry
            VALUES (?)""",
                   (chat_id,))
        db.commit()
        bot.send_message(chat_id=update.message.chat_id, text="➕")


def unmeme_(bot, update):
    db = sqlite3.connect('database.sqlite')
    chat_id = update.message.chat_id
    if id_in_db(db, chat_id):
        db.execute("""DELETE FROM entry
            WHERE chat_id=?""",
                   (update.message.chat_id,))
        db.commit()
        bot.send_message(chat_id=update.message.chat_id, text="➖")


def ping_(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="pong")


def voice_(bot, update, args):
    subprocess.run(['python3', 'texttovoice.py', 'temp', ' '.join(args)])
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('temp.ogg', 'rb'))


#  register handlers
# dispatcher.add_handler(CommandHandler('start', start_))
dispatcher.add_handler(CommandHandler('meme', meme_))
dispatcher.add_handler(CommandHandler('unmeme', unmeme_))
dispatcher.add_handler(CommandHandler('ping', ping_))
dispatcher.add_handler(CommandHandler('voice', voice_, pass_args=True))

# set up scheduler
scheduler = BackgroundScheduler()


def post_():
    db = sqlite3.connect('database.sqlite')
    c = db.cursor()
    c.execute("""SELECT chat_id
        FROM entry""")
    for result in c.fetchall():
        url = next((submission.url for submission in subreddit.hot(limit=10) if (submission.url.endswith(
            '.jpg') or submission.url.endswith('.png') and not submission.stickied)), None)
        text = "It is {} my dudes[.]({})".format(weekday_string(), url)
        bot = Bot(token=token)
        bot.send_message(chat_id=result[0], text=text, parse_mode="Markdown")


scheduler.add_job(post_, 'cron', hour=16, minute=20)
scheduler.start()

# start polling
print("Starting polling...")
updater.start_polling()
updater.idle()
