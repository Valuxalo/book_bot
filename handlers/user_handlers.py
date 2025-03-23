from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination_kb import create_three_kb, create_start_two_kb, create_end_two_kb
from lexicon.lexicon_ru import LEXICON
from services.services import book

router = Router()

#На команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

#На команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

#На команду /beginning, отправляет первую страницу книги
@router.message(Command(commands='beginning'))
async def process_begin_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_start_two_kb()
    )

#На команду /continue, отправляет страницу, на которой пользователь остановился
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_three_kb(users_db[message.from_user.id]["page"])
    )

#На команду /bookmarks, отправляет сохранённые закладки
@router.message(Command(commands='bookmarks'))
async def process_continue_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])

#На кнопку вперёд
@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] += 1
    text = book[users_db[callback.from_user.id]['page']]
    if users_db[callback.from_user.id]['page'] != len(book):
        await callback.message.edit_text(
            text=text,
            reply_markup=create_three_kb(users_db[callback.from_user.id]["page"])
        )
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_end_two_kb(users_db[callback.from_user.id]["page"])
        )

#На кнопку назад
@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] -= 1
    text = book[users_db[callback.from_user.id]['page']]
    if users_db[callback.from_user.id]['page'] != 1:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_three_kb(users_db[callback.from_user.id]["page"])
        )
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_start_two_kb()
        )

#На номер текущей страницы
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки')

#На закладку из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_three_kb(users_db[callback.from_user.id]["page"])
        )
    

#На кнопку редактировать под закладками
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]["bookmarks"]
            )
        )
    
#на отменить
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])

#на нажатие закладки для удаления
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_press(callback: CallbackQuery):
    users_db[callback.from_user.id]["bookmarks"].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]["bookmarks"]:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]['bookmarks'] 
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])

