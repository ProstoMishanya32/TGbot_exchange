# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted, CantParseEntities
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from modules.services import db, json_logic
from modules.keyboards import  reply_admin, inline_page, inline_admin
from modules.utils.check_func import CheckAdmin
from modules.utils.const_func import get_unix
from handlers import start_user

from contextlib import suppress
from bot_telegram import dp

@dp.message_handler(CheckAdmin(), text = '🟠Управление биржами 🟠', state = "*")
async def admin_menu_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Панель управления биржами</b>", reply_markup=reply_admin.admin__edit_exchange())


# Создание новой категории
@dp.message_handler(CheckAdmin(), text= 'Создать биржу ➕', state="*")
async def exchange_create(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Введите название для биржи</b>")

    await state.set_state("exchange_name")


# Открытие страниц выбора категорий для редактирования
@dp.message_handler(CheckAdmin(), text= 'Изменить биржу 🖍', state="*")
async def exchange_edit(message: Message, state: FSMContext):
    await state.finish()
    if len(db.get_all_info("exchange")) >= 1:
        await message.answer("<b>🗃 Выберите биржу для изменения 🖍</b>", reply_markup= inline_page.exchange_edit_swipe_(0))

    else:
        await message.answer("<b>❌ Отсутствуют биржи для изменения позиций</b>")



# уточнение удалить все категории
@dp.message_handler(CheckAdmin(), text='Удалить все биржи ❌', state="*")
async def exchange_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>Вы действительно хотите удалить все биржи? ❌</b>\n"
                         "❗ Так же будут удалены все позиции и товары", reply_markup=inline_admin.exchange_remove_confirm())




@dp.message_handler(CheckAdmin(), text= '⬅ Главное меню', state="*")
async def exit_menu(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Добро пожаловать в Админ меню</b>", reply_markup=reply_admin.menu_admin())


####################################
########Создание категории##########
#####################################


@dp.message_handler(CheckAdmin(), state="exchange_name")
async def exchange_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 50:
        exchange_id = get_unix()
        db.add_exchange(exchange_id, message.text)
        await state.finish()

        exchange = db.get_exchange(exchange_id=exchange_id)

        await message.answer("➖➖➖➖<b>Биржа создана!</b>➖➖➖➖\n"
                            f"<b>🗃 Биржа: <code>{exchange['exchange_name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n", reply_markup=inline_admin.exchange_edit(exchange_id, 0))

    else:
        await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                             "🗃 Введите название для биржи 🏷")



# Страница выбора категорий для редактирования
@dp.callback_query_handler(CheckAdmin(), text_startswith="catategory_edit_swipe:", state="*")
async def product_exchange_edit_swipe(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>Выберите биржу для изменения</b>",reply_markup=inline_page.exchange_edit_swipe_(remover))



@dp.callback_query_handler(CheckAdmin(), text_startswith="exchange_edit_open:", state="*")
async def product_exchange_edit_open(call: CallbackQuery, state: FSMContext):
    exchange_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    await state.finish()

    exchange = db.get_exchange(exchange_id=exchange_id)


    await call.message.edit_text(f"<b>🗃 Категория: <code>{exchange['exchange_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖\n", reply_markup=inline_admin.exchange_edit(exchange_id, remover))


###########################################
#Редактирование категории #################
@dp.callback_query_handler(CheckAdmin(), text_startswith="exchange_edit_name:", state="*")
async def сategory_edit_name(call: CallbackQuery, state: FSMContext):
    exchange_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    await state.update_data(cache_exchange_id=exchange_id)
    await state.update_data(cache_exchange_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("change_exchange_name")
    await call.message.answer("<b>🗃 Введите новое название для биржи 🏷</b>", reply_markup=inline_admin.exchange_edit_cancel(exchange_id, remover))

@dp.message_handler(CheckAdmin(), state="change_exchange_name")
async def exchange_edit_name_get(message: Message, state: FSMContext):
    exchange_id = (await state.get_data())['cache_exchange_id']
    remover = (await state.get_data())['cache_exchange_remover']
    if len(message.text) <= 50:
        await state.finish()

        db.update_exchange(exchange_id, exchange_name= message.text)

        exchange = db.get_exchange(exchange_id=exchange_id)

        await message.answer(f"<b>🗃 Категория: <code>{exchange['exchange_name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖\n",  reply_markup=inline_admin.exchange_edit(exchange_id, remover))

    else:
        await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                             "🗃 Введите новое название для биржии 🏷",
                             reply_markup=inline_admin.exchange_edit_cancel(exchange_id, remover))


@dp.callback_query_handler(CheckAdmin(), text_startswith="exchange_edit_delete:", state="*")
async def exchange_edit_delete(call: CallbackQuery, state: FSMContext):
    exchange_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    await call.message.edit_text("<b>❗ Вы действительно хотите удалить биржу и все её данные?</b>", reply_markup=inline_admin.exchange_edit_delete_selected(exchange_id, remover))

# Выбор удаление или нет
@dp.callback_query_handler(CheckAdmin(), text_startswith="exchange_delete:", state="*")
async def product_exchange_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    exchange_id = call.data.split(":")[1]
    selected = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    if selected == "yes":
        db.delete_exchange(exchange_id=exchange_id)

        await call.answer("🗃 Биржа и все её данные были успешно удалены ✅")

        if len(db.get_all_info("exchange")) >= 1:
            await call.message.edit_text("<b>🗃 Выберите Биржу для изменения 🖍</b>", reply_markup=inline_page.exchange_edit_swipe_(remover))

        else:
            with suppress(MessageCantBeDeleted):
                await call.message.delete()

    else:
        exchange = db.get_exchange(exchange_id=exchange_id)
        await message.answer(f"<b>🗃 Биржа: <code>{exchange['exchange_name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖\n",  reply_markup=inline_admin.exchange_edit(exchange_id, remover))


@dp.callback_query_handler(CheckAdmin(), text_startswith="confirm_remove_exchange:", state="*")
async def exchange_remove_confirm(call: CallbackQuery, state: FSMContext):
    selected = call.data.split(":")[1]

    if selected == "yes":
        exchange = len(db.get_all_info("exchange"))
        db.clear_all_exchange()

        await call.message.edit_text(f"<b>🗃 Вы удалили все биржи<code>({exchange}шт)</code> ☑</b>")
    else:
        await call.message.edit_text("<b>🗃 Вы отменили удаление всех бирж ✅</b>")

