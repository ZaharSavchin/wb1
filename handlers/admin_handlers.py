from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from services.price_monitor import monitoring
from database.database import users_db, users_items, users_max_items
from aiogram.filters.callback_data import CallbackData
from config_data.config import admin_id
from handlers.currency_handlers import bot


router = Router()


@router.message(F.text.startswith('bot stat'))
async def stat_message(message: Message):
    if message.text.endswith('start'):
        await message.answer('цикл запущен')
        await monitoring()
    elif message.text.endswith("all"):
        answer = []
        counter = 1
        country = {'rub': 0, 'byn': 0, 'kzt': 0, 'kgs': 0, 'uzs': 0, 'usd': 0, 'amd': 0}
        for i in users_db.copy():
            name = users_db[i][0]
            username = users_db[i][1]
            refs = users_max_items[i]
            if i in users_items:
                cur = users_items[i][0]
                country[cur] += 1
                items = users_items[i][1:]
                if message.from_user.id == admin_id:
                    answer.append(f"{counter}){name}(@{username}, {i}, {refs}): {cur}, {items}✅\n")
                else:
                    answer.append(f"{counter}){name}, @{username}: {cur}\n")

                counter += 1
            else:
                if message.from_user.id == admin_id:
                    answer.append(f"{counter}){name}(@{username}, {i}, {refs})🤷\n")
                else:
                    answer.append(f"{counter}){name}, @{username}\n")
                counter += 1

        country_message = f'Россия: {country["rub"]}\n' \
                          f'Беларусь: {country["byn"]}\n' \
                          f'Казахстан: {country["kzt"]}\n' \
                          f'Киргизстан: {country["kgs"]}\n' \
                          f'Узбекистан: {country["uzs"]}\n' \
                          f'Армения: {country["amd"]}\n' \
                          f'В долларах США: {country["usd"]}'

        if len(answer) > 50:
            messages = len(answer) // 50
            counter = 0
            for i in range(messages + 1):
                stat = ''.join(answer[counter: counter + 50])
                counter += 50
                await message.answer(f"{stat}")
            await message.answer(f'{country_message}')
        else:
            stat = ''.join(answer)
            await message.answer(f"{stat}")
            await message.answer(f'{country_message}')
    else:
        counter = 0
        for i in users_items.copy():
            if len(users_items.copy()[i][1]) > 0:
                counter += 1
        if message.from_user.id == admin_id:
            await message.answer(f"users: {len(users_db)}\nactive users: {counter}")
        else:
            await message.answer(f"users: {len(users_db)}")


class MaxItemsCallbackFactory(CallbackData, prefix='max_items'):
    user_id: int
    change: str


@router.message(F.text.startswith('bot change max_items'))
async def change_max_items(message: Message):
    i = int(message.text.split()[-1])
    name = users_db[i][0]
    username = users_db[i][1]
    refs = users_max_items[i]
    if i in users_items:
        cur = users_items[i][0]
        items = users_items[i][1:]
        answer = f"{name}(@{username}, {i}, {refs}): {cur}, {items}✅\n"
    else:
        answer = f"{name}(@{username}, {i}, {refs})🤷\n"

    button_plus = InlineKeyboardButton(text='+', callback_data=MaxItemsCallbackFactory(user_id=i, change='+').pack())
    button_minus = InlineKeyboardButton(text='-', callback_data=MaxItemsCallbackFactory(user_id=i, change='-').pack())
    markup = InlineKeyboardMarkup(inline_keyboard=[[button_minus, button_plus]])

    await message.answer(text=answer, reply_markup=markup)


@router.message(F.text.startswith('bot cur'))
async def count_cur(message: Message):
    country = {'rub': 0, 'byn': 0, 'kzt': 0, 'kgs': 0, 'uzs': 0, 'usd': 0, 'amd': 0}
    for i in users_db.copy():
        cur = users_items[i][0]
        country[cur] += 1
    country_message = f'Россия: {country["rub"]}\n' \
                      f'Беларусь: {country["byn"]}\n' \
                      f'Казахстан: {country["kzt"]}\n' \
                      f'Киргизстан: {country["kgs"]}\n' \
                      f'Узбекистан: {country["uzs"]}\n' \
                      f'Армения: {country["amd"]}\n' \
                      f'В долларах США: {country["usd"]}'
    await message.answer(f'{country_message}')


@router.message(F.text == 'bot send ads to users')
async def send_ads(message: Message):
    counter = 0
    for user_id, name in users_db.copy().items():
        name = name[0]
        if "<" in name or ">" in name:
            name = name.replace(">", "&gt;").replace("<", "&lt;")
        try:
            await bot.send_photo(chat_id=user_id,
                                 photo='https://raw.githubusercontent.com/ZaharSavchin/images-/main/IMG_20230807_094759.jpg',
                                 caption=f'Здравствуйте <b>{name}</b>👋\n\n'
                                         f'    Если бот оказался Вам полезен, Вы можете оказать поддержку любой удобной для Вас суммой.\n'
                                         f'    Любая Ваша поддержка помогает боту оставаться бесплатным и без рекламы.\n'
                                         f'🙏Заранее Огромная Благодарность!🙏\n\n'
                                         f'<b>на номер телефона</b> (MTC): +375(29)833-49-64\n\n'
                                         f'<b>на карту:</b> (БелКарт, МИР):\n'
                                         f'номер карты: 9112 3930 4117 4546\n'
                                         f'срок действия: 06/28\n'
                                         f'имя держателя карты: VIRTUAL CARD\n\n'
                                         f'<b>через ЕРИП:</b> Банковские, финансовые услуги -> Банки, НКФО -> Белинвестбанк -> Пополнение счёта -> номер договора: 99oBYN-D85F11\n\n'
                                         f'<b>на QIWI кошелек:</b> +375 29 833 4964\n'
                                         f'http://qiwi.com/p/375298334964', parse_mode='HTML'
                                 )
            counter += 1
        except Exception:
            await bot.send_message(chat_id=admin_id, text=f'{user_id}, {name} недоступен')

    await bot.send_message(chat_id=admin_id, text=f'{counter} сообщений доставлено')

