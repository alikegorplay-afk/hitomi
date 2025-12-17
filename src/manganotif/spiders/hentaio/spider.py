from ...core.base import BaseSpider
from .parser import parse_manga, parse_page

__all__ = [
    "HentaIoSpider"
]

class HentaIoSpider(BaseSpider):
    DOMEN = "https://hentai1.io"
    
    async def get_info(self, url: str):
        soup = await self._get_soup(url)
        return parse_manga(soup, self.DOMEN) if soup else None
    
    async def get_last(self):
        soup = await self._get_soup(self.DOMEN)
        return parse_page(soup, self.DOMEN) if soup else None
    
    #async def get_chapter_img(self, url: str):
    #    soup = await self._get_soup(url) # NOTE: На потом)
    #    
        
    async def get_by_id(self, id: str):
        return await self.get_info(f"https://hentai1.io/?p={id}")