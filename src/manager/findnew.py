from ..manganotif.core.base import BaseSpider
from ..manganotif.core.models import MiniManga

class FindNewManager:
    def __init__(self, spider: BaseSpider):
        self.spider = spider
        self._used_ids: set[int] = set()
    
    async def has_new(self) -> bool:
        """Проверяет наличие новых манги"""
        return True if await self.get_new() else False
        
    async def get_new(self):
        """Возвращает список новых манги"""
        new_manga: list[MiniManga] = []
        
        mangas = await self.spider.get_last()
        for manga in mangas:
            if manga.id not in self._used_ids:
                self._used_ids.add(manga.id)
                new_manga.append(manga)
                
        return new_manga