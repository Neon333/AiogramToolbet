from typing import Union, Optional

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup

from ..exceptions.helper import raise_exc


class Menu:

    """
    Base class for building custom menus.
    Inherit from this class to create your menu.

    Attributes:
        parse_mode - one of available parse modes from telegram bot api that will be applied to message
        static_text - message text
        static_keyboard - inline or reply aiogram keyboard object that will be attached to message
    """

    parse_mode: str = 'HTML'

    static_text: Union[str, None] = None
    static_keyboard: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, None] = None

    callback_key: Optional[str] = None

    @classmethod
    def _get_answer_handler(cls, target: Union[Message, CallbackQuery], render_in: bool = False) -> callable:
        handler_map = cls._get_handler_mapping(target)
        return handler_map[render_in]

    @classmethod
    def _get_handler_mapping(cls, target: Union[Message, CallbackQuery]) -> dict:
        return {
            False: target.answer if isinstance(target, Message) else target.message.answer,
            True: target.edit_text if isinstance(target, Message) else target.message.edit_text
        }

    @classmethod
    async def _get_keyboard(cls) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, None]:
        """
        Method returns current keyboard instance that will be attached to message.
        You can override this method to provide dynamic keyboard generation.

        Examples:

        .. code-block:: python3

            async def _get_keyboard(cls):
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                        InlineKeyboardButton(f'generated_btn_{i}', callback_data=f'cb_{i}') for i in range(5)
                    ]
                )


        :return: ReplyKeyboardMarkup, InlineKeyboardMarkup, None
        """
        return cls.static_keyboard if cls.static_keyboard is not None else raise_exc(NotImplementedError)

    @classmethod
    async def _get_text(cls) -> str:
        return cls.static_text if cls.static_text is not None else raise_exc(NotImplementedError)

    @classmethod
    async def render(cls, initiator: Union[Message, CallbackQuery], state: FSMContext, **kwargs):
        """
        Send message built from current class fields
        :param initiator: Message or CallbackQuery object
        :param state: FSMContext object
        :param kwargs:
        :return:
        """

        handler = cls._get_answer_handler(target=initiator)
        return await handler(
            text=await cls._get_text(),
            reply_markup=await cls._get_keyboard(),
            parse_mode=cls.parse_mode
        )

    @classmethod
    async def render_in(cls, target_message: Union[Message, CallbackQuery], state: FSMContext, **kwargs):
        """
        Same as render method, but allows you to display menu in existing message
        :param target_message: Message or CallbackQuery object
        :param state: FSMContext object
        :param kwargs:
        :return:
        """

        handler = cls._get_answer_handler(target=target_message)
        return await handler(
            text=await cls._get_text(),
            reply_markup=await cls._get_keyboard(),
            parse_mode=cls.parse_mode
        )

    @classmethod
    def register_handlers(cls, dp: Dispatcher):
        """
        Abstract method for aiogram handlers registration.
        It is strongly recommended use it to separate logic in your app
        :param dp:
        :return:
        """
        pass
