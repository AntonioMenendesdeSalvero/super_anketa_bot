from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Головне меню з кнопками
def get_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Про нас')],
            [KeyboardButton(text='Аналітика')],
            [KeyboardButton(text='Подати інформацію про себе')],
            [KeyboardButton(text='Для адміністратора')],
            [KeyboardButton(text='Профіль')]
        ],
        resize_keyboard=True
    )

# Інлайн-клавіатура для профілю
def get_profile_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Переглянути свою анкету', callback_data='view_own_profile')],
        [InlineKeyboardButton(text='Видалити анкету', callback_data='delete_profile')]
    ])

# Інлайн-клавіатура для адміністратора
def get_admin_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Список користувачів', callback_data='user_list')],
        [InlineKeyboardButton(text='Додати адміна', callback_data='add_admin')],
        [InlineKeyboardButton(text='Детальний перегляд анкети', callback_data='view_user_details')]
    ])
