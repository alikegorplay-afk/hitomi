from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag
from loguru import logger

from ...core.models import Manga, MiniManga, NamedEntity
from ...tools import required

class ParseManga:
    ALLOWED = {"contents": "genres", "artist": "author", "language": "language"}
    
    def __new__(cls, soup: BeautifulSoup, domen: str):
        title = cls.extract_title(soup)
        url = cls.extract_url(soup)
        poster = cls.extract_poster(soup, domen)
        
        genres = cls.extract_tags(soup, "标签", domen)
        author = cls.extract_tags(soup, "作者", domen)
        language = cls.extract_tags(soup, "语言", domen)
        
        return Manga(
            title = title,
            url = url,
            poster = poster,
            genres = genres,
            author = author,
            language = language,
            _id_scraper = lambda url: url.replace("https://hitomi.si/mangazine/si", '')
        )
    
    @required
    @staticmethod
    def extract_title(soup: BeautifulSoup) -> str:
        title = soup.select_one('h1')
        return title.get_text(strip=True) if title else None
    
    @required
    @staticmethod
    def extract_url(soup: BeautifulSoup) -> str:
        url = soup.select_one('link[rel="canonical"]')
        return url.get("href") if url else None
    
    @required
    @staticmethod
    def extract_poster(soup: BeautifulSoup, domen: str) -> dict[str, str]:
        poster = soup.select_one('div.img-holder img')
        if poster is None:
            return None
        if url := poster.get("src"):
            return urljoin(domen, url)
        
    @staticmethod
    def extract_tags(soup: BeautifulSoup, tag_name: str, domen: str) -> list[str]:
        for br in soup.select('div.manga-detail ul li.br'):
            if (title := br.select_one("div.md-title")) is None:
                continue
            
            elif title.get_text(strip=True) != tag_name + ":":
                continue
            
            return [NamedEntity(x.get('title'), urljoin(domen, x.get("href"))) for x in br.select("div.md-content a") if x.get('title') and x.get("href")]
        
        return []

class ParseNewUploads:
    def __new__(cls, soup: BeautifulSoup, domen: str):
        return [cls.parse_manga(manga, domen) for manga in cls.extract_all(soup)]
    
    @required
    @staticmethod
    def parse_manga(soup: Tag, domen: str) -> MiniManga:
        if not (manga := soup.select_one('div[class$="img"] a.__link')):
            return None
        
        if not (url := manga.get("href")):
            return None
        
        if not (title := manga.get("title")):
            return None
        
        if not (poster_box := manga.select_one('img')) or not (poster := poster_box.get('data-src')):
            return None
        
        return MiniManga(
            title = title,
            url = urljoin(domen, url),
            poster = urljoin(domen, poster),
            _id_scraper = lambda url: url.replace("https://hitomi.si/mangazine/si", '')
        )
    
    @required
    @staticmethod
    def extract_all(soup: BeautifulSoup):   
        return [x for x in soup.select('div.m-item') if not x.select_one('a.__link.read-more')]
            
            

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

def parse_gallery(soup: BeautifulSoup, server: str) -> list[str]:
    """Получить всю галерею"""
    urls = []
    for img in soup.select('.chapter-img img'):
        if (url := img.get("data-url")) is None:
            logger.warning(f"Не удалось получит url (html={img})")
            continue
        
        urls.append(urljoin(server, url))
    
    return urls