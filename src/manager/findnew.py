from collections import deque
from typing import Optional

from loguru import logger

from ..manganotif.core.base import BaseSpider
from ..manganotif.core.models import MiniManga

class LimitedSet:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._set: set[int] = set()
        self._deque: deque[int] = deque()
    
    def add(self, item: int) -> None:
        if item in self._set:
            return
        
        if len(self._set) >= self.max_size:
            oldest = self._deque.popleft()
            self._set.remove(oldest)
        
        self._set.add(item)
        self._deque.append(item)
    
    def __contains__(self, item: int) -> bool:
        return item in self._set
    
    def __len__(self) -> int:
        return len(self._set)
    
    def clear(self) -> None:
        self._set.clear()
        self._deque.clear()

class FindNewManager:
    def __init__(self, spider: BaseSpider):
        self.spider = spider
        self._used_ids = LimitedSet()
    
    async def has_new(self) -> bool:
        """Проверяет наличие новых манги"""
        return True if await self.get_new() else False
        
    async def get_new(self):
        """Возвращает список новых манги"""
        new_manga: list[MiniManga] = []
        
        mangas = await self.spider.get_last()
        if not mangas:
            logger.warning("Не удалось получить манги")
            return []
            
        for manga in mangas:
            if manga.id not in self._used_ids:
                self._used_ids.add(manga.id)
                new_manga.append(manga)
                
        return new_manga