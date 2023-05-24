from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from settings.settings import Settings
from router.handlers import AlfredHandlers
from router.router import Router
from utils.logger import setup_logger


settings = Settings()
setup_logger(settings)

application = ApplicationBuilder().token(settings.TG_TOKEN).build()
user_router = Router()
handlers = AlfredHandlers(application, user_router)
handlers.add_handlers()


def main():
    application.run_polling()


if __name__ == '__main__':
    main()
