import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token='7955193002:AAHMXa15LTyrsWKfyYMkoG0TyaAzCSdYPg0')
dp = Dispatcher()
# cod = 1234
ADMIN_IDS = [456028350]  # Список адміністративних ID
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

class RegistrationStates(StatesGroup):
    photo = State()
    description = State()
    price = State()
    seminar_link = State()
    phone_number = State()

# Створюємо таблицю, якщо вона ще не існує
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    full_name TEXT,
                    phone_number TEXT,
                    photo TEXT,
                    description TEXT,
                    price INTEGER,
                    seminar_link TEXT
                )''')
conn.commit()
# cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
# cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
# cursor.execute("ALTER TABLE users ADD COLUMN phone_number TEXT")
conn.commit()
# Перевірка і додавання нових колонок, якщо вони відсутні
try:
    cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
except sqlite3.OperationalError:
    pass  # Колонка вже існує

try:
    cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
except sqlite3.OperationalError:
    pass  # Колонка вже існує

try:
    cursor.execute("ALTER TABLE users ADD COLUMN phone_number TEXT")
except sqlite3.OperationalError:
    pass  # Колонка вже існує
conn.commit()


user_data = {}

def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Про нас')],
            [KeyboardButton(text='Аналітика')],
            [KeyboardButton(text='Подати інформацію про себе')],
            [KeyboardButton(text='Для адміністратора')],
            [KeyboardButton(text='Профіль')]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_admin_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Список користувачів', callback_data='user_list')],
        [InlineKeyboardButton(text='Додати адміна', callback_data='add_admin')],
        [InlineKeyboardButton(text='Детальний перегляд анкети', callback_data='view_user_details')]
    ])
    return keyboard

def get_profile_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Переглянути свою анкету', callback_data='view_own_profile')],
        [InlineKeyboardButton(text='Видалити анкету', callback_data='delete_profile')]
    ])
    return keyboard

@dp.message(CommandStart())
async def start_com(message: Message):
    await message.answer(text='Вітаю!', reply_markup=get_reply_keyboard())

# @dp.message(F.text == '1234')
# async def good_code(message: Message):
#     await message.answer(
#         text='Пароль вірний. Тож використовуй кнопки для навігації',
#         reply_markup=get_reply_keyboard())

@dp.message(F.text == 'Про нас')
async def for_me_btn(message: Message):
    await message.answer('Це розділ про нас')

@dp.message(F.text == 'Аналітика')
async def analitic_btn(message: Message):
    await message.answer('Розділ Аналітики')


@dp.message(F.text == 'Переглянути свою анкету')
async def view_profile(message: Message):
    user_id = message.from_user.id
    cursor.execute(
        'SELECT photo, description, price, seminar_link FROM users WHERE user_id = ?',
        (user_id,))
    user = cursor.fetchone()

    if user:
        photo_id, description, price, seminar_link = user
        # Надсилаємо фото
        await message.answer_photo(photo=photo_id, caption="Ось ваша анкета:")
        # Надсилаємо іншу інформацію
        profile_info = (
            f"Опис: {description}\n"
            f"Ціна: {price} грн\n"
            f"Посилання на семінар: {seminar_link}"
        )
        await message.answer(profile_info)
    else:
        await message.answer("Ваша анкета не знайдена. Можливо, ви ще не зареєструвались.")


@dp.message(F.text == 'Для адміністратора')
async def admin_panel(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer('Панель адміністратора', reply_markup=get_admin_inline_keyboard())
    else:
        await message.answer('У вас немає прав адміністратора')

@dp.callback_query(F.data == 'user_list')
async def show_user_list(callback_query: types.CallbackQuery):
    cursor.execute('SELECT user_id, description, price, seminar_link, phone_number, username, full_name FROM users')
    users = cursor.fetchall()

    if users:
        user_list = '\n\n'.join([
            f'ID: {user[0]}\nОпис: {user[1]}\nЦіна: {user[2]}\nПосилання: {user[3]}\n'
            f'Номер телефону: {user[4] if user[4] else "невідомо"}\nТег: @{user[5]}\nІм\'я: {user[6]}'
            for user in users
        ])
        await callback_query.message.answer(f"Список користувачів:\n\n{user_list}")
    else:
        await callback_query.message.answer('Немає зареєстрованих користувачів')
    await callback_query.answer()

@dp.callback_query(F.data == 'add_admin')
async def prompt_add_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Надішліть ID нового адміністратора.')
    await state.set_state('add_admin')
    await callback_query.answer()


from aiogram import F

# Замініть декоратори з state='add_admin' на використання окремого фільтра

@dp.message(F.text, F.state == 'add_admin')
async def add_admin(message: Message, state: FSMContext):
    try:
        new_admin_id = int(message.text)
        ADMIN_IDS.append(new_admin_id)
        await message.answer(f'Користувача з ID {new_admin_id} додано як адміністратора.')
    except ValueError:
        await message.answer('Будь ласка, надішліть коректний числовий ID.')
    await state.clear()



@dp.callback_query(F.data == 'view_user_details')
async def prompt_user_details(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Надішліть тег користувача для перегляду детальної анкети (формат: @username).')
    await state.set_state('view_user')
    await callback_query.answer()

#######

@dp.message(F.text, F.state == 'view_user')
async def view_user_details(message: Message, state: FSMContext):
    username = message.text.lstrip('@')
    cursor.execute(
        'SELECT user_id, description, price, seminar_link, phone_number, username, full_name FROM users WHERE username = ?',
        (username,))
    user = cursor.fetchone()

    if user:
        user_details = (
            f'ID: {user[0]}\nОпис: {user[1]}\nЦіна: {user[2]}\nПосилання: {user[3]}\n'
            f'Номер телефону: {user[4] if user[4] else "невідомо"}\nТег: @{user[5]}\nІм\'я: {user[6]}'
        )
        await message.answer(f"Детальна анкета користувача:\n\n{user_details}")
    else:
        await message.answer('Користувач відсутній. Перевірте правильність введених даних.')
    await state.clear()

@dp.message(F.text == 'Подати інформацію про себе')
async def registration_btn(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Якщо анкета вже є, відправляємо повідомлення про її наявність
        await message.answer(
            "Ваша анкета вже прийнята! Для того, щоб переглянути її, перейдіть у розділ 'Профіль'."
        )
    else:
        # Якщо анкета відсутня, починаємо процес реєстрації
        await message.answer("Надішліть своє фото для реєстрації.")
        await state.set_state(RegistrationStates.photo)

@dp.message(RegistrationStates.photo, F.photo)
async def photo_handler(message: Message, state: FSMContext):
    user_data[message.from_user.id] = {'photo': message.photo[-1].file_id}
    await message.answer("Опишіть себе текстом.")
    await state.set_state(RegistrationStates.description)

@dp.message(RegistrationStates.description)
async def description_handler(message: Message, state: FSMContext):
    user_data[message.from_user.id]['description'] = message.text
    await message.answer('Вкажіть свою ціну в грн.')
    await state.set_state(RegistrationStates.price)

@dp.message(RegistrationStates.price)
async def price_handler(message: Message, state: FSMContext):
    try:
        user_data[message.from_user.id]['price'] = int(message.text)
        await message.answer('Надішліть посилання на онлайн семінар.')
        await state.set_state(RegistrationStates.seminar_link)
    except ValueError:
        await message.answer('Введіть числове значення для ціни.')

@dp.message(RegistrationStates.seminar_link)
async def link_handler(message: Message, state: FSMContext):
    user_data[message.from_user.id]['seminar_link'] = message.text
    user_data[message.from_user.id]['username'] = message.from_user.username
    user_data[message.from_user.id]['full_name'] = message.from_user.full_name
    user_data[message.from_user.id]['phone_number'] = "невідомо"

    cursor.execute(
        '''INSERT INTO users (user_id, username, full_name, phone_number, photo, description, price, seminar_link)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
        message.from_user.id,
        user_data[message.from_user.id]['username'],
        user_data[message.from_user.id]['full_name'],
        user_data[message.from_user.id]['phone_number'],
        user_data[message.from_user.id]['photo'],
        user_data[message.from_user.id]['description'],
        user_data[message.from_user.id]['price'],
        user_data[message.from_user.id]['seminar_link']
    ))
    conn.commit()

    await message.answer('Ваші дані успішно збережено.')
    await state.clear()

@dp.message(F.text == 'Профіль')
async def profile_menu(message: Message):
    await message.answer(
        "Оберіть дію:",
        reply_markup=get_profile_inline_keyboard()
    )

@dp.callback_query(F.data == 'view_own_profile')
async def view_own_profile(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute(
        'SELECT photo, description, price, seminar_link FROM users WHERE user_id = ?',
        (user_id,))
    user = cursor.fetchone()

    if user:
        photo_id, description, price, seminar_link = user
        await callback_query.message.answer_photo(
            photo=photo_id,
            caption="Ось ваша анкета:")
        profile_info = (
            f"Опис: {description}\n"
            f"Ціна: {price} грн\n"
            f"Посилання на семінар: {seminar_link}"
        )
        await callback_query.message.answer(profile_info)
    else:
        await callback_query.message.answer(
            "Ваша анкета не знайдена. Можливо, ви ще не зареєструвались."
        )
    await callback_query.answer()

@dp.callback_query(F.data == 'delete_profile')
async def delete_profile(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute(
        'DELETE FROM users WHERE user_id = ?',
        (user_id,))
    conn.commit()

    await callback_query.message.answer(
        "Вашу анкету успішно видалено. Якщо бажаєте, можете подати анкету в будь-який зручний для вас час."
    )
    await callback_query.answer()

if __name__ == '__main__':
    dp.run_polling(bot)




#
# # bot.py
# import logging
# from aiogram import Bot, Dispatcher
# from config import BOT_TOKEN
# from aiogram.fsm.storage.memory import MemoryStorage
#
# # Ініціалізація бота та логера
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(storage=MemoryStorage())
#
# # Імпортуємо хендлери
# from handlers import admin_handlers, profile_handlers, registration_handlers, general_handlers
#
# # Додаємо роутери
# dp.include_router(admin_handlers.router)
# dp.include_router(profile_handlers.router)
# dp.include_router(registration_handlers.router)
# dp.include_router(general_handlers.router)
#
# if __name__ == '__main__':
#     dp.run_polling(bot)
