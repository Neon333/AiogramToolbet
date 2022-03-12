from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from . import MenuType


def render_menu(menu_cls: MenuType, integrate: bool = False):
    async def _wrapper(initiator_message: Message, state: FSMContext, **kwargs):
        return await menu_cls.render(initiator_message, state, **kwargs) if not integrate else await menu_cls.render_in(
            initiator_message, state, **kwargs
        )

    return _wrapper
