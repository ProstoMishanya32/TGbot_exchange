# - *- coding: utf- 8 - *-

from aiogram import executor, Dispatcher

from handlers import dp

from modules.utils import main_config
from modules.utils.logging_system import logger
from modules.utils.bot_commands import set_commands
from modules import alerts
from modules.services import db

import os, sys, colorama

colorama.init() #инициализация colorama для цветного текста


async def on_startup(dp: Dispatcher): # Запуск бота
    await set_commands(dp) #Установка перевоначальных команд для пользователей
    await alerts.on_startup_notify(dp) #Оповещение админов при старте
    db.start_bot(colorama) #Подключение БД
    logger.warning("Бот вошел в сеть") #Подключение логгирования
    print(colorama.Fore.LIGHTBLUE_EX + "--- Бот вошел в сеть ---\n" + colorama.Fore.LIGHTRED_EX +
    "--- Разработчик @michailcoding ---\n"
    + colorama.Fore.YELLOW + "--- https://kwork.ru/user/prostomishanya32 ---" +  colorama.Fore.RESET)







if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
