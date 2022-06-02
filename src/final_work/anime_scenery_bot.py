from typing import IO
from io import BytesIO
from PIL import Image
from tempfile import TemporaryFile
from telegram import Update
from telegram.ext import (
    Updater,
    Dispatcher,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)
from src.final_work.image_converter import ImageConverter, ModelType


class AnimeSceneryBot:
    def __init__(self):
        self.updater = Updater(token="TOKEN")
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler("start", self._start, run_async=True))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self._image_loaded, run_async=True))
        self.updater.start_polling()

    @staticmethod
    def _image_loaded(update: Update, context: CallbackContext):
        image_file_id = update.message.photo[-1]

        with TemporaryFile() as temp_file:
            context.bot.get_file(image_file_id).download(out=temp_file)
            converted_image = AnimeSceneryBot._convert_image(temp_file)
            converted_image_name = f"converted_{temp_file.name}"

        AnimeSceneryBot._send_image(update, converted_image, converted_image_name)

    @staticmethod
    def _convert_image(image_file: IO) -> Image:
        converter = ImageConverter()
        image = Image.open(image_file)
        converted_image = converter.convert_image(image, ModelType.HOSODA)

        return converted_image

    @staticmethod
    def _start(update: Update, context: CallbackContext):
        user_first_name = update.effective_user.first_name
        update.message.reply_text(
            f"Hi! {user_first_name}\nI can turn an ordinary scenery into an anime sketch!", quote=True
        )

    @staticmethod
    def _send_image(update: Update, image: Image, image_name: str):
        bytesIO = BytesIO()
        bytesIO.name = image_name
        image.save(bytesIO, "JPEG")
        bytesIO.seek(0)
        update.message.reply_photo(bytesIO)


bot = AnimeSceneryBot()
