# =======================================Location ======================================================================
import math
import httpx

# Har bir joy: (nomi, latitude, longitude)
BRANCHES = [
    ("Filial 1 - Yunusobod", 41.3525, 69.2412),
    ("Filial 2 - Chilonzor", 41.2853, 69.2034),
    ("Filial 3 - Sergeli", 41.2302, 69.2020),
    ("Filial 4 - Yakkasaroy", 41.2973, 69.2635),
]


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Yer radiusi
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # km

def find_nearest_branch(user_lat, user_lon):
    nearest = None
    min_distance = float('inf')

    for name, lat, lon in BRANCHES:
        distance = calculate_distance(user_lat, user_lon, lat, lon)
        if distance < min_distance:
            min_distance = distance
            nearest = (name, lat, lon, distance)

    return nearest



async def get_address_from_location(lat: float, lon: float) -> str:
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 18,
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "YourBotName/1.0"  # kerakli bo‘lgan Nominatim talabi
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("display_name", "Manzil topilmadi")
    else:
        return "🌐 Geolokatsiya aniqlanmadi"



# =======================================BACK ==========================================================================
from aiogram.fsm.context import FSMContext

async def set_state_with_history(state: FSMContext, new_state):
    data = await state.get_data()
    history = data.get("state_history", [])
    current = await state.get_state()

    if current and (not history or history[-1] != current):
        history.append(current)

    await state.update_data(state_history=history)
    await state.set_state(new_state)
# ======================================================================================================================

