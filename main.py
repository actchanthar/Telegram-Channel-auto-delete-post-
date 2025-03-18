import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

# Get the bot token from Heroku config vars
TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID") #Get channel ID from Heroku config vars

if not TOKEN:
    print("Error: TOKEN environment variable not set.")
    exit(1)

if not CHANNEL_ID:
    print("Error: CHANNEL_ID environment variable not set.")
    exit(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def delete_last_message(update, context):
    try:
        messages = context.bot.get_chat_history(chat_id=CHANNEL_ID, limit=2)
        if len(messages) > 1:
            message_to_delete = messages[1]
            context.bot.delete_message(chat_id=CHANNEL_ID, message_id=message_to_delete.message_id)
            update.message.reply_text("Last message deleted.")
        else:
            update.message.reply_text("No messages to delete.")
    except telegram.error.BadRequest as e:
        update.message.reply_text(f"Error: {e}")
    except Exception as e:
        update.message.reply_text(f"An unexpected error occurred: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("delete", delete_last_message))

    updater.start_polling() #using polling, webhooks are better for production.
    updater.idle()

if __name__ == '__main__':
    main()
