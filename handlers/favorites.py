from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from data.database import get_favorites, load_dishes

def register_handlers(app: Client):
    @app.on_message(filters.command("favorites"))
    async def favorites_command(client: Client, message: Message):
        user_id = str(message.from_user.id)
        
        # Получаем список избранных блюд пользователя
        favorite_ids = get_favorites(user_id)
        
        if not favorite_ids:
            await message.reply(
                "У тебя пока нет избранных блюд. "
                "Используй команду /choice, чтобы получить рекомендацию, "
                "и добавь понравившееся блюдо в избранное."
            )
            return
        
        # Загружаем все блюда
        all_dishes = load_dishes()
        
        # Фильтруем только избранные блюда
        favorite_dishes = [dish for dish in all_dishes if dish["id"] in favorite_ids]
        
        if not favorite_dishes:
            await message.reply(
                "К сожалению, не удалось найти твои избранные блюда. "
                "Попробуй добавить новые блюда в избранное."
            )
            return
        
        # Отправляем список избранных блюд
        await message.reply("Твои избранные блюда:")