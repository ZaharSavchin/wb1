from aiogram import Router
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from commercial.send_button import CommercialUrlFactory
from commercial.main_commercial import commercial_dict
from services.search_function import bot
from config_data.config import admin_id


router = Router()


@router.callback_query(CommercialUrlFactory.filter())
async def url_button(callback: CallbackQuery,
                     callback_data: CommercialUrlFactory):
    print("обработчик")
    commercial_id = callback_data.commercial_id
    # commercial_url = commercial_dict[commercial_id]["commercial_url"]
    await callback.answer()
    commercial_dict[commercial_id]["users_go_on_url"] += 1
    name = callback.from_user.full_name
    username = callback.from_user.username
    go_on_url = commercial_dict[commercial_id]["users_go_on_url"]
    try:
        await bot.send_message(chat_id=commercial_id, text=f'{go_on_url}) {name}, @{username} перешел по ссылке')
    except Exception:
        await bot.send_message(chat_id=admin_id, text=f'{go_on_url}) {name}, @{username} перешел по ссылке от рекламодателя {commercial_dict[commercial_id]["name"]}')