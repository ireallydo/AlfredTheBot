# maybe change for a better voice - https://www.geeksforgeeks.org/text-to-speech-changing-voice-in-python/
import speech_recognition as speech_rec
from typing import BinaryIO, TextIO, NoReturn
import os
from gtts import gTTS
from telegram import Update
from telegram.ext import ContextTypes
from settings.settings import Settings
from utils.paths import clear_paths
from loguru import logger


settings = Settings()


class AlfredVoice:

    @staticmethod
    async def convert_text_to_voice(text_message: TextIO) -> str:
        """converts text file into voice file and returns file path to voice file (static, from settings)"""
        logger.info('AlfredVoice: convert text to voice')
        logger.trace(f'AlfredVoice: convert following text: {text_message}')
        language = 'en'
        try:
            voice_message = gTTS(text=text_message, lang=language, slow=False)
            clear_paths(settings.VOICE_RESP_mp3, settings.VOICE_RESP_ogg)
            voice_message.save(settings.VOICE_RESP_mp3)
            os.system(f'ffmpeg -i {settings.VOICE_RESP_mp3} {settings.VOICE_RESP_ogg}')
        except Exception as ex:
            logger.debug(f'AlfredVoice: Did not manage to convert text into voice,\
                        exception raised: {ex}')
        return settings.VOICE_RESP_ogg

    @staticmethod
    async def reply_with_voice(voice_message: BinaryIO,
                               update: Update,
                               context: ContextTypes.DEFAULT_TYPE) -> NoReturn:
        """send voice message to the chatbot"""
        logger.info('AlfredVoice: reply with voice')
        await context.bot.send_voice(chat_id=update.effective_chat.id,
                                     voice=voice_message)

    @staticmethod
    async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """transcribes voice message into text"""
        logger.info(f'AlfredVoice: transcribe_voice. Message duration: {update.message.voice.duration}')
        try:
            logger.info('AlfredVoice: fetch voice message')
            voice = await context.bot.getFile(update.message.voice.file_id)
        except Exception as ex:
            logger.debug(f'AlfredVoice: did not manage to fetch the voice: \n\
            raised exception: {ex}')
            txt_msg = False
        # renewable media file path is used, so delete the previously saved version
        clear_paths(settings.VOICE_REQ_ogg, settings.VOICE_REQ_wav)
        try:
            logger.info('AlfredVoice: save voice message to drive')
            await voice.download_to_drive(settings.VOICE_REQ_ogg)
        except Exception as ex:
            logger.debug(f'AlfredVoice: did not manage to save voice message to drive: \n\
                        raised error: {ex}')
            txt_msg = False
        try:
            logger.info('AlfredVoice: transcode ogg to wav')
            os.system(f'ffmpeg -i {settings.VOICE_REQ_ogg} {settings.VOICE_REQ_wav}')
        except Exception as ex:
            logger.debug(f'AlfredVoice: did not manage to transcode ogg to wav: \n\
            raised exception: {ex}')
            txt_msg = False
        try:
            logger.info('AlfredVoice: recognize speech from the voice message')
            recog_voice = speech_rec.Recognizer()
            with speech_rec.WavFile(settings.VOICE_REQ_wav) as voice_req_msg:
                speech = recog_voice.record(voice_req_msg)
            # renewable media file path is used, so delete the file after usage
            clear_paths(settings.VOICE_REQ_ogg, settings.VOICE_REQ_wav)
        except Exception as ex:
            logger.debug(f'AlfredVoice: did not manage to transcode ogg to wav, raised exception: {ex}')
            txt_msg = False
        try:
            logger.info('AlfredVoice: convert voice message into text')
            txt_msg = recog_voice.recognize_google(speech)
            logger.trace(f'AlfredVoice: converted message: {txt_msg}')
        except speech_rec.UnknownValueError as e:
            logger.debug(f'AlfredVoice: did not manage to convert speech to text, raised error: {e}')
            txt_msg = False
        except speech_rec.RequestError as e:
            logger.debug(f'AlfredVoice: did not manage to request results from Speech to Text service, \
            raised error: {e}')
            txt_msg = False
        finally:
            return txt_msg


alfred_voice = AlfredVoice()
