from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from loguru import logger

from ...manager.bossmanager import BossManager
from ...manganotif.core.models import MiniManga

def create_content(domain: str, mangas: list[MiniManga]) -> str:
    """Создаёт и возращает готовый текст

    Args:
        domain (str): Домен сайта
        mangas (list[MiniManga]): Название манги

    Returns:
        str: Готовый текст для отправки в чат Telegram.
    """
    return (
        f"🔥 <b>Найдены новые манги!</b>\n"
        f"🌐 Домен: <a href='{domain}'>{domain}</a>\n"
        f"📌 Количество: <b>{len(mangas)} шт.</b>\n\n"
        f"<b>Первые {len(mangas[:3])} манг:</b>"
        f"\n{''.join([f'• <a href=\"{manga.url}\">{manga.id} - {manga.title[:30]}</a>\n' for manga in mangas[:3]])}"
    )

def getnew_router(manager: BossManager):
    """
    Создаёт и возвращает Router с обработчиком команды /getnew.
    """
    router = Router()

    @router.message(Command("getnew"))
    async def getnew_handler(msg: Message):
        logger.info(f"Запрос на ручную проверку (chat_id={msg.chat.id})")
        data = await manager.find_new()
        if not all([True if x else False for x in data.values()]):
            await msg.answer("На данный момент новых данных нет — всё уже обработано!")
            
        else:
            for domain, mangas in data.items():
                if not len(mangas): continue # skip empty domains
                text = create_content(domain, mangas)
                
                await msg.answer(text, parse_mode="HTML")

    return router