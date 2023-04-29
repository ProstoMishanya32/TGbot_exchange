from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb



def exchange_edit(exchange_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("🏷 Изм. название", callback_data=f"exchange_edit_name:{exchange_id}:{remover}")
    ).add(
        ikb("⬅ Вернуться ↩", callback_data=f"catategory_edit_swipe:{remover}"),
        ikb("❌ Удалить", callback_data=f"exchange_edit_delete:{exchange_id}:{remover}"))

    return keyboard

def exchange_edit_cancel(exchange_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Отменить", callback_data=f"exchange_edit_open:{exchange_id}:{remover}"),
    )
    return keyboard

# Кнопки с удалением категории
def exchange_edit_delete_selected(exchange_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Да, удалить", callback_data=f"exchange_delete:{exchange_id}:yes:{remover}"),
        ikb("✅ Нет, отменить", callback_data=f"exchange_delete:{exchange_id}:not:{remover}")
    )

    return keyboard


def exchange_remove_confirm():
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Да, удалить все", callback_data="confirm_remove_exchange:yes"),
        ikb("✅ Нет, отменить", callback_data="confirm_remove_exchange:not")
    )
    return keyboard

def item_remove_confirm():
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Да, удалить все", callback_data="confirm_remove_item:yes"),
        ikb("✅ Нет, отменить", callback_data="confirm_remove_item:not")
    )

    return keyboard
