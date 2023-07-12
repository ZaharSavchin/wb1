from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from services.search_function import bot
from config_data.config import admin_id
from database.database import commercial_dict, save_commercial_dict, users_db


router = Router()

commercial_messages = {}


class CommercialCallbackFactory(CallbackData, prefix='commercial'):
    commercial_id: int


@router.message(F.text == 'my id')
async def get_id(message: Message):

    user_id = message.from_user.id
    name = users_db[user_id][0]
    username = users_db[user_id][1]

    await message.answer(text=f'Ваш id: {user_id}')
    await bot.send_message(chat_id=admin_id, text=f'id пользователя "{name}", @{username} :')
    await bot.send_message(chat_id=admin_id, text=f'{user_id}')


@router.message(F.text == 'help commercial')
async def test_message(message: Message):
    await message.answer('send commercial (id рекламодателя)\n'
                         '&имя рекламы*\n'
                         '#страны или all\n'
                         '{photo_url}\n'
                         '[url]\n'
                         'текст\n')


@router.message(F.text.startswith('send commercial ('))
async def test_message(message: Message):

    name_ = message.from_user.full_name
    username = message.from_user.username

    commercial_id = int(message.text[message.text.find("(")+1: message.text.find(")")])
    c_username = f'@{users_db[commercial_id][1]}'
    c_fullname = users_db[commercial_id][0]
    photo_url = "none"
    countries = message.text[message.text.find("#")+1: message.text.find("{")]
    if "{" in message.text and "}" in message.text:
        photo_url = message.text[message.text.find("{")+1: message.text.find("}")]
    commercial_url = message.text[message.text.find("[")+1: message.text.find("]")]
    name = message.text[message.text.find("&")+1: message.text.find("*")]

    closing_index = message.text.find(']')
    clear_message = message.text[closing_index + 1:]

    if message.from_user.id == admin_id:

        commercial_dict[commercial_id] = {'name': [name, c_username, c_fullname],
                                          'image_url': photo_url,
                                          'commercial_url': commercial_url,
                                          'countries': countries,
                                          'message': clear_message,
                                          'sent_messages': 0,
                                          'users_go_on_url': 0}

        await save_commercial_dict()

        await message.answer(text=f'id рекламодателя: {commercial_id}')
        await message.answer(text=f'имя рекламодателя: {commercial_dict[commercial_id]["name"]}')
        await message.answer(text=f'url рекламодателя: {commercial_dict[commercial_id]["commercial_url"]}')
        if countries == 'all':
            await message.answer(text=f'страны: все')
        if countries != 'all':
            await message.answer(text=f'страны: {countries}')

        button = InlineKeyboardButton(text=f"разослать",
                                      callback_data=CommercialCallbackFactory(commercial_id=commercial_id).pack())
        markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

        if photo_url != "none":

            await message.answer_photo(photo=commercial_dict[commercial_id]["image_url"],
                                       caption=commercial_dict[commercial_id]["message"],
                                       reply_markup=markup)

        elif photo_url == "none":
            await message.answer(text=commercial_dict[commercial_id]["message"], reply_markup=markup)

    else:

        await message.answer(text="У вас нет прав администратора")
        await bot.send_message(chat_id=admin_id, text=f'⚠️пользователь {name_}, @{username} пытался отправить рекламу⚠️')
    print(commercial_dict)
