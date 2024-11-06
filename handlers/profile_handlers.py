# handlers/profile_handlers.py
from aiogram import Router, types
from database import get_user, delete_user
import logging
from aiogram import F
from keyboards import get_reply_keyboard, get_profile_inline_keyboard, get_admin_inline_keyboard


router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == 'Профіль')
async def profile_menu(message: types.Message):
    await message.answer("Оберіть дію:", reply_markup=get_profile_inline_keyboard())
    logger.info(f"Profile menu accessed by user {message.from_user.id}")

@router.callback_query(F.data == 'delete_profile')
async def delete_profile(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    delete_user(user_id)
    await callback_query.message.answer("Вашу анкету успішно видалено. Якщо бажаєте, можете подати анкету в будь-який зручний для вас час.")
    logger.info(f"Profile deleted for user {user_id}")
    await callback_query.answer()
