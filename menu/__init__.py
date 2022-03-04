from typing import TypeVar, Type, Union
from .base import Menu

MenuBase = TypeVar('MenuBase', bound=Menu)
MenuType = Union[Type[Menu], MenuBase]
