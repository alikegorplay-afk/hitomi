"""ТГ Бот, для манги"""
import asyncio

from aiohttp import ClientSession
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession

from ..manager.bossmanager import BossManager
from .manager import UserManager
from .handlers import get_handlers
from ..core.config import config

commands = [
    BotCommand(command="start", description="Приветствие"),
    BotCommand(command="help", description="Получить справку")
]

def get_bot(manager: BossManager) ->  tuple[Bot, Dispatcher, UserManager]:
    dp = Dispatcher()
    session = AiohttpSession(proxy=(config.PROXY, config.get_proxy()["proxy_auth"])) if config.get_proxy() else None
    
    bot = Bot(config.BOT_TOKEN, session)
    user_manager  = UserManager(bot, manager)
    
    dp.include_routers(  # NOTE: Единый вход для добавление новых роутов.
        *get_handlers(manager, user_manager)
    )
    
    return bot, dp, user_manager

async def start_check(user_manager: UserManager):
    """Начинаетс вечную проверку

    Args:
        user_manager (UserManager): Менеджер пользователей
    """
    while True:
        await user_manager.send_all()
        await asyncio.sleep(config.SCAN_INTERVAL)

async def start_bot(session: ClientSession):
    """
    Запускает бота.

    Перед началом опроса вебхуки отключаются — это необходимо при использовании
    режима polling, чтобы избежать конфликта между вебхуками и опросом.

    Пример использования:
        await start_bot()
    """
    manager = BossManager(session)
    bot, dp, user_manager = get_bot(manager)
    
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    
    await asyncio.gather(
        dp.start_polling(bot),
        start_check(user_manager)
    )