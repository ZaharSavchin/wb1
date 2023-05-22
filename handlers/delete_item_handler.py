from services.search_function import DeleteCallbackFactory
from aiogram import Router
from aiogram.types import CallbackQuery
from database.database import users_items, save_users_items


router = Router()


@router.callback_query(DeleteCallbackFactory.filter())
async def delete_press(callback: CallbackQuery,
                       callback_data: DeleteCallbackFactory):
    user_id = callback.from_user.id
    item_id = callback_data.item_id
    items = users_items.copy()[user_id][1:]
    for item in items:
        if item_id in item:
            users_items[user_id].remove(item)
    await callback.message.edit_text(text='товар удален')
    await callback.answer()
    await save_users_items()



