import asyncio

from loguru import logger
from aiogram import Bot

from ...manager.bossmanager import BossManager

def create_content(domain: str, mangas: list) -> str:
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

__all__ = [
    "UserManager"
]

class UserManager:
    def __init__(self, bot: Bot, manager: BossManager):
        self.users: set[int] = set()
        self.bot = bot
        self.manager = manager
        
    def add_user(self, user_id: int):
        logger.info(f"Добавлен новый пользователь: {user_id}")
        self.users.add(user_id)
        
    async def send_all(self) -> None:
        """Проверяет на наличие новых манг, и при обнаружении отправляет сообщение"""
        
        logger.info(f"Автоматическая проверка")
        data = await self.manager.find_new()
        tasks = []
        
        if not all([True if x else False for x in data.values()]):
            #NOTE: Ничего не найдено DEBUG
            tasks = [self.bot.send_message(user_id, "Ничё нету сучка!") for user_id in self.users]
        
        else:
            for domain, mangas in data.items():
                if not len(mangas): continue # skip empty domains
                text = create_content(domain, mangas)
                
                tasks.extend([self.bot.send_message(user_id, text) for user_id in self.users])
                
        await asyncio.gather(*tasks)