from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)

from config import TOKEN, admin_id, webapp_url


def get_main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    webAppInfo = types.WebAppInfo(url=webapp_url, display_name="Страница сайта")

    b1 = KeyboardButton("Заказать оборудование", web_app=webAppInfo)
    b2 = KeyboardButton("О наc")
    b3 = KeyboardButton("Написать в поддержку")
    b5 = KeyboardButton("Заказать обратный звонок")
    b6 = KeyboardButton("Получить презентацию")
    kb.add(b1)
    kb.add(b3)
    kb.add(b5)
    kb.add(b6, b2)
    return kb


def get_chatbot_keyboard(manager_type=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("Поговорить с менеджером")
    b2 = KeyboardButton("Прекратить диалог")
    if not manager_type:
        kb.add(b1)
    kb.add(b2)
    return kb


def get_final_order_btns():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("Подтвердить")
    b3 = KeyboardButton("Отменить")
    kb.add(b1)
    kb.add(b3)
    return kb


start_message = "Привет! Я ЭнергоПроБот. Чем могу вам помочь?"

about_message = """
Основной миссией "Завода Энерготехники" является работа и обеспечение заказчика электрощитовой продукции. "Завод Энерготехника" выполняет проекты заказчика с высоким качеством. Мы говорим высокое напряжение - высокое качество.
  
Мы - Высококвалифицированный персонал, опытные конструкторы и современные производственные мощности позволяют нам постоянно расширять и обновлять номенклатуру выпускаемого оборудования.

Компания ООО Завод "Энерготехника" выпускает корпуса электрощитов навесного и напольного типа, пульты, распределительные панели ЩО 70. Все корпуса выполнены в едином конструктиве и с универсальным набором аксессуаров для всех типов шкафов. Корпуса комплектуются рейками, монтажными платами различных размеров. Степень защиты шкафов IP 54.

Наш адрес: 192148, г. Санкт - Петербург, ул. Невзоровой д. 9
(въезд для грузового транспорта до 16.30, через Уездный переулок)

Тел./факс: +7 (812) 560-59-24

E-mail: info@zavod-et.ru"""

start_talk = "Что вас интересует?"

end_dialog = 'Диалог завершен.'
