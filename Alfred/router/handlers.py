from telegram.ext import filters, MessageHandler, CommandHandler, ContextTypes, CallbackQueryHandler
from loguru import logger


class AlfredHandlers:

    def __init__(self, application, router):
        self.__application = application
        self.__router = router
        self.START_HANDLER = CommandHandler('start', self.__router.start)
        self.MAIN_MENU = CallbackQueryHandler(self.__router.main_menu, pattern='main')
        self.ADD_API_HANDLER = CallbackQueryHandler(self.__router.add_api_key, pattern='m1')
        self.CHOOSE_REPLY_HANDLER = CallbackQueryHandler(self.__router.choose_reply_menu, pattern='m2')
        self.REPLY_MODE_VOICE_HANDLER = CallbackQueryHandler(self.__router.voice_reply_menu, pattern='reply1')
        self.REPLY_MODE_TEXT_HANDLER = CallbackQueryHandler(self.__router.text_reply_menu, pattern='reply2')
        self.REPLY_MODE_DEFAULT_HANDLER = CallbackQueryHandler(self.__router.default_reply_menu, pattern='reply3')
        self.TEXT_HANDLER = MessageHandler(filters.TEXT & (~filters.COMMAND), self.__router.text_request)
        self.UNKNOWN_HANDLER = MessageHandler(filters.COMMAND, self.__router.unknown)
        self.VOICE_HANDLER = MessageHandler(filters.VOICE, self.__router.voice_request)

    def add_handlers(self):
        logger.info(f'AlfredHandlers: Adding handlers to the bot')
        handlers = [(attr, value) for attr, value in self.__dict__.items() if attr.isupper()]
        for attr, value in handlers:
            try:
                logger.trace(f'AlfredHandlers: Adding a handler: {attr}')
                self.__application.add_handler(value)
            except TypeError as e:
                logger.debug(f'AlfredHandlers: could not add a handler: {attr} \
                error raised: {e}')
        logger.info(f'AlfredHandlers: Handlers have been added')
