from database.database import users_items, save_users_items
from services.search_function import get_price, main_search, bot
import asyncio


async def monitoring():
    loop_counter = 0
    while True:
        for user_id, list_of_items in users_items.copy().items():
            if len(list_of_items) > 1:
                for item in list_of_items[1:]:
                    for item_id, price in item.items():
                        actuat_price = await get_price(list_of_items[0], item_id)
                        actuat_price_float = actuat_price.pop()
                        if actuat_price_float < price:
                            await bot.send_message(chat_id=user_id, text=f"цена товара (Артикул: {item_id})"
                                                                         f" снизилась на {round(price - actuat_price_float, 2)} "
                                                                         f"{list_of_items[0]}")
                            await main_search(list_of_items[0], item_id, user_id)
        loop_counter += 1
        if loop_counter % 120 == 0 or loop_counter == 0:
            await bot.send_message(chat_id=1042048167, text=f"{loop_counter}")
        await asyncio.sleep(60)

