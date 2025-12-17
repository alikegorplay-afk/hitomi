from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..manager import UserManager
from .._texts import (
    HELLOTEXT,
    HELPTEXT,
    GETSUPPORTTEXT
)

def user_router(user_manager: UserManager) -> Router:
    router = Router()

    @router.message(Command("start"))
    async def start_handler(message: Message) -> None:
        """Обработчик команды /start"""
        user_manager.add_user(message.chat.id)
        await message.answer(HELLOTEXT, parse_mode="HTML")

    @router.message(Command("help"))
    async def help_handler(message: Message) -> None:
        """Обработчик команды /help"""
        user_manager.add_user(message.chat.id)
        await message.answer(HELPTEXT, parse_mode="HTML")
        
    @router.message(Command("getsupport"))
    async def getsupport_handler(message: Message) -> None:
        """Обработчик команды /getsupport"""
        user_manager.add_user(message.chat.id)
        await message.answer(GETSUPPORTTEXT, parse_mode="HTML")
        
    return router