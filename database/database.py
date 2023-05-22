import redis
import json


users_db = {}
users_items = {5754662958: ['byn', {139854535: 74.9}], 1042048167: ['byn', {17420899: 5.95}, {144132397: 50}, {6883909: 37.09}, {14747575: 20.02}]}
url_images: [int, str] = {}

r = redis.Redis(host='127.0.0.1', port=6379, db=5)


def convert_to_int(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (int, float)):
                data[key] = int(value)
            else:
                data[key] = convert_to_int(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = convert_to_int(item)
    elif isinstance(data, (int, float)):
        data = int(data)
    return data


# Получение словаря из Redis
user_dict_json = r.get('users_db')
if user_dict_json is not None:
    users_db = json.loads(user_dict_json)
    users_db = {int(k): v for k, v in users_db.items()}
else:
    users_db = {}


# users_items_dict_json = r.get('users_items')
# if users_items_dict_json is not None:
#     users_items = json.loads(users_items_dict_json)
#     users_items = {int(k): v for k, v in users_items.items()}
#     for k, v in users_items.items():
#         if len(v) > 1:
#             for i in range(1, len(v)):
#                 item = v[i]
#                 updated_item = {int(key): value for key, value in item.items()}
#                 v[i] = updated_item
#
# else:
#     users_items = {}


url_images_dict_json = r.get('url_images')
if url_images_dict_json is not None:
    url_images = json.loads(url_images_dict_json)
    url_images = {int(k): v for k, v in url_images.items()}
else:
    url_images = {}

print(users_items)


async def save_url_images():
    r.set('url_images', json.dumps(url_images))


async def save_users_db():
    r.set('users_db', json.dumps(users_db))


async def save_users_items():
    r.set('users_items', json.dumps(users_items))
