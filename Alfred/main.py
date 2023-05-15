import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from settings import TG_TOKEN
from Alfred.alfred_brain import alfred_brain
from Alfred.alfred_voice import alfred_voice


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# TODO media files names to constants
# TODO menu
# TODO several modes: answer in writing and answer in text, set the mode from the menu
# TODO maybe better voice
# TODO have some fun
# TODO bot settings, like audio or text quotes in reply to emojis
# TODO find out how to deal with different chat channels and saving different tokens maybe? ... or not lol

# maybe change for a better voice - https://www.geeksforgeeks.org/text-to-speech-changing-voice-in-python/


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hello there, beautiful creature!\nWhat a lovely day!\nWhat are we up to?")

# async def parrot(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id,
#                                    text=update.message.text)


async def voice_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = await alfred_voice.transcribe_voice(update, context)
    response = await alfred_brain.think_about_it(txt)
    voice_message = await alfred_voice.convert_text_to_voice(response)
    # await context.bot.send_message(chat_id=update.effective_chat.id,
    #                                text=response)
    await alfred_voice.reply_with_voice(voice_message, update, context)


async def text_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.message.text
    print(request)
    print(type(request))
    response = await alfred_brain.think_about_it(request)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, sir, I do not quite understand you.\n\
I would suggest to ask that nice dev lady for help \
with our little misunderstanding.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TG_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), text_answer)
    application.add_handler(text_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    voice_handler = MessageHandler(filters.VOICE, voice_answer)
    application.add_handler(voice_handler)

    application.run_polling()
