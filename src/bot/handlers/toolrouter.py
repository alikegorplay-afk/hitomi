from aiogram import Router, F
from aiogram.types import Message

router = Router()
@router.message(F.text.startswith('/'))
async def unknown_command(message: Message):
    await message.answer("Я вас не понял. Пропишите /help для того чтобы ознакомиться с командами")