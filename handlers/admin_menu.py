# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.services import db, json_logic
from bot_telegram import dp
from modules.keyboards import  reply_admin, inline_page, inline_user, inline_admin
from contextlib import suppress
from modules.utils.check_func import CheckAdmin
from handlers import start_user
from bot_telegram import bot

@dp.message_handler(CheckAdmin(), text = '/admin', state = "*")
async def admin_menu(message: Message, state: FSMContext):
    await message.answer("<b>Добро пожаловать в Админ меню</b>", reply_markup=reply_admin.menu_admin())


@dp.message_handler(CheckAdmin(), text = '🧑‍✈️ Администаторы', state = "*")
async def admin_menu_start(message: Message, state: FSMContext):
    await message.answer("<b>Панель управления администраторами</b>", reply_markup=reply_admin.admin__edit_selected())


@dp.message_handler(CheckAdmin(), text = 'Добавить Администратора', state = "*")
async def admin_edit_menu(message: Message, state: FSMContext):

    await message.answer("<b>Перешлите <code>сообщение пользователя</code>, которого хотите добавить в Администаторы, в диалог с ботом</b>", reply_markup=reply_admin.admin_back())
    await state.set_state("add_admin")

@dp.message_handler(CheckAdmin(), state = "add_admin")
async def add_admin(message: Message, state: FSMContext):
    if message.text in ['Назад']:
        await state.finish()
        await message.answer("<b>Панель управления администраторами</b>", reply_markup=reply_admin.admin__edit_selected())

    else:
        try:
            user_id = message['forward_from']['id']
            if message['forward_from']['last_name'] == None:
                nickname = message['forward_from']['first_name']
            else:
                nickname = f"{message['forward_from']['first_name']} {message['forward_from']['last_name']}"

            result = json_logic.add_admin(user_id, nickname)
            if result:
                await message.answer("<b>Успешно 👍</b>\n"
                                     f"Пользователь <code>{nickname}</code> добавлен в Администраторы",
                                     reply_markup=reply_admin.admin__edit_selected())

                await state.finish()

        except TypeError:
            await message.answer("<b>Не найдено пересланое сообщение. Повторите попытку! Или пользователь запретил пересылку сообщений</b>", reply_markup=reply_admin.admin_back())

            await state.set_state("add_admin")

@dp.message_handler(CheckAdmin(), text = 'Удалить Администратора', state = "*")
async def admin_delete_admin(message: Message, state: FSMContext):
    await see_admin(message)
    await message.answer("<b>Введите <code>ID Администратора</code>, которого хотите удалить 👆</b>", reply_markup=reply_admin.admin_back())

    await state.set_state("delete_admin")

@dp.message_handler(CheckAdmin(), text = 'Назад в меню', state = "*")
async def admin_exit_menu(message: Message, state: FSMContext):
    await message.answer("<b>Добро пожаловать в Админ меню</b>", reply_markup=reply_admin.menu_admin())

@dp.message_handler(CheckAdmin(), text = 'Выйти из Админ меню⬆️', state = "*")
async def admin_exit(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Успешно 👍", reply_markup=None)





@dp.message_handler(CheckAdmin(), state = "delete_admin")
async def admin_delete_admin(message: Message, state: FSMContext):

    if message.text in ['Назад']:
        await state.finish()
        await message.answer("<b>Панель управления администраторами</b>", reply_markup=reply_admin.admin__edit_selected())

    else:
        admins = json_logic.see_admins()
        user_ids = []
        for character in admins:
            user_ids.append(character['user_id'])
        try:
            if int(message.text) in user_ids:
                json_logic.remove_admin(message.text)
                await message.answer("<b>Успешно 👍</b>", reply_markup=reply_admin.admin__edit_selected())

                await state.finish()

            else:
                await message.answer("<b>ID сообщения не найден! Повторите попытку</b>", reply_markup=reply_admin.admin_back())

                await state.set_state("delete_admin")
        except ValueError:
            await message.answer("<b>ID сообщения должен содержать только целые числа. Повторите попытку</b>",reply_markup=reply_admin.admin_back())

            await state.set_state("delete_admin")


@dp.message_handler(CheckAdmin(), text = 'Посмотреть список Администраторов', state = "*")
async def admin_see_admins(message: Message, state: FSMContext):
    await see_admin(message)

async def see_admin(message):
    admins = json_logic.see_admins()
    text = ''
    if admins:
        for character in admins:
            text += f"<b>#{character['position']}  {character['nickname']} || <code>{character['user_id']}</code></b>\n"
    await message.answer(f"<b>ИМЯ ➖➖➖➖➖➖ ID</b>\n{text}")


@dp.message_handler(text = 'Изменить текст лиц. соглашения', state = "*")
async def edit_texts(message: Message, state: FSMContext):
    await state.set_state("change_texts")
    await message.answer("<b>⚒ Выберите нужный пункт:</b>", reply_markup=reply_admin.admin__edit_texts())



@dp.message_handler(state = "change_texts")
async def get_category(message: Message, state: FSMContext):
    text_category = message.text

    await state.set_state("change_text_final")

    if text_category == "🇷🇺 Русский":
        message_text = json_logic.get_texts(f"licensing_agreement_ru")
        await state.update_data(text_category=f"licensing_agreement_ru")

    elif text_category == "🇬🇧 Английский":
        message_text = json_logic.get_texts(f"licensing_agreement_eng")
        await state.update_data(text_category= f"licensing_agreement_eng")

    with suppress(MessageCantBeDeleted):
        await message.delete()


    await message.answer(f"<b>Введите новый текст данного отдела!</b>\nСтарый текст таков: \n\n<i>{message_text}</i>", reply_markup = reply_admin.admin__edit_texts_cancel())


@dp.message_handler(state = "change_text_final")
async def edit_texts_selected(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await start_user.user_menu(message)
    else:
        async with state.proxy() as data:
            text_category = data['text_category']
        json_logic.update_texts(text_category, message.text)
        await state.finish()
        await message.answer("Успешно!", reply_markup = reply_admin.menu_admin())


