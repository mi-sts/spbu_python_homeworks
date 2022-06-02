from typing import IO
from io import BytesIO
from PIL import Image
from tempfile import TemporaryFile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)
from src.final_work.image_converter import ImageConverter, ModelType


class AnimeSceneryBot:
    MAX_IMAGE_SIZE = 1280

    def __init__(self):
        self.selected_model = ModelType.HOSODA
        self.updater = Updater(token="TOKEN")
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler("start", self._start, run_async=True))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self._image_loaded, run_async=True))
        self.dispatcher.add_handler(CallbackQueryHandler(self._button_pressed))
        self.updater.start_polling()
        self.updater.idle()

    def _image_loaded(self, update: Update, context: CallbackContext):
        image_file = update.message.photo[-1]
        update.message.reply_text(image_file.width)
        if image_file.width >= AnimeSceneryBot.MAX_IMAGE_SIZE or image_file.height >= AnimeSceneryBot.MAX_IMAGE_SIZE:
            self._large_image_loaded(update)
            return

        with TemporaryFile() as temp_file:
            context.bot.get_file(image_file).download(out=temp_file)
            converted_image = self._convert_image(temp_file)
            converted_image_name = f"converted_{temp_file.name}"

        self._send_image(update, converted_image, converted_image_name)

    def _large_image_loaded(self, update: Update):
        update.message.reply_text("Loading image should not be larger than 1280px in width or height!")
        self._show_model_selection_keyboard(update)

    def _convert_image(self, image_file: IO) -> Image:
        converter = ImageConverter()
        image = Image.open(image_file)
        converted_image = converter.convert_image(image, self.selected_model)

        return converted_image

    def _show_model_selection_keyboard(self, update: Update):
        model_selection_keyboard = [
            [
                InlineKeyboardButton("Hosoda Mamoru", callback_data=ModelType.HOSODA.value),
                InlineKeyboardButton("Kon Satoshi", callback_data=ModelType.KON.value),
            ],
            [
                InlineKeyboardButton("Miyazaki Hayao", callback_data=ModelType.MIYAZAKI.value),
                InlineKeyboardButton("Shinkai Makoto", callback_data=ModelType.SHINKAI.value),
            ],
        ]
        model_selection_markup = InlineKeyboardMarkup(model_selection_keyboard)
        update.message.reply_text(
            "Choose the style of one of the anime producers:", reply_markup=model_selection_markup
        )

    def _start(self, update: Update, context: CallbackContext):
        user_first_name = update.effective_user.first_name
        update.message.reply_text(
            f"Hi, {user_first_name}!\nI can turn an ordinary scenery into an anime sketch!", quote=True
        )
        self._show_model_selection_keyboard(update)

    def _send_image(self, update: Update, image: Image, image_name: str):
        bytes_io = BytesIO()
        bytes_io.name = image_name
        image.save(bytes_io, "JPEG")
        bytes_io.seek(0)
        update.message.reply_photo(bytes_io)
        self._show_model_selection_keyboard(update)

    def _button_pressed(self, update: Update, context: CallbackContext):
        callback_data = update.callback_query.data
        callback_query = update.callback_query
        callback_query.answer()
        self.selected_model = ModelType(callback_data)
        callback_query.edit_message_text(text="Send a message with a photo to convert:")


if __name__ == "__main__":
    anime_scenery_bot = AnimeSceneryBot()
