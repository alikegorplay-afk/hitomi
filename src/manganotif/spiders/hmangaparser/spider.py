from loguru import logger
from bs4 import BeautifulSoup

from ...core.base import BaseSpider
from ....core.config import config
from .parser import parse_manga, parse_page, parse_popular

__all__ = [
    "HMangaSpider"
]

class HMangaSpider(BaseSpider):
    DOMEN = "https://hmanga.my"
    
    async def get_info(self, url: str):
        soup = await self._get_soup(url)
        return parse_manga(soup, self.DOMEN) if soup else None
    
    async def get_last(self):
        soup = await self._get_soup(self.DOMEN)
        return parse_page(soup, self.DOMEN) if soup else None
    
    async def get_popular(self):
        soup = await self._get_soup(self.DOMEN)
        return parse_popular(soup, self.DOMEN) if soup else None