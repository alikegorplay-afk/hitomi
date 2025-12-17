from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag
from loguru import logger
from ...core.errors import RequiredAttributeError
from ...core.models import MiniManga, Manga, NamedEntity
from ...tools import required

class ParsePage:
    GALLERY_SELECTOR = "div.page-item-detail.manga"
    
    def __new__(cls, soup: BeautifulSoup, domen: str):
        return [cls.parse_child(manga_item, domen) for manga_item in cls.find_all(soup)]
            
    @required
    @staticmethod
    def find_all(soup: BeautifulSoup, selector: str = GALLERY_SELECTOR):
        logger.debug(f'CSS селектор (CSS="{selector}")')
        return soup.select(selector)
        
    @required
    @staticmethod
    def parse_child(soup: Tag, domen: str):
        if (title := soup.select_one("div.item-summary h3.h5")) is None or not (name := title.get_text(strip=True)):
            raise RequiredAttributeError("Обязательный атрибут (attr='title') не найден")
        if (url_box := title.select_one("a")) is None or not (url := url_box.get('href')):
            raise RequiredAttributeError("Обязательный атрибут (attr='url') не найден")
        if (img := soup.select_one("img")) is None or not (img_url := img.get("src")):
            raise RequiredAttributeError("Обязательный атрибут (attr='url') не найден")
        if _id := soup.select_one("div.item-thumb"):
            _id_scrapper = lambda _: _id.get("data-post-id")
        
        return MiniManga(
            title = name,
            url = url,
            poster = urljoin(domen, img_url),
            _id_scraper = _id_scrapper
        )

class ParseManga:
    ALLOWED = {"genre(s)": "genres", "author(s)": "author", "language(s)": "language"}
    
    def __new__(cls, soup: BeautifulSoup, domen: str) -> Manga:
        title = cls._parse_title(soup)
        url = cls._parse_url(soup)
        poster = urljoin(domen, cls._parse_poster(soup))
        
        gallery = [urljoin(domen, x) for x in cls._parse_gallery(soup)]
        tags = cls._parse_tags(soup, cls.ALLOWED)
        if _id := soup.select_one("input.rating-post-id"):
            _id_scrapper = lambda _: _id.get("value")
        
        return Manga(
            title = title,
            url = url,
            poster = poster,
            gallery = gallery,
            **tags,
            _id_scraper = _id_scrapper
        )

    @staticmethod
    def _parse_tags(soup: BeautifulSoup, allowed_tags: dict[str, str]) -> dict[str, NamedEntity]:
        genres = [NamedEntity(x.get_text(strip=True), x.get('href')) for x in soup.select("div.genres-content a")]
        author = [NamedEntity(x.get_text(strip=True), x.get('href')) for x in soup.select("div.author-content a")]
        language = [NamedEntity("English")] # Это скорее костыль так-как на сайте все манги на английском
        
        return {
            "genres": genres,
            "author": author,
            "language": language
        }
    
    @required
    @staticmethod
    def _parse_gallery(soup: BeautifulSoup) -> list[str]:
        if (gallery := soup.select_one("div.page-content-listing.single-page")):
            return [x.get("href") for x in gallery.select("li.wp-manga-chapter a")]
        else:
            raise RequiredAttributeError("Обязательный атрибут (attr='gallery') не найден")
    
    @required
    @staticmethod
    def _parse_poster(soup: BeautifulSoup) -> str:
        url = soup.select_one('div.tab-summary img')
        if url is not None:
            return url.get("src")
    
    
    @required
    @staticmethod
    def _parse_title(soup: BeautifulSoup):
        title  = soup.select_one("div.post-title h1")
        if title is not None:
            return title.get_text(strip=True)
        
    @required
    @staticmethod
    def _parse_url(soup: BeautifulSoup) -> str:
        url = soup.select_one('link[rel="canonical"]')
        if url is not None:
            return url.get("href")
    

def parse_page(soup: BeautifulSoup, domen: str) -> list[MiniManga]:
    """Получить всю информацию об новыйх тайтлах"""
    return ParsePage(soup, domen)

def parse_manga(soup: BeautifulSoup, domen: str) -> Manga | None:
    """Получить всю информацию о манге"""

    return ParseManga(soup, domen)