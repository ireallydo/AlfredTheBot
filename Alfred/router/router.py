from telegram import Update
from telegram.ext import ContextTypes
from services import alfred_brain
from services import alfred_voice
from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Router:

    def __init__(self):
        self.__API_mode = False
        self.__API_token = False
        self.__reply_mode = False

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info('Router: start request')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=await self.main_menu_message(),
                                       reply_markup=await self.main_menu_keyboard())

    async def main_menu(self, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.callback_query.message.edit_text(await self.main_menu_message(),
                                                           reply_markup=await self.main_menu_keyboard())

    async def main_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('OpenAI API key', callback_data='m1')],
                    [InlineKeyboardButton('Reply mode', callback_data='m2')]
                    ]
        return InlineKeyboardMarkup(keyboard)

    async def main_menu_message(self):
        return "Hello there, beautiful creature!\nWhat a lovely day!\nWhat are we up to?"

    async def add_api_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query

        if query.data == 'm1':
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Please type in your OpenAI API token')
            self.__API_mode = True
            logger.trace(f'API MODE IS SET TO: {self.__API_mode}')

    async def choose_reply_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query

        if query.data == 'm2':
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=await self.reply_menu_message(),
                                           reply_markup=await self.reply_menu_keyboard())

    async def reply_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('Voice', callback_data='reply1')],
                    [InlineKeyboardButton('Text', callback_data='reply2')],
                    [InlineKeyboardButton('Default', callback_data='reply3')]
                    ]
        return InlineKeyboardMarkup(keyboard)

    async def reply_menu_message(self):
        return "Please choose the reply mode for Alfred.\n\
By default Alfred answers the same way he got request.\n\
I.e. voice answers to voice requests and text answers to text requests."

    async def voice_reply_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query

        if query.data == 'reply1':
            self.__reply_mode = 1
            logger.info('Reply mode is set to: voice')
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Alfred will answer your questions with voice messages!')

    async def text_reply_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query

        if query.data == 'reply2':
            self.__reply_mode = 2
            logger.info('Reply mode is set to: text')
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Alfred will answer your questions with text messages!')

    async def default_reply_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query

        if query.data == 'reply3':
            self.__reply_mode = False
            logger.info('Reply mode is set to: text')
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Alfred will answer in voice to voice messages \
                                                and in text to text messages!')

    async def voice_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info('Router: voice request')
        txt = await alfred_voice.transcribe_voice(update, context)
        if not txt:
            response = 'Excuse me, could you repeat your request more clearly please?'
        elif txt == 'start':
            await self.start(update, context)
            return
        elif self.__API_token:
            response = await alfred_brain.think_about_it(txt, self.__API_token)
        else:
            response = 'Sorry, you should provide an OpenAI API token for Alfred to answer you. \
            Please use the /start command to see the menu'
        if self.__reply_mode != 2:
            await self.voice_answer(response, update, context)
        else:
            await self.text_answer(response, update, context)

    async def text_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info('Router: text request')
        request = update.message.text
        if self.__API_mode:
            self.__API_token = request
            self.__API_mode = False
            logger.debug(f'Router: new OpenAI token provided for chat \
                        {update.effective_chat.id} is: {self.__API_token}')
            response = 'Your token has been successfully changed'
        elif not self.__API_token:
            response = 'Sorry, you should provide an OpenAI API token for Alfred to answer you. \
            Please use the /start command to see the menu'
        else:
            response = await alfred_brain.think_about_it(request, self.__API_token)
        if self.__reply_mode != 1:
            await self.text_answer(response, update, context)
        else:
            await self.voice_answer(response, update, context)

    async def voice_answer(self, response: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        voice_message = await alfred_voice.convert_text_to_voice(response)
        await alfred_voice.reply_with_voice(voice_message, update, context)

    async def text_answer(self, response: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=response)

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info('Router: unknown request')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Sorry, sir, I do not quite understand you.\n\
    I would suggest to ask that nice dev lady for help \
    with our little misunderstanding.")
