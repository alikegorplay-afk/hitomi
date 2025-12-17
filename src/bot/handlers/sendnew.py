import json
import aiofiles

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from loguru import logger

from ...core.config import config
from ..manager import UserManager

def sendnew_router(user_manager: UserManager) -> Router:
    router = Router()

    @router.message(Command("sendnew"))
    async def sendnew_handler(msg: Message):
        """
        Обработчик команды /sendnew <url> — добавляет URL в список на рассмотрение.
        Если URL уже есть — уведомляет об этом.
        """
        user_manager.add_user(msg.chat.id)
        try:
            command, url = msg.text.strip().split(maxsplit=1)
        except ValueError:
            await msg.answer(
                "Пожалуйста, укажите команду в формате:\n<code>/sendnew https://example.com</code>",
                parse_mode="HTML"
            )
            return
        logger.info(f"Получен запрос на добавление нового домена (url={url})")
        
        try:
            async with aiofiles.open(config.save_path, 'r', encoding='utf-8') as f:
                urls = json.loads(await f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            urls = []

        if url in urls:
            await msg.answer("Этот URL уже добавлен на рассмотрение!")
            return

        urls.append(url)
        async with aiofiles.open(config.save_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(urls, ensure_ascii=False, indent=2))

        await msg.answer("✅ URL успешно добавлен на рассмотрение!")

    return router