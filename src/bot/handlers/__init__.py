"""Всякие хэндлеры"""

__all__ = [
    "COMMANDS",
    "get_handlers"
]
from aiogram import Router

from .start import user_router as start_router
from .sendnew import sendnew_router as sendnew_router
from .toolrouter import get_tool_router as tool_router
from .getnew import getnew_router

from ...manager.bossmanager import BossManager
from ..manager import UserManager
COMMANDS = [
    "start",
    "help",
    "getsupport",
    "getnew"
]

def get_handlers(manager: BossManager, user_manager: UserManager) -> list[Router]:
    """Главная точка входа которая возращает все роутеры

    Args:
        manager (BossManager): Менеджер пауков.

    Returns:
        list[Router]: Роуты.
    """
    
    return [
        start_router(user_manager),
        getnew_router(manager, user_manager),
        sendnew_router(user_manager),
        tool_router(user_manager)
    ]