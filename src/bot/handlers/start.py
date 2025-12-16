from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from .._texts import (
    HELLOTEXT,
    HELPTEXT,
    GETSUPPORTTEXT
)

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    await message.answer(HELLOTEXT, parse_mode="HTML")

@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Обработчик команды /help"""
    await message.answer(HELPTEXT, parse_mode="HTML")
    
@router.message(Command("getsupport"))
async def getsupport_handler(message: Message) -> None:
    """Обработчик команды /getsupport"""
    await message.answer(GETSUPPORTTEXT, parse_mode="HTML")