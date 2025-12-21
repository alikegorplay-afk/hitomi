import json

from bs4 import BeautifulSoup
from loguru import logger

from ...core.base import BaseSpider
from .parser import parse_manga, parse_page, parse_gallery

__all__ = [
    "HitomiSpider"
]

class HitomiSpider(BaseSpider):
    DOMEN = "https://hitomi.si"
    GALLERY_URL = "https://hitomi.si/spa/manga/{id}/read"
    
    async def get_info(self, url: str):
        soup = await self._get_soup(url)
        manga = parse_manga(soup, self.DOMEN) if soup else None
        manga.gallery = await self.get_gallery(manga.id)
        return manga
    
    async def get_last(self):
        soup = await self._get_soup(self.DOMEN)
        return parse_page(soup, self.DOMEN) if soup else None
        
    async def get_by_id(self, id: str):
        return await self.get_info(f"https://hitomi.si/mangazine/si{id}")
    
    async def get_gallery(self, id: str):
        url = self.GALLERY_URL.format(id = id)
        data = json.loads(await self.get_text(url))
        try:
            return parse_gallery(BeautifulSoup(data['chapter_detail']['chapter_content'], self.parser), data['chapter_detail']['server'])
        except KeyError:
            logger.error("Путь к данным изменён, невозможно получить галерею.")
        
        return []