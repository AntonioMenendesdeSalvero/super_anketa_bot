from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from database import cursor, conn  # Імпорт підключення до бази даних

# Об'єкт для керування маршрутизацією
router = Router()

# Стан для анкети
class RegistrationStates(StatesGroup):
    photo = State()
    description = State()
    price = State()
    seminar_link = State()

user_data = {}

@router.message(F.text == 'Подати інформацію про себе')
async def registration_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    # Перевірка, чи є анкета користувача в базі
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

@router.message(RegistrationStates.photo, F.photo)
async def photo_handler(message: Message, state: FSMContext):
    user_data[message.from_user.id] = {'photo': message.photo[-1].file_id}
    await message.answer("Опишіть себе текстом.")
    await state.set_state(RegistrationStates.description)

@router.message(RegistrationStates.description)
async def description_handler(message: Message, state: FSMContext):
    user_data[message.from_user.id]['description'] = message.text
    await message.answer('Вкажіть свою ціну в грн.')
    await state.set_state(RegistrationStates.price)

@router.message(RegistrationStates.price)
async def price_handler(message: Message, state: FSMContext):
    try:
        user_data[message.from_user.id]['price'] = int(message.text)
        await message.answer('Надішліть посилання на онлайн семінар.')
        await state.set_state(RegistrationStates.seminar_link)
    except ValueError:
        await message.answer('Введіть числове значення для ціни.')

@router.message(RegistrationStates.seminar_link)
async def seminar_link_handler(message: Message, state: FSMContext):
    user_data[message.from_user.id]['seminar_link'] = message.text
    user_data[message.from_user.id]['username'] = message.from_user.username
    user_data[message.from_user.id]['full_name'] = message.from_user.full_name
    user_data[message.from_user.id]['phone_number'] = "невідомо"

    # Збереження даних до бази
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
        )
    )
    conn.commit()

    await message.answer("Ваші дані успішно збережено.")
    await state.clear()






# # handlers/registration_handlers.py
# from aiogram import Router, types, F
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import Message
# from database import cursor, conn  # Імпорт вашого підключення до бази даних
#
# # Об'єкт для керування маршрутизацією
# router = Router()
#
# # Стан для анкети
# class RegistrationStates(StatesGroup):
#     photo = State()
#     description = State()
#     price = State()
#     seminar_link = State()
#
# user_data = {}
#
# # @router.message(F.text == 'Подати інформацію про себе')
# # async def registration_btn(message: types.Message, state: FSMContext):
# #     user_id = message.from_user.id
# #     if get_user(user_id):
# #         await message.answer("Ваша анкета вже прийнята! Для того, щоб переглянути її, перейдіть у розділ 'Профіль'.")
# #     else:
# #         await message.answer("Надішліть своє фото для реєстрації.")
# #         await state.set_state(RegistrationStates.photo)
# #     logger.info(f"Registration process started by user {user_id}")
# #
# # Додаткові хендлери реєстрації тут
#
# @router.message(RegistrationStates.photo, F.photo)
# async def photo_handler(message: Message, state: FSMContext):
#     user_data[message.from_user.id] = {'photo': message.photo[-1].file_id}
#     await message.answer("Опишіть себе текстом.")
#     await state.set_state(RegistrationStates.description)
#
# @router.message(RegistrationStates.description)
# async def description_handler(message: Message, state: FSMContext):
#     user_data[message.from_user.id]['description'] = message.text
#     await message.answer('Вкажіть свою ціну в грн.')
#     await state.set_state(RegistrationStates.price)
#
# @router.message(RegistrationStates.price)
# async def price_handler(message: Message, state: FSMContext):
#     try:
#         user_data[message.from_user.id]['price'] = int(message.text)
#         await message.answer('Надішліть посилання на онлайн семінар.')
#         await state.set_state(RegistrationStates.seminar_link)
#     except ValueError:
#         await message.answer('Введіть числове значення для ціни.')
#
# @router.message(RegistrationStates.seminar_link)
# async def seminar_link_handler(message: Message, state: FSMContext):
#     user_data[message.from_user.id]['seminar_link'] = message.text
#     user_data[message.from_user.id]['username'] = message.from_user.username
#     user_data[message.from_user.id]['full_name'] = message.from_user.full_name
#     user_data[message.from_user.id]['phone_number'] = "невідомо"
#
#     # Збереження даних до бази
#     cursor.execute(
#         '''INSERT INTO users (user_id, username, full_name, phone_number, photo, description, price, seminar_link)
#            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
#             message.from_user.id,
#             user_data[message.from_user.id]['username'],
#             user_data[message.from_user.id]['full_name'],
#             user_data[message.from_user.id]['phone_number'],
#             user_data[message.from_user.id]['photo'],
#             user_data[message.from_user.id]['description'],
#             user_data[message.from_user.id]['price'],
#             user_data[message.from_user.id]['seminar_link']
#         )
#     )
#     conn.commit()
#
#     await message.answer("Ваші дані успішно збережено.")
#     await state.clear()



# from aiogram import Router, types
# from aiogram.fsm.context import FSMContext
# from database import add_user, get_user
# import logging
# from aiogram import F
# from keyboards import get_reply_keyboard, get_profile_inline_keyboard, get_admin_inline_keyboard
#
#
# router = Router()
# logger = logging.getLogger(__name__)
#
# from aiogram.fsm.state import StatesGroup, State
#
# class RegistrationStates(StatesGroup):
#     photo = State()
#     description = State()
#     price = State()
#     seminar_link = State()
#     phone_number = State()
#
# @router.message(F.text == 'Подати інформацію про себе')
# async def registration_btn(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     if get_user(user_id):
#         await message.answer("Ваша анкета вже прийнята! Для того, щоб переглянути її, перейдіть у розділ 'Профіль'.")
#     else:
#         await message.answer("Надішліть своє фото для реєстрації.")
#         await state.set_state(RegistrationStates.photo)
#     logger.info(f"Registration process started by user {user_id}")

# Додаткові хендлери реєстрації тут
