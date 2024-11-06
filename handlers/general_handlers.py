from aiogram import F, types, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import get_reply_keyboard, get_profile_inline_keyboard, get_admin_inline_keyboard
from aiogram.filters import CommandStart, Command



router = Router()

# Головне меню з кнопками
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

@router.message(CommandStart())
async def start_com(message: Message):
    await message.answer(text='Вітаю! Можете подати анкету.', reply_markup=get_reply_keyboard())


@router.message(F.text == 'Про нас')
async def about_us(message: Message):
    await message.answer("Це розділ про нас")

@router.message(F.text == 'Аналітика')
async def analytics(message: Message):
    await message.answer("Розділ Аналітики")

