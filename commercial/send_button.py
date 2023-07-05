from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from main_commercial import CommercialCallbackFactory, commercial_dict
from database.database import users_db
from services.search_function import bot
from config_data.config import admin_id


class CommercialUrlFactory(CallbackData, prefix='commercial_url'):
    commercial_id: int


router = Router()


@router.callback_query(CommercialCallbackFactory.filter())
async def send_commercial_pressed(callback: CallbackQuery,
                                  callback_data: CommercialCallbackFactory):
    commercial_id = callback_data.commercial_id
    button = InlineKeyboardButton(text=f"перейти по ссылке",
                                  callback_data=CommercialUrlFactory(commercial_id=commercial_id).pack())
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    if commercial_dict[commercial_id]["image_url"] == "none":
        for user, name_username in users_db.copy().items():
            try:
                await bot.send_message(chat_id=user, text=commercial_dict[commercial_id]["message"], reply_markup=markup)
                commercial_dict[commercial_id]["sent_messages"] += 1
                try:
                    await bot.send_message(chat_id=commercial_id, text=f"{commercial_dict[commercial_id]['sent_messages']}) {name_username[0]}, @{name_username[1]} получил рекламу")
                except Exception:
                    await bot.send_message(chat_id=admin_id, text=f'рекламодатель {commercial_dict[commercial_id]["name"]} недоступен, реклама отправлена {commercial_dict[commercial_id]["sent_messages"]}) {name_username[0]}, @{name_username[1]}')
            except Exception:
                await bot.send_message(chat_id=admin_id, text=f'{name_username[0]}, @{name_username[1]} недоступен')
    else:
        for user, name_username in users_db.copy().items():
            try:
                await bot.send_photo(chat_id=user, photo=commercial_dict[commercial_id]["image_url"], caption=commercial_dict[commercial_id]["message"], reply_markup=markup)
                commercial_dict[commercial_id]["sent_messages"] += 1
                try:
                    await bot.send_message(chat_id=commercial_id,
                                           text=f"{commercial_dict[commercial_id]['sent_messages']}) {name_username[0]}, @{name_username[1]} получил рекламу")
                except Exception:
                    await bot.send_message(chat_id=admin_id,
                                           text=f'рекламодатель {commercial_dict[commercial_id]["name"]} недоступен, реклама отправлена {commercial_dict[commercial_id]["sent_messages"]}) {name_username[0]}, @{name_username[1]}')
            except Exception:
                await bot.send_message(chat_id=admin_id, text=f'{name_username[0]}, @{name_username[1]} недоступен')


