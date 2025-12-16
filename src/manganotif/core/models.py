import re
from dataclasses import dataclass, field
from typing import Optional, Callable
from urllib.parse import urlparse

@dataclass
class NamedEntity:
    """Базовый класс для именованных сущностей с URL"""
    name: str
    url: str = ""
    
    def __str__(self) -> str:
        return self.name

Author = NamedEntity
Genre = NamedEntity
Language = NamedEntity

class IdScraper:
    """Класс для извлечения ID из URL"""
    @staticmethod
    def base_scraper(url: str) -> str:
        """Базовый скрапер: берет последнюю часть пути и разбивает по '-'"""
        path = urlparse(url).path.rstrip('/')
        return path.split('/')[-1].split('-')[0]
    
    @staticmethod
    def numeric_scraper(url: str) -> str:
        """Извлекает только цифры из последнего сегмента URL"""
        path = urlparse(url).path.rstrip('/')
        last_part = path.split('/')[-1]
        numbers = re.findall(r'\d+', last_part)
        return numbers[0] if numbers else ''

@dataclass
class MiniManga:
    """Базовый класс для храниение базовой информации
    Args:
        title (str): Название
        url (str): URL к тайтлу
        poster (str): URL к постеру сайта
    """
    title: str
    url: str
    poster: str
    _id_scraper: Callable[[str], str] = field(
        default=IdScraper.base_scraper,
        repr=False,
        compare=False,
        kw_only=True
    )
    
    @property
    def id(self) -> int:
        scraped_id = self._id_scraper(self.url)
        return int(scraped_id) if scraped_id and scraped_id.isdigit() else 0
    
    def __post_init__(self):
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL: {self.url}")

@dataclass
class Manga(MiniManga):
    """Базовый класс для храниение полной информации об тайтле
    Args:
        title (str): Название
        url (str): URL к тайтлу
        poster (str): URL к постеру сайта
        gallery (list[str]): URL постеров
        genres (list[Genre] | None): Жанры тайтла
        author (Author | None): Автор тайтла
        language (Language | None): Язык тайтла
    """
    gallery: list[str] = field(default_factory=list)
    genres: list[Genre] = field(default_factory=list)
    author: list[Author] = field(default_factory=list)
    language: list[Language] = field(default_factory=list)