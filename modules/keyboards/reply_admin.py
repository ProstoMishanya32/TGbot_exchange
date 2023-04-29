# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from modules.services import db
from modules.utils import main_config


def menu_admin():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🟠Управление биржами 🟠")
    keyboard.row("🧑‍✈️ Администаторы", "Изменить текст лиц. соглашения")
    keyboard.row("Выйти из Админ меню⬆️")
    return keyboard

# Кнопки главного меню
def admin__edit_selected():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Добавить Администратора", "Удалить Администратора")
    keyboard.row("Посмотреть список Администраторов", "Назад в меню")
    return keyboard

def admin_back():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Назад")
    return keyboard

def admin__edit_exchange():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Создать биржу ➕", "Изменить биржу 🖍", "Удалить все биржи ❌")
    keyboard.row("⬅ Главное меню")
    return keyboard

def admin__edit_texts():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🇷🇺 Русский", "🇬🇧 Английский")
    keyboard.row("Отмена")
    return keyboard

def admin__edit_texts_cancel():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Отмена")
    return keyboard


