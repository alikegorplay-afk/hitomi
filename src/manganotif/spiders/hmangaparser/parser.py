from bs4 import BeautifulSoup

from ...core.models import Manga, MiniManga
from ..multiparser.parser import ParseManga, BasePageParser

class ParseManga(ParseManga):
    ALLOWED = {"contents": "genres", "artist": "author", "language": "language"}

class ParseNewUploads(BasePageParser):
    GALLERY_SELECTOR = 'div[class="container index-container"] div.gallery'
    
class ParsePopularNow(BasePageParser):
    GALLERY_SELECTOR = "div.container.index-container.index-popular div.gallery"

def parse_manga(soup: BeautifulSoup, domen: str) -> Manga:
    """Получить всю информацию об манге

    Args:
        soup (BeautifulSoup): Исходный суп
        domen (str): домен
        
    Raises:
        RequiredAttributeError: Если не удалось получить обязательный атрибут
        
    Returns:
        Manga: Манга с полной информацией об тайтле
    """
    return ParseManga(soup, domen)

def parse_page(soup: BeautifulSoup, domen: str) -> list[MiniManga]:
    """Получить всю информацию об новыйх тайтлах

    Args:
        soup (BeautifulSoup): Исходный суп
        domen (str): домен
        
    Raises:
        RequiredAttributeError: Если не удалось получить обязательный атрибут
        
    Returns:
        list[MiniManga]: Информация об мангах
    """
    return ParseNewUploads(soup, domen)

def parse_popular(soup: BeautifulSoup, domen: str) -> list[MiniManga]:
    """Получить всю информацию о том какие тайтлы самые популярные

    Args:
        soup (BeautifulSoup): Исходный суп
        domen (str): домен
        
    Raises:
        RequiredAttributeError: Если не удалось получить обязательный атрибут
        
    Returns:
        list[MiniManga]: Информация об мангах
    """
    return ParsePopularNow(soup, domen)