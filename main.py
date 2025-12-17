import asyncio

import aiohttp
from loguru import logger
from src.bot import start_bot

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