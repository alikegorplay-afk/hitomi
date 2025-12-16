import asyncio

import aiohttp
from src.bot import start_bot

async def main():
    async with aiohttp.ClientSession() as session:
        await start_bot(session)
        
        
if __name__ == '__main__':
    asyncio.run(main())