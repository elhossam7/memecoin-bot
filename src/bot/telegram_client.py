from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

class TelegramClient:
    def __init__(self, token: str):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text("Welcome to the MemeCoin Trading Bot!")

    def run(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.updater.start_polling()
        self.updater.idle()