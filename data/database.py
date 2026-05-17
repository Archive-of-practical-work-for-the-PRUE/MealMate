import json
import os
from typing import Dict, List, Optional, Any

# Путь к файлу с пользовательскими данными
USER_DATA_FILE = "data/users.json"
# Путь к файлу с блюдами
DISHES_FILE = "data/dishes.json"

# Создаем директорию data, если она не существует
os.makedirs("data", exist_ok=True)

# Функция для загрузки данных пользователей


def load_users() -> Dict[str, Any]:
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Функция для сохранения данных пользователей


def save_users(users: Dict[str, Any]) -> None:
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Функция для загрузки блюд


def load_dishes() -> List[Dict[str, Any]]:
    if os.path.exists(DISHES_FILE):
        with open(DISHES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # Если файл не существует, создаем пример блюд
    sample_dishes = [
        {
            "id": 1,
            "name": "Борщ",
            "description": "Традиционный славянский суп с капустой, свеклой и мясом.",
            "image_url": "https://adygsalt.ru/blog/foto/borsh/3.jpg",
            "recipe_url": "https://example.com/borsch-recipe",
            "order_url": "https://example.com/order-borsch",
            "tags": ["суп", "мясо", "горячее", "русская кухня"],
            "diet_restrictions": ["без глютена"],
            "mood": ["уютный", "традиционный"]
        },
        {
            "id": 2,
            "name": "Греческий салат",
            "description": "Свежий салат с огурцами, помидорами, оливками и сыром фета.",
            "image_url": "https://podacha-blud.com/uploads/posts/2022-12/1670423703_99-podacha-blud-com-p-sir-dlya-grecheskogo-salata-foto-105.jpg",
            "recipe_url": "https://example.com/greek-salad-recipe",
            "order_url": "https://example.com/order-greek-salad",
            "tags": ["салат", "вегетарианское", "холодное", "греческая кухня"],
            "diet_restrictions": ["вегетарианское"],
            "mood": ["легкий", "свежий"]
        },
        {
            "id": 3,
            "name": "Паста Карбонара",
            "description": "Итальянская паста с соусом из яиц, сыра, гуанчиале и черного перца.",
            "image_url": "https://images.squarespace-cdn.com/content/v1/5ecbe0c67be6c04e8f0ef576/1594115419162-RKYMMO5DU0F954BF9C3U/Pasta.png",
            "recipe_url": "https://example.com/carbonara-recipe",
            "order_url": "https://example.com/order-carbonara",
            "tags": ["паста", "горячее", "итальянская кухня"],
            "diet_restrictions": [],
            "mood": ["сытный", "комфортный"]
        }
    ]
    with open(DISHES_FILE, "w", encoding="utf-8") as f:
        json.dump(sample_dishes, f, ensure_ascii=False, indent=4)
    return sample_dishes

# Функция для сохранения блюд


def save_dishes(dishes: List[Dict[str, Any]]) -> None:
    with open(DISHES_FILE, "w", encoding="utf-8") as f:
        json.dump(dishes, f, ensure_ascii=False, indent=4)

# Функция для получения предпочтений пользователя


def get_user_preferences(user_id: str) -> Dict[str, Any]:
    users = load_users()
    return users.get(user_id, {}).get("preferences", {})

# Функция для сохранения предпочтений пользователя


def save_user_preferences(user_id: str, preferences: Dict[str, Any]) -> None:
    users = load_users()
    if user_id not in users:
        users[user_id] = {}
    users[user_id]["preferences"] = preferences
    save_users(users)

# Функция для добавления блюда в избранное


def add_to_favorites(user_id: str, dish_id: int) -> None:
    users = load_users()
    if user_id not in users:
        users[user_id] = {}
    if "favorites" not in users[user_id]:
        users[user_id]["favorites"] = []
    if dish_id not in users[user_id]["favorites"]:
        users[user_id]["favorites"].append(dish_id)
    save_users(users)

# Функция для получения избранных блюд пользователя


def get_favorites(user_id: str) -> List[int]:
    users = load_users()
    return users.get(user_id, {}).get("favorites", [])

# Функция для фильтрации блюд по предпочтениям пользователя


def filter_dishes_by_preferences(preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
    dishes = load_dishes()
    filtered_dishes = []

    # Если предпочтения не заданы, возвращаем все блюда
    if not preferences:
        return dishes

    for dish in dishes:
        # Проверяем соответствие диетическим ограничениям
        if "diet_restrictions" in preferences:
            if not all(restriction in dish["diet_restrictions"] for restriction in preferences["diet_restrictions"]):
                continue

        # Проверяем соответствие настроению
        if "mood" in preferences and preferences["mood"]:
            if not any(mood in dish["mood"] for mood in preferences["mood"]):
                continue

        # Проверяем соответствие тегам (вкусовым предпочтениям)
        if "tags" in preferences and preferences["tags"]:
            if not any(tag in dish["tags"] for tag in preferences["tags"]):
                continue

        filtered_dishes.append(dish)

    return filtered_dishes
