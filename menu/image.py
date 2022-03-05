from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile

from .base import Menu


class MediaMenu(Menu):

    photo_path: Union[str, None] = None

    @classmethod
    def _get_handler_mapping(cls, target: Union[Message, CallbackQuery]) -> dict:
        handlers = super()._get_handler_mapping(target)
        handlers[False].update({Message: target.answer_photo, CallbackQuery: target.message.answer_photo})
        handlers[True].update({Message: target.edit_media, CallbackQuery: target.message.edit_media})

        return handlers

    @classmethod
    async def render(cls, initiator: Union[Message, CallbackQuery], state: FSMContext, **kwargs):
        handler = cls._get_answer_handler(target=initiator)

        if cls.photo_path is None:
            raise AttributeError("Empty photo input file")

        return await handler(
            photo=InputFile(cls.photo_path),
            caption=await cls._get_text(),
            reply_markup=await cls._get_keyboard(),
            parse_mode=cls.parse_mode
        )

    @classmethod
    async def render_in(cls, target_message: Union[Message, CallbackQuery], state: FSMContext, **kwargs):
        handler = cls._get_answer_handler(target=target_message, render_in=True)
        return await handler(
            caption=await cls._get_text(),
            reply_markup=await cls._get_keyboard(),
            parse_mode=cls.parse_mode
        )
