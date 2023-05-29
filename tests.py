import asyncio
import aiohttp


users_items = {5754662958: ['byn', {139854535: 74.9}], 1042048167: ['byn', {17420899: 5.95}, {144132397: 33}, {6883909: 37.09}, {14747575: 20.02}]}


items = [144132397, 22078591, 151325062, 152134244, 12816055]


async def get_item(session, currency, item_id):
    url = f'https://card.wb.ru/cards/detail?appType=128&curr={currency}&locale=by&lang=ru&dest=-59208&regions=1,4,22,30,31,33,40,48,66,68,69,70,80,83,114,115&reg=1&spp=0&nm={item_id}'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.by',
        'Referer': 'https://www.wildberries.by/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    async with session.get(url, headers=headers) as response:
        return await response.json()


async def get_price(session, currency, item_id):
    print(item_id)
    async with session:
        response = await get_item(session, currency, item_id)
        item_details = response.get('data', {}).get('products', [])
        if item_details:
            await asyncio.sleep(0.5)
            print(float(item_details[0].get('salePriceU', 0)) / 100)
            return float(item_details[0].get('salePriceU', 0)) / 100
        await asyncio.sleep(0.5)
        return None


async def main():
    async with aiohttp.ClientSession() as session:
        for user_id, list_of_items in users_items.copy().items():
            await asyncio.sleep(0.5)
            if len(list_of_items) > 1:
                for item in list_of_items[1:]:
                    # for item_id, price in item.items():
                    tasks = [get_price(session, list_of_items[0], item_id) for item_id, price in item.items()]
                    prices = await asyncio.gather(*tasks)
                    for item_id, price in zip(items, prices):
                        print(f'{item_id}: {price}')
