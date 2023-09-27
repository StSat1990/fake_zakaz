from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu(get_pr_name_id):
    buttons = InlineKeyboardMarkup(row_width=2)

    order = InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    cart = InlineKeyboardButton(text='Корзина', callback_data='cart')

    all_products = [InlineKeyboardButton(text=f'{i[0]}', callback_data=i[1]) for i in get_pr_name_id]
    buttons.row(order, cart)
    buttons.add(*all_products)

    return buttons

def choose_product_count(plus_or_minus='', current_ammount=1):
    buttons = InlineKeyboardMarkup(row_width=3)

    back = InlineKeyboardButton(text='Назад', callback_data='back')
    plus = InlineKeyboardButton(text='+', callback_data='plus')
    minus = InlineKeyboardButton(text='-', callback_data='minus')
    count = InlineKeyboardButton(text=str(current_ammount), callback_data=str(current_ammount))
    add_to_cart = InlineKeyboardButton(text='В корзину', callback_data='to_cart')

    if plus_or_minus == 'plus':
        new_amount = int(current_ammount) + 1

        count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))

    elif plus_or_minus == 'minus':
        if int(current_ammount) > 1:
            new_amount = int(current_ammount) - 1
            count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))

    buttons.add(minus, count, plus)
    buttons.row(add_to_cart)
    buttons.row(back)

    return buttons

def get_accept():
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Подтвердить')
    no = KeyboardButton('Отменить')

    buttons.add(yes, no)

    return buttons

def get_cart():
    buttons = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton(text='Очистить корзину', callback_data='clear_cart')
    order = InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    back = InlineKeyboardButton(text='Назад', callback_data='back')

    buttons.add(clear_cart, order, back)

    return buttons

def choose_buttons():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    service_button = types.KeyboardButton('Заказать услугу')
    buttons.add(service_button)

    return buttons

def number_buttons():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    num_button = types.KeyboardButton('Поделиться контактом', request_contact=True)
    buttons.add(num_button)

    return buttons

def geo_buttons():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    geo_button = types.KeyboardButton('Отправить геолокацию', request_location=True)
    buttons.add(geo_button)

    return buttons