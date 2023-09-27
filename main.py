import telebot
import buttons
import database
from telebot import types

bot = telebot.TeleBot("TOKEN")
database.add_products('Apple', 12000, 10, 'Pro MAX', 'images/apple.jpg')
users = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if checker:
        products = database.get_pr_name_id()
        bot.send_message(user_id, 'Здравствуйте')
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))

    elif not checker:
        bot.send_message(user_id, 'Здравствуйте, отправьте свое имя')

        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id

    user_name = message.text

    bot.send_message(user_id, 'Отправьте свой номер телефона:', reply_markup=buttons.number_buttons())

    bot.register_next_step_handler(message, get_number, user_name)

def get_number(message, name):
    user_id = message.from_user.id

    if message.contact:
        phone_number = message.contact.phone_number

        database.register_user(user_id, name, phone_number, 'Not yet')
        bot.send_message(user_id, 'Вы успешно зарегистрировались', reply_markup=telebot.types.ReplyKeyboardRemove())

        products = database.get_pr_name_id()
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))

    elif not message.contact:
        bot.send_message(user_id, 'Отправьте контакт с помощью кнопки', reply_markup=buttons.number_buttons())
        bot.register_next_step_handler(message, get_number, name)

@bot.callback_query_handler(lambda call: call.data in ['minus', 'plus' , 'back', 'to_cart'])
def get_user_product_count(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'plus':
        quantity = users[user_id]['pr_count']

        users[user_id]['pr_count'] += 1

        bot.edit_message_reply_markup(user_id,  message_id, reply_markup=buttons.choose_product_count('plus', quantity))

    elif call.data == 'minus':
        quantity = users[user_id]['pr_count']
        if quantity > 1:
            users[user_id]['pr_count'] -= 1
            bot.edit_message_reply_markup(user_id, message_id, reply_markup=buttons.choose_product_count('minus', quantity))
        else:
            pass

    elif call.data == 'back':
        products = database.get_pr_name_id()

        bot.edit_message_text('Выберите пункт меню', user_id, message_id, reply_markup=buttons.main_menu(products))

    elif call.data == 'to_cart':
        quantity = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']

        database.add_product_to_cart(user_id, user_product, quantity)

        products = database.get_pr_name_id()

        bot.edit_message_text('Продукт добавлен в корзину, хотите выбрать что нибудь еще?', user_id, message_id, reply_markup=buttons.main_menu(products))

@bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'clear_cart'])
def main_menu_handle(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'order':
        bot.delete_message(user_id, message_id)
        user_cart = database.user_cart(user_id)

        full_text = 'Ваш заказ:\n\n'
        user_info = database.get_user_number_name(user_id)
        print(user_info)
        full_text += f'Имя: {user_info[0]}\nНомер телефона: {user_info[1]}\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        full_text += f'\nИтог: {total_amount}'

        bot.send_message(user_id, full_text, reply_markup=buttons.get_accept())
        bot.register_next_step_handler(call.message, get_accept,  full_text)

    elif call.data == 'cart':
        user_cart = database.user_cart(user_id)

        full_text = 'Ваша корзина:\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        full_text += f'\nИтог: {total_amount}'

        bot.edit_message_text(full_text, user_id, message_id, reply_markup=buttons.get_cart())

    elif call.data == 'clear_cart':
        database.del_product_from_cart(user_id)

        bot.edit_message_text('Ваша корзина очищена', user_id, message_id, reply_markup=buttons.main_menu(database.get_pr_name_id()))
def get_accept(message, full_text):
    user_id = message.from_user.id
    message_id = message.message_id
    user_answer = message.text

    products = database.get_pr_name_id()

    if user_answer == 'Подтвердить':
        admin_id = 6432664420
        database.del_product_from_cart(user_id)

        bot.send_message(admin_id, full_text.replace("Ваш", "Новый"))

        bot.send_message(user_id, 'Заказ оформлен, ожидайте звонка курьера', reply_markup=types.ReplyKeyboardRemove())

    elif user_answer == 'Отменить':
        bot.send_message(user_id, 'Заказ отменен', reply_markup=types.ReplyKeyboardRemove())

    bot.send_message(user_id, 'Меню', reply_markup=buttons.main_menu(products))

@bot.callback_query_handler(lambda call: int(call.data) in database.get_pr_id())
def get_user_product(call):
    user_id = call.message.chat.id

    users[user_id] = {'pr_name': call.data, 'pr_count': 1}

    message_id = call.message.message_id

    bot.edit_message_text('Выберите количество:', user_id, message_id, reply_markup=buttons.choose_product_count())

bot.infinity_polling()