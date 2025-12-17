import asyncio
import aiohttp

from  .findnew import FindNewManager
from ..manganotif import __all_spiders__


class BossManager:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.spiders: list[FindNewManager] = [
            FindNewManager(x(session)) for x in __all_spiders__
        ]
    
    async def find_new(self):
        """Ищет новые манги."""
        tasks = {spider.spider.DOMEN: spider.get_new() for spider in self.spiders}
        results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), results))