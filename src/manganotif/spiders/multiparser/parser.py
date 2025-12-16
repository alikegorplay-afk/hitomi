from urllib.parse import  urljoin

from bs4 import BeautifulSoup
from loguru import logger

from ...core.models import Manga, MiniManga, NamedEntity
from ...core.errors import RequiredAttributeError
from ...tools import required

class ParseManga:
    ALLOWED = {"теги": "genres", "автор": "author", "язык": "language"}
    
    
    def __new__(cls, soup: BeautifulSoup, domen: str) -> Manga:
        title = cls._parse_title(soup)
        url = cls._parse_url(soup)
        poster = urljoin(domen, cls._parse_poster(soup))
        
        gallery = [urljoin(domen, x) for x in cls._parse_gallery(soup)]
        tags = cls._parse_tags(soup, cls.ALLOWED)
        
        return Manga(
            title = title,
            url = url,
            poster = poster,
            gallery = gallery,
            **tags
        )
    
    @staticmethod
    def _parse_tags(soup: BeautifulSoup, allowed_tags: dict[str, str]) -> dict[str, NamedEntity]:
        tags = {}
        for tag in soup.select("section#tags div.tag-container"):
            if not tag.next_element or not (tag_all := tag.select("a.tag")):
                continue
            elif not (tag_name := allowed_tags.get(tag.next_element.get_text(strip=True).lower())):
                continue
            
            tags[tag_name] = [
                NamedEntity(x.get_text(strip=True), x.get("href"))
                for x in tag_all
            ]
        return tags
                
    
    @required
    @staticmethod
    def _parse_gallery(soup: BeautifulSoup) -> list[str]:
        gallery = soup.select("#thumbnail-container div.thumb-container img")
        if gallery:
            return [x.get("data-src") for x in gallery if x.get("data-src")]
        
    @required
    @staticmethod
    def _parse_poster(soup: BeautifulSoup) -> str:
        url = soup.select_one('#cover img')
        if url is not None:
            return url.get("data-src")
    
    @required
    @staticmethod
    def _parse_url(soup: BeautifulSoup) -> str:
        url = soup.select_one('link[rel="canonical"]')
        if url is not None:
            return url.get("href")

    @required
    @staticmethod
    def _parse_title(soup: BeautifulSoup) -> str:
        h1 = soup.select_one('#info h1')
        if h1 is not None:
            return h1.get_text(strip=True)

class BasePageParser:
    GALLERY_SELECTOR = "div.gallery"
    
    def __new__(cls, soup: BeautifulSoup, domen: str) -> list[MiniManga]:
        return [cls._extract_mini_manga(x, domen) for x in cls._extract_all(soup, cls.GALLERY_SELECTOR)]
    
    @required
    @staticmethod
    def _extract_mini_manga(soup: BeautifulSoup, domen: str) -> MiniManga:
        if not (title := soup.get_text(strip=True)):
            raise RequiredAttributeError("Обязательный атрибут (attr='title') не найден")
        if (url := soup.select_one("a")) is None or not url.get("href"):
            raise RequiredAttributeError("Обязательный атрибут (attr='url') не найден")
        if (img := soup.select_one("img")) is None or not img.get("data-src"):
            raise RequiredAttributeError("Обязательный атрибут (attr='url') не найден")
        
        return MiniManga(
            title = title,
            url = url.get("href"),
            poster = urljoin(domen, img.get("data-src"))
        )
    
    @required
    @staticmethod
    def _extract_all(soup: BeautifulSoup, selector: str = GALLERY_SELECTOR):
        logger.debug(f'CSS селектор для (CSS="{selector}")')
        return soup.select(selector)

class ParseNewUploads(BasePageParser):
    GALLERY_SELECTOR = "#dle-content div.gallery"
    
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