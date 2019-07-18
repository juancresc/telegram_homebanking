import sqlite3
import logging
from hb import HB
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Help!')


def echo(bot, update):
	"""Echo the user message."""
	bot.send_message(chat_id=update.message.chat_id, text="Loading...")
	old_msg = update.message.text
	hb = HB()
	with open("data.json", 'r') as f:
		data = json.load(f)
	for account in data['accounts']:
		username = account['username']
		password = account['password']
		saldo = hb.get_saldo(username, password)
		msg = "username %s: %s \n " % (username, saldo)
		bot.send_message(chat_id=update.message.chat_id, text=msg)
	print(update.message.chat_id, msg)
	


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)




def main():
	sqlite_file = 'db.sqlite'
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()
	SQL = """CREATE TABLE IF NOT EXISTS
			accounts 
			(id INTEGER PRIMARY KEY,
			chat_id TEXT,
			username TEXT,
			password TEXT,
			balance TEXT, 
			status INTEGER)"""
	c.execute(SQL)
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater("740902647:AAF47k_QYeEcTIb2bqIJTs4PuP3pDpG7VNU")

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))

	# on noncommand i.e message - echo the message on Telegram
	dp.add_handler(MessageHandler(Filters.text, echo))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
    main()
