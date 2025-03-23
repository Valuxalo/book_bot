import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config_data.config import Config_book, load_config_book


config: Config_book = load_config_book()
book: dict[int, str] = {}

# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    sign = [',', '.', '!', ':', ';', '?']
    if len(text) > start + size and text[start+size-1] in sign and text[start+size-2] in sign:
        while text[start+size] in sign:
            size -= 1    

    text = text[start:start+size]
    text_inv = text[::-1]
    for i, v in enumerate(text_inv):
        if v in sign:
            break
    text_out = text if i == 0 else text[:-i]

    return text_out, len(text_out)

# Функция, формирующая словарь книги
def prepare_book(path: str, page_size: int) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    idx, n = 0, 1
    while idx < len(text):
        text_dict, ss = _get_part_text(text, idx, page_size)
        
        book[n] = text_dict.lstrip()
        idx += ss
        n +=1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(config.book.book_path)), config.book.page_size)