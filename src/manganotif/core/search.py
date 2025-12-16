from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from .models import MiniManga

# Это на будующий, если будет реализовано много поисковых движков (ЛОЛ)

class BaseSearch(ABC):
    """
    Абстрактный класс для поисковой функциональности.
    Может быть использован как миксин или отдельная сущность.
    """

    @abstractmethod
    async def search(self, query: str) -> List[MiniManga]:
        """
        Поиск манги по текстовому запросу.

        Args:
            query (str): Поисковый запрос.

        Returns:
            List[MiniManga]: Список найденных тайтлов.
        """

    @abstractmethod
    async def tags(self) -> Dict[str, str]:
        """
        Получить список доступных тегов/жанров.

        Returns:
            Dict[str, str]: Словарь {название_тега: идентификатор_или_url}
        """

    @abstractmethod
    async def search_by_tags(
            self,
            tags: List[str]
    ) -> List[MiniManga]:
        """
        Поиск манги по тегам.

        Args:
            tags (List[str]): Список тегов (например, ["боевик", "сёнен"]).

        Returns:
            List[MiniManga]: Отфильтрованные тайтлы.
        """