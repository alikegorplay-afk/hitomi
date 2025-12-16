import asyncio

from urllib.parse import urlparse
from abc import ABC, abstractmethod
from typing import LiteralString

import aiohttp
from loguru import logger

from ...core.config import config
from .models import Manga, MiniManga

class BaseSpider(ABC):
    """Базовый класс паука"""

    DOMEN: LiteralString = "EXAMPLE"

    def __init__(
            self, 
            client: aiohttp.ClientSession, 
            max_concurents: int = config.MAX_CONCURENTS, 
            max_try: int = config.MAX_TRY,
            parser: str = config.BASE_PARSER
        ):
        self.client = client
        self.max_concurents = max_concurents
        self.max_try = max_try
        self.parser = parser
        
        self.SEMAPHORE = asyncio.Semaphore(self.max_concurents)
        self._check()

    @abstractmethod
    async def get_info(self, url: str) -> Manga:
        """Абстрактный метод для получение ифнормации об тайтле"""

    @abstractmethod
    async def get_last(self) -> list[MiniManga]:
        """Абстрактный метод для получение последней манги"""
    
    async def get_full_last(self) -> list[Manga]:
        """Метод чтобы получить полную информацию об последних тайтлах"""
        tasks = [
            asyncio.create_task(self.get_info(manga.url))
            for manga in await self.get_last()
        ]
        return await asyncio.gather(*tasks)
    
    async def get_text(
            self, 
            url: str,
            *args, 
            **kwargs
        ) -> str | None:
        """Метод для получение только текста

        Args:
            url (str): URL к запрашеваемому ресурсу

        Returns:
            str | None: Текст ресурса  иначе None
        """
        return await self.request("GET", url, *args, **kwargs)
    
    async def request(
            self, 
            method: str, 
            url: str, 
            *args, 
            **kwargs
        ) -> str | None:
        """Метод получение информации

        Args:
            method (str): Тип запроса: GET, POST, и тп.
            url (str): URL к запрашеваемому ресурсу

        Returns:
            str | None: Вернуть текст если всё успешно иначе None
        """
        async with self.SEMAPHORE: 
            for indx in range(1, self.max_try + 1):
                logger.info(f"Попытка получить данные (url={url}, method={method})")
                try:
                    async with self.client.request(method, url, *args, **kwargs) as response:
                        response.raise_for_status()
                        logger.success(f"Удалось получить данные (url={url}, status={response.status})")
                        return await response.text()
                except aiohttp.ClientResponseError as e:
                    logger.warning(f"Не удалось получить данные (status={e.status}, try-num={indx}, url={url})")
                    
                except Exception as e:
                    logger.error(f"Не удалось получит данные (try-num={indx}, error={e})")
                    
        logger.error(f"Не удалось получить данные (max-try={self.max_try}, url={url})")

    def _check(self):
        """Обязательные тесты перед инцилизацией"""
        if not urlparse(self.DOMEN).scheme:
            raise AttributeError("Не валидный URL")
        elif self.max_try < 1:
            raise ValueError("Количество попыток никак не может быть меньше нуля")
        elif not self.max_try.is_integer():
            raise ValueError("Количество попыток никак не может быть с плавающей запятой")