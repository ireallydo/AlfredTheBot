# maybe change for a better voice - https://www.geeksforgeeks.org/text-to-speech-changing-voice-in-python/
import speech_recognition as speech_rec
from typing import BinaryIO, TextIO, NoReturn
import os
from gtts import gTTS
from telegram import Update
from telegram.ext import ContextTypes
from consts import VOICE_RESP_mp3, VOICE_RESP_ogg, VOICE_REQ_wav, VOICE_REQ_ogg


class AlfredVoice:

    @staticmethod
    async def convert_text_to_voice(text_message: TextIO) -> str:
        """converts text file into voice file and returns file path to voice file"""
        language = 'en'
        voice_message = gTTS(text=text_message, lang=language, slow=False)
        if os.path.isfile(VOICE_RESP_mp3):
            os.remove(VOICE_RESP_mp3)
        if os.path.isfile(VOICE_RESP_ogg):
            os.remove(VOICE_RESP_ogg)
        voice_message.save(VOICE_RESP_mp3)
        os.system(f'ffmpeg -i {VOICE_RESP_mp3} {VOICE_RESP_ogg}')
        return VOICE_RESP_ogg

    @staticmethod
    async def reply_with_voice(voice_message: BinaryIO,
                               update: Update,
                               context: ContextTypes.DEFAULT_TYPE) -> NoReturn:
        """send voice message to the chatbot"""
        await context.bot.send_voice(chat_id=update.effective_chat.id,
                                     voice=voice_message)

    @staticmethod
    async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """transcribes voice message into text"""
        logger.info(f'transcribe_voice. Message duration: {update.message.voice.duration}')
        # fetch voice message
        voice = await context.bot.getFile(update.message.voice.file_id)
        # renewable media file path is used, so delete the previously saved version
        if os.path.isfile(VOICE_REQ_ogg):
            os.remove(VOICE_REQ_ogg)
        if os.path.isfile(VOICE_REQ_wav):
            os.remove(VOICE_REQ_wav)
        await voice.download_to_drive(VOICE_REQ_ogg)
        # transcode ogg to wav
        os.system(f'ffmpeg -i {VOICE_REQ_ogg} {VOICE_REQ_wav}')
        # get the speech from the voice message
        recog_voice = speech_rec.Recognizer()
        with speech_rec.WavFile(VOICE_REQ_wav) as voice_req_msg:
            speech = recog_voice.record(voice_req_msg)
        # speech to text
        try:
            txt_msg = recog_voice.recognize_google(speech)
            # logger.info(txt)
        except speech_rec.UnknownValueError:
            print('Speech to Text could not understand audio')
            # logger.warn('Speech to Text could not understand audio')
        except speech_rec.RequestError as e:
            print(f'Could not request results from Speech to Text service; {e}')
            # logger.warn('Could not request results from Speech to Text service; {0}'.format(e))

        return txt_msg


alfred_voice = AlfredVoice()
