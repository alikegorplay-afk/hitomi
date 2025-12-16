"""ТГ Бот, для манги"""

from aiohttp import ClientSession
from aiogram import Bot, Dispatcher

from .handlers import get_handlers
from ..core.config import config

def get_bot(session: ClientSession) ->  tuple[Bot, Dispatcher]:
    
    dp = Dispatcher()
    bot = Bot(config.BOT_TOKEN)
    
    dp.include_routers(  # NOTE: Единый вход для добавление новых роутов.
        *get_handlers(session)
    )
    
    return bot, dp

async def start_bot(session: ClientSession):
    """
    Запускает бота.

    Перед началом опроса вебхуки отключаются — это необходимо при использовании
    режима polling, чтобы избежать конфликта между вебхуками и опросом.

    Пример использования:
        await start_bot()
    """
    bot, dp = get_bot(session)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)