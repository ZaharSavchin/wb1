from aiogram import Router, F
from aiogram.types import Message
from services.price_monitor import monitoring

router = Router()


@router.message(F.text.startswith('bot stat'))
async def stat_message(message: Message):
    if message.text.endswith('start'):
        await monitoring()
