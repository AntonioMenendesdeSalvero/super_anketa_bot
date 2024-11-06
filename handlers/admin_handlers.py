# handlers/admin_handlers.py
from aiogram import Router, types
from config import ADMIN_IDS
from database import get_user
import logging
from aiogram import F
from keyboards import get_reply_keyboard, get_profile_inline_keyboard, get_admin_inline_keyboard


router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == 'Для адміністратора')
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer('Панель адміністратора', reply_markup=get_admin_inline_keyboard())
    else:
        await message.answer('У вас немає прав адміністратора')
    logger.info(f"Admin panel accessed by user {message.from_user.id}")

# Додаткові адміністративні хендлери тут
