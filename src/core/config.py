import os

from pathlib import Path
from dataclasses import dataclass, field

from aiohttp import BasicAuth
from dotenv import load_dotenv
from loguru import logger
load_dotenv()

@dataclass
class ProxyConfig:
    PROXY: str | None = os.getenv("PROXY")
    PROXY_LOGIN: str | None = os.getenv("PROXY_LOGIN")
    PROXY_PASSWORD: str | None = os.getenv("PROXY_PASSWORD")
    
    def get_proxy(self) -> dict[str, str | BasicAuth]:
        if self.PROXY and self.PROXY_LOGIN and self.PROXY_PASSWORD:
            logger.info("Обнаружен прокси")
            return {
                "proxy": self.PROXY,
                "proxy_auth": BasicAuth(self.PROXY_LOGIN, self.PROXY_PASSWORD)
            }
        else:
            logger.info("Прокси отсутствует")
            return {}

@dataclass
class UserConfig:
    USERS: list[int] = field(
        default_factory=lambda: [
            int(x) for x in os.getenv("START_CHATS", "").split(',') 
            if x.strip().isdigit()
        ] if os.getenv("START_CHATS") else []
    )

@dataclass
class Config(
    ProxyConfig,
    UserConfig
):
    """
    Класс конфигурации приложения с настройками бота и парсинга.

    Использует `dataclass` для удобного создания объекта конфигурации.
    Значения по умолчанию берутся из переменных окружения или задаются явно.
    Проверяет наличие обязательных параметров при инициализации.

    Attributes:
        BOT_TOKEN (str): Токен Telegram-бота, полученный от @BotFather.
            Должен быть задан через переменную окружения `BOT_TOKEN`.
            Является обязательным параметром.
        MAX_TRY (int): Максимальное количество попыток повторного запроса
            при неудачном HTTP-запросе (по умолчанию: 5).
        MAX_CONCURENTS (int): Максимальное количество одновременных
            асинхронных задач (запросов), управляемых семафором (по умолчанию: 3).
        BASE_PARSER (str): Название парсера, используемого BeautifulSoup
            для разбора HTML-страниц (по умолчанию: 'html.parser').

    Raises:
        ValueError: Если переменная окружения `BOT_TOKEN` не установлена,
            вызывается исключение при создании экземпляра класса.

    Example:
        config = Config()
        print(config.BOT_TOKEN)  # Получение токена
        print(config.MAX_TRY)    # 5

    Note:
        Убедитесь, что переменная окружения `BOT_TOKEN` установлена перед
        созданием экземпляра класса Config, иначе будет выброшено исключение.
    """
    
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    SCAN_INTERVAL: int = int(os.getenv("SCAN_INTERVAL"))
    MAX_TRY: int = 5
    MAX_CONCURENTS: int = 3
    BASE_PARSER: str = 'html.parser'
    SAVE_DOMAIN_PATH: Path = Path('data')
    FILE_NAME: str = "domains.json"
    

    def __post_init__(self):
        """
        Проверяет корректность конфигурации после инициализации полей.

        Выполняется автоматически после создания экземпляра dataclass.
        Проверяет, что `BOT_TOKEN` задан. Если токен отсутствует,
        выбрасывается исключение `ValueError`.

        Raises:
            ValueError: Если `BOT_TOKEN` не задан в переменных окружения.
        """
        if not self.BOT_TOKEN:
            raise ValueError(
                "BOT_TOKEN is not set. Please set the BOT_TOKEN environment variable."
            )
        
        self.create_dir()
            
    def create_dir(self):
        if not self.SAVE_DOMAIN_PATH.exists():
            self.SAVE_DOMAIN_PATH.mkdir(exist_ok=True, parents=True)
        
        if not self.save_path.exists():
            with open(self.save_path, 'w', encoding='utf-8') as f:
                f.write('[]')
        
        with open(self.save_path, 'r', encoding='utf-8') as f:
            if f.readline():
                return
            
        with open(self.save_path, 'w', encoding='utf-8') as f:
            f.write('[]')
    
    @property
    def save_path(self):
        if self.SAVE_DOMAIN_PATH.exists():
            return self.SAVE_DOMAIN_PATH / self.FILE_NAME
        else:
            raise FileNotFoundError("Directory not found")

config = Config()