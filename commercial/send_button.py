import asyncio

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from commercial.main_commercial import CommercialCallbackFactory, commercial_dict
from database.database import users_db, users_items, save_commercial_dict
from services.search_function import bot
from config_data.config import admin_id


class CommercialUrlFactory(CallbackData, prefix='commercial_url'):
    commercial_id: int


router = Router()


async def send_commercial_stat(answer: list, bot, commercial_id, admin_id):
    message_long = 50
    if len(answer) > message_long:
        messages = len(answer) // message_long
        counter = 0
        for i in range(messages + 1):
            stat = ''.join(answer[counter: counter + message_long])
            counter += message_long
            try:
                await bot.send_message(chat_id=commercial_id, text=f"{stat}")
            except Exception:
                try:
                    await bot.send_message(chat_id=admin_id, text=f"{stat}")
                except Exception as err:
                    await bot.send_message(chat_id=admin_id, text=f"проблемы с отправкой статистики, {err}")
            await asyncio.sleep(1)
    else:
        stat = ''.join(answer)
        try:
            await bot.send_message(chat_id=commercial_id, text=f"{stat}")
        except Exception:
            await bot.send_message(chat_id=admin_id, text=f"{stat}")


@router.callback_query(CommercialCallbackFactory.filter())
async def send_commercial_pressed(callback: CallbackQuery,
                                  callback_data: CommercialCallbackFactory):
    commercial_id = callback_data.commercial_id
    button = InlineKeyboardButton(text=f"перейти по ссылке",
                                  callback_data=CommercialUrlFactory(commercial_id=commercial_id).pack(),
                                  url=commercial_dict[commercial_id]["commercial_url"])

    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    answer = []
    if commercial_dict[commercial_id]["image_url"] == "none":
        for user, name_username in users_db.copy().items():
            users_country = users_items[user][0]
            if users_country in commercial_dict[commercial_id]["countries"] or commercial_dict[commercial_id]["countries"] == 'all':
                try:
                    await bot.send_message(chat_id=user, text=commercial_dict[commercial_id]["message"], reply_markup=markup)
                    commercial_dict[commercial_id]["sent_messages"] += 1
                    answer.append(f"{commercial_dict[commercial_id]['sent_messages']}) {name_username[0]}, @{name_username[1]} получил рекламу\n")
                except Exception:
                    await bot.send_message(chat_id=admin_id, text=f'{name_username[0]}, @{name_username[1]} недоступен')
    else:
        for user, name_username in users_db.copy().items():
            users_country = users_items[user][0]
            if users_country in commercial_dict[commercial_id]["countries"] or commercial_dict[commercial_id]["countries"] == 'all':
                try:
                    await bot.send_photo(chat_id=user, photo=commercial_dict[commercial_id]["image_url"], caption=commercial_dict[commercial_id]["message"], reply_markup=markup)
                    commercial_dict[commercial_id]["sent_messages"] += 1
                    answer.append(f"{commercial_dict[commercial_id]['sent_messages']}) {name_username[0]}, @{name_username[1]} получил рекламу\n")
                except Exception:
                    await bot.send_message(chat_id=admin_id, text=f'{name_username[0]}, @{name_username[1]} недоступен')

    await save_commercial_dict()
    await send_commercial_stat(answer, bot, commercial_id, admin_id)
    await callback.answer()


@router.message(F.text == "check commercial")
async def check_commercial(message: Message):
    await save_commercial_dict()
    if message.from_user.id == admin_id:
        for id_, data in commercial_dict.copy().items():
            await message.answer(f'{id_}\n'
                                 f'Имя: {data["name"]}\n'
                                 f'Ссылка на фото: {data["image_url"]}\n'
                                 f'Ссылка: {data["commercial_url"]}\n'
                                 f'Страны: {data["countries"]}\n'
                                 f'Сообщение:\n{data["message"]}\n'
                                 f'Сообщений отправлено: {data["sent_messages"]}')


@router.message(F.text.startswith('test commercial message'))
async def test_message(message: Message):
    answer = []
    counter = 0
    for id_, name in users_db.copy().items():
        counter += 1
        answer.append(f"{counter}) {name[0]}, @{name[1]} получил рекламу\n")
    await send_commercial_stat(answer, bot, message.from_user.id, admin_id)

