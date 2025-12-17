from aiogram import Router, F
from aiogram.types import Message
from ..manager import UserManager

def get_tool_router(user_manager: UserManager) -> Router:
    """Создает роутер для обработки команд."""
    router = Router()
    @router.message(F.text.startswith('/'))
    async def unknown_command(message: Message):
        user_manager.add_user(message.chat.id)
        await message.answer("Я вас не понял. Пропишите /help для того чтобы ознакомиться с командами")
        
    return router