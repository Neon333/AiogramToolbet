from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from menu import MenuType


def render_menu(menu_cls: MenuType, integrate: bool = False):
    async def _wrapper(initiator_message: Message, state: FSMContext):
        return await menu_cls.render(initiator_message, state) if not integrate else await menu_cls.render_in(
            initiator_message, state
        )

    return _wrapper
