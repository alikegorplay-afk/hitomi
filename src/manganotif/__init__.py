"""Все парсеры сайтов"""
from typing import NamedTuple
from .spiders import hmangaparser, multiparser, hentaio, hitomisi
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
HitomiSi = hitomisi.HitomiSpider

__suppor_sites__ = [
    SupporSite("multi-manga", "https://multi-manga.today"),
    SupporSite("hmanga", "https://hmanga.my"),
    SupporSite("hentai1", "https://hentai1.io"),
    SupporSite("hitomi.si", "https://hitomi.si")
]

__all_spiders__: list[BaseSpider] = [
    HManga,
    MultiManga,
    HentaiO,
    HitomiSi
]