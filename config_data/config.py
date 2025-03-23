from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class BookBot:
    book_path: str
    page_size: int

@dataclass
class Config:
    tg_bot: TgBot

@dataclass
class Config_book:
    book: BookBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))

def load_config_book(path: str | None = None) -> Config_book:
    env = Env()
    env.read_env(path)
    return Config_book(book=BookBot(book_path=env('BOOK_PATH'), page_size=env.int('PAGE_SIZE')))