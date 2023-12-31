"""Module messages"""

import enum


class UserAnswer(enum.Enum):
    """Сообщения для пользователя"""
    START = "Чем могу вам помочь?"
    ANSWER_INVOICE = "Сейчас пришлю список номеров ваших накладных"
    GET_INVOICE = ("Для получения подробной информации"
                   " о накладной, укажите в ответном сообщении ее номер")


class ManagerAnswer(enum.Enum):
    """Сообщения для менеджера"""
    START = "Выберите операцию"


class CreateInvoice(enum.Enum):
    """Сообщения для создания накладной"""
    DESCRIPTION = "Укажите описание груза"
    WEIGHT = ("Укажите вес груза в граммах,"
              " например 1917, что будет равняться 1кг и 917 граммам")
    HEIGHT = ("Укажите высоту груза, например 120,"
              " что будет равняться 1-му метру и 20-ти сантиметрам")
    LENGTH = ("Укажите длину груза, например 120,"
              " что будет равняться 1-му метру и 20-ти сантиметрам")
    WIDTH = ("Укажите ширину груза, например 120,"
             " что будет равняться 1-му метру и 20-ти сантиметрам")
    WHERE_FROM = ("Укажите с какого адреса забрать груз,"
                  " пример ответа: Страна, Регион, Город, Улица, Дом,"
                  " Квартира")
    TO_LOCATION = ("Укажите на какой адрес доставить груз,"
                   " пример ответа: Страна, Регион, Город, Улица, Дом, "
                   "Квартира")
    PAYMENT = "Выберите способ оплаты"
    DROP = "Вы прекратили создавать накладную"
