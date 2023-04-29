import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb
from bot_telegram import dp
from modules.services import db, main_config


def exchange_edit_swipe_(remover):
    get_categories = db.get_all_info("exchange")
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['exchange_name'],
                             callback_data=f"exchange_edit_open:{get_categories[a]['exchange_id']}:{remover}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"))

    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...") )

    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"), )

    return keyboard



def exchange_swipe_fp(remover):
    get_categories = db.get_all_info('exchange')
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['exchange_name'],
                             callback_data=f"buy_exchange_open:{get_categories[a]['exchange_id']}:0"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_exchange_swipe:{remover + 10}"),
        )

    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_exchange_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )

    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_exchange_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_exchange_swipe:{remover + 10}"),
        )

    return keyboard


def exchange_name__swipe_fp(remover):
    get_categories = main_config.bot.exchange
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10


    for count, a in enumerate(range(remover, len(get_categories))):

        if count < 10:
            keyboard.add(ikb(get_categories[a],
                             callback_data=f"name_exchange_create:{(get_categories[a])}:0"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"name_exchange_swipe:{remover + 10}"),
        )

    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"name_exchange_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )

    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"name_exchange_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"name_exchange_swipe:{remover + 10}"),
        )

    return keyboard