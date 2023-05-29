from aiogram import Router, F
from aiogram.types import Message
from services.price_monitor import monitoring
from database.database import users_db, users_items, users_max_items


router = Router()


@router.message(F.text.startswith('bot stat'))
async def stat_message(message: Message):
    if message.text.endswith('start'):
        await message.answer('цикл запущен')
        await monitoring()
    elif message.text.endswith("all"):
        answer = []
        counter = 1
        for i in users_db.copy():
            name = users_db[i][0]
            username = users_db[i][1]
            refs = users_max_items[i]
            if i in users_items:
                cur = users_items[i][0]
                items = users_items[i][1:]
                answer.append(f"{counter}){name}(@{username}, {refs}): {cur}, {items}✅\n")
                counter += 1
            else:
                answer.append(f"{counter}){name}(@{username}, {refs})🤷\n")
                counter += 1

        if len(answer) > 100:
            messages = len(answer) // 100
            counter = 0
            for i in range(messages + 1):
                stat = ''.join(answer[counter: counter + 100])
                counter += 100
                await message.answer(f"{stat}")
        else:
            stat = ''.join(answer)
            await message.answer(f"{stat}")
    else:
        counter = 0
        for i in users_items.copy():
            if len(users_items.copy()[i]) > 1:
                counter += 1
        await message.answer(f"users: {len(users_db)}\nactive users: {counter}")

