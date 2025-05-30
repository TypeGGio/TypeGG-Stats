import random

import aiohttp

from config import API_URL
from database.users import get_user

async def get_tgg_user(discordID: str) -> dict:
    user = get_user(discordID)
    url = f"{API_URL}/user/{user['user_id']}/username"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": f"API returned status {response.status}"}

async def get_profile(username: str):
    url = ""

    return {
        "username": "keegan",
        "avatar": "https://media.istockphoto.com/id/1350375018/vector/k-letter-logo-luxury-concept-initial-k-logo-design-golden-monogram-letter-for-company-name.jpg?s=612x612&w=0&k=20&c=-x8Dc_X0ny2nPvoJaxL2NH8F4uDbaOMiyVVi-zdSeU0=",
        "joined": 1736931064,
        "country": "ca",
        "global_ranking": 10,
        "total_pp": 100,
        "highest_wpm": 300,
        "highest_pp": 50,
    }

async def get_top_quotes(username: str, quote_count: int):
    url = ""

    quote_id = 0
    top_quotes = []

    for i in range(quote_count):
        quote_id += 1
        top_quotes.append(
            {
                "quote_id": quote_id,
                "pp": random.randint(100, 1500),
            }
        )

    top_quotes.sort(key=lambda x: x["pp"], reverse=True)

    return top_quotes
