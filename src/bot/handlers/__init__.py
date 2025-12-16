"""Всякие хэндлеры"""

__all__ = [
    "COMMANDS",
    "get_handlers"
]

import aiohttp
from aiogram import Router

from .start import router as start_router
from .sendnew import router as sendnew_router
from .toolrouter import router as tool_router
from .getnew import getnew_router

from ...manager.bossmanager import BossManager

COMMANDS = [
    "start",
    "help",
    "getsupport",
    "getnew"
]

def get_handlers(session: aiohttp.ClientSession) -> list[Router]:
    manager = BossManager(session)
    get_new_router = getnew_router(manager)
    
    return [
        start_router,
        get_new_router,
        sendnew_router,
        tool_router
    ]