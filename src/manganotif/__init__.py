"""Все парсеры сайтов"""
from typing import NamedTuple
from .spiders import hmangaparser, multiparser, hentaio
from .core.base import BaseSpider

__all__ = [
    "HManga",
    "MultiManga"
]

class SupporSite(NamedTuple):
    name: str
    domen: str

HManga = hmangaparser.HMangaSpider
MultiManga = multiparser.MultiMangaSpider
HentaiO = hentaio.HentaIoSpider

__suppor_sites__ = [
    SupporSite("multi-manga", "https://multi-manga.today"),
    SupporSite("hmanga", "https://hmanga.my"),
    SupporSite("hentai1", "https://hentai1.io")
]

__all_spiders__: list[BaseSpider] = [
    HManga,
    MultiManga,
    HentaiO
]