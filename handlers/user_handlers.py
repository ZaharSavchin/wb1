from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from database.database import users_db, save_users_db, users_items, save_users_items, users_max_items, save_users_max_items
from lexicon.lexicon import LEXICON, LEXICON_CURRENCY
from services.search_function import main_search, get_name
from keyboards.currency_kb import create_currency_keyboard

from config_data.config import Config, load_config
from aiogram import Bot


router = Router()

config: Config = load_config()
BOT_TOKEN = config.tg_bot.token
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


async def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


async def new_user(message):
    await bot.send_message(chat_id=1042048167,
                           text=f'{message.from_user.full_name}, @{message.from_user.username} присоединился')


@router.message(CommandStart())
async def process_start_command(message: Message):
    ref_id = await extract_unique_code(message.text)
    if ref_id is not None and int(ref_id) in users_db and message.from_user.id not in users_db:
        users_max_items[int(ref_id)] += 1
        await save_users_max_items()
        await bot.send_message(chat_id=int(ref_id), text=f"Пользователь @{message.from_user.username} "
                                                         f"присоединился по вашему приглашению!\n"
                                                         f"Теперь у Вас максимальное количество отслеживаемых товаров: "
                                                         f"{users_max_items[int(ref_id)]}")
    if message.from_user.id not in users_max_items:
        users_max_items[message.from_user.id] = 1
        await save_users_max_items()
    if message.from_user.id not in users_db:
        await new_user(message)
    users_db[message.from_user.id] = [message.from_user.full_name, message.from_user.username]
    users_items[message.from_user.id] = ['rub']
    await message.answer(LEXICON["/start"])
    await message.answer('Выберите необходимую валюту для цен товара', reply_markup=create_currency_keyboard(*LEXICON_CURRENCY.keys()))
    await save_users_db()
    await save_users_items()


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    if message.from_user.id not in users_max_items:
        users_max_items[message.from_user.id] = 1
        await save_users_max_items()
    if message.from_user.id not in users_db:
        await new_user(message)
    users_db[message.from_user.id] = [message.from_user.full_name, message.from_user.username]
    await message.answer(LEXICON["/help"])


@router.message(Command(commands='list'))
async def get_list_of_items(message: Message):
    if message.from_user.id not in users_max_items:
        users_max_items[message.from_user.id] = 1
        await save_users_max_items()
    user_id = message.from_user.id
    if user_id not in users_items or len(users_items[user_id]) < 2:
        await message.answer(text="У вас нет отслеживаемых товаров!\n"
                                  "Отправьте боту артикул товара, цену которого хотите отслеживать.")
    else:
        items = users_items.copy()[user_id][1:]
        cur = users_items.copy()[user_id][0]
        keys = []
        for dictionary in items:
            keys.extend(int(key) for key in dictionary.keys())
        for i in keys.copy():
            await main_search(cur, i, user_id)


@router.message(lambda message: isinstance(message.text, str) and re.match(r'^\s*\d+\s*$', message.text))
async def add_item_process(message: Message):
    if message.from_user.id not in users_max_items:
        users_max_items[message.from_user.id] = 1
        await save_users_max_items()
    if message.from_user.id not in users_db:
        await new_user(message)
    users_db[message.from_user.id] = [message.from_user.full_name, message.from_user.username]
    # users_items[message.from_user.id] = []
    if message.from_user.id not in users_items:
        await process_start_command(message)
    else:
        if len(users_items[message.from_user.id]) < users_max_items[message.from_user.id] + 1 \
                or int(message.text) in [element for each_list in [[i for i in k] for k in users_items[message.from_user.id][1:]] for element in each_list]:
            await main_search(users_items[message.from_user.id][0], int(message.text), message.from_user.id)
        else:
            bot_info = await bot.get_me()
            bot_username = bot_info.username
            await message.answer(f"{LEXICON['max_items']}\n\n Чтобы увеличить количество отслеживаемых товаров"
                                 f" пригласите друга!\nПросто отправьте ему это сообщение с вашей реферальной ссылкой:")
            await message.answer(f"Привет!\n"
                                 f"Я хочу поделиться с тобой полезным ботом, который помогает выгодно "
                                 f"покупать на Wildberries (он присылает уведомления, "
                                 f"когда снижается цена на выбранный тобою товар!)\n\n"
                                 f"Чтобы присоединиться просто перейди по ссылке и отправь боту "
                                 f"артикул интересующего тебя товара:\n"
                                 f"https://t.me/{bot_username}?start={message.from_user.id}")
            await message.answer(f"https://t.me/{bot_username}?start={message.from_user.id}")
