from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON
from services.services import book

def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons
    ])

    return kb_builder.as_markup()


def create_three_kb(num: int) -> InlineKeyboardMarkup:
        return create_pagination_keyboard(
        'backward',
        f'{num}/{len(book)}',
        'forward')

def create_start_two_kb() -> InlineKeyboardMarkup:
        return create_pagination_keyboard(
        f'1/{len(book)}',
        'forward')

def create_end_two_kb() -> InlineKeyboardMarkup:
        return create_pagination_keyboard(
        'backward',
        f'{len(book)}/{len(book)}')