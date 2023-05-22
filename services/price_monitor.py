from database.database import users_items, save_users_items
from services.search_function import get_price, main_search
import asyncio


async def monitoring():
    counter = 0
    while True:
        for user_id, list_of_items in users_items.copy().items():
            if len(list_of_items) > 1:
                for item in list_of_items[1:]:
                    for item_id, price in item.items():
                        print(f"{item_id} = {price}")
                        actuat_price = await get_price(list_of_items[0], item_id)
                        actuat_price_float = actuat_price.pop()
                        if actuat_price_float < price:
                            await main_search(list_of_items[0], item_id, user_id)
        print('\n\n')
        print(counter)
        counter += 1
        await asyncio.sleep(120)

