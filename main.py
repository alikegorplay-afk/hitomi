import asyncio

import aiohttp
from loguru import logger
from src.bot import start_bot

logger.remove()
logger.add(
    "logs.log",
    format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    rotation="10 MB",
)

async def main():
    async with aiohttp.ClientSession() as session:
        await start_bot(session)
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Процесс остановлен по желанию пользователя.")
    
    except Exception as e:
        logger.exception(f"НЕИЗВЕСТНАЯ ОШИБКА: {e}")