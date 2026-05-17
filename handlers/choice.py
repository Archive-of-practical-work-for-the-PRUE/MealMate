import random
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from data.database import get_user_preferences, filter_dishes_by_preferences, add_to_favorites
from keyboards import dish_action_keyboard

# Словарь для хранения последних рекомендаций пользователей
user_last_recommendations = {}

def register_handlers(app: Client):
    @app.on_message(filters.command("choice"))
    async def choice_command(client: Client, message: Message):
        user_id = str(message.from_user.id)
        
        # Получаем предпочтения пользователя
        preferences = get_user_preferences(user_id)
        
        if not preferences:
            await message.reply(
                "Похоже, ты еще не настроил свои предпочтения. "
                "Используй команду /taste_settings, чтобы указать свои вкусы, "
                "диетические ограничения и настроение."
            )
            return
        
        # Фильтруем блюда по предпочтениям
        filtered_dishes = filter_dishes_by_preferences(preferences)
        
        if not filtered_dishes:
            await message.reply(
                "К сожалению, не удалось найти блюда, соответствующие твоим предпочтениям. "
                "Попробуй изменить настройки с помощью команды /taste_settings."
            )
            return
        
        # Выбираем случайное блюдо из отфильтрованных
        dish = random.choice(filtered_dishes)
        
        # Сохраняем рекомендацию для пользователя
        user_last_recommendations[user_id] = filtered_dishes
        
        # Отправляем информацию о блюде
        await send_dish_info(client, message, dish)
    
    @app.on_callback_query(filters.regex(r"^new_choice$"))
    async def new_choice_callback(client: Client, callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        
        # Проверяем, есть ли сохраненные рекомендации
        if user_id not in user_last_recommendations or not user_last_recommendations[user_id]:
            await callback_query.message.reply(
                "Не удалось найти сохраненные рекомендации. "
                "Используй команду /choice, чтобы получить новую рекомендацию."
            )
            return
        
        # Выбираем случайное блюдо из сохраненных рекомендаций
        dish = random.choice(user_last_recommendations[user_id])
        
        # Отправляем информацию о блюде
        await send_dish_info(client, callback_query.message, dish, is_edit=True)
        
        # Отвечаем на callback_query, чтобы убрать индикатор загрузки
        await callback_query.answer()
    
    @app.on_callback_query(filters.regex(r"^favorite_"))
    async def favorite_callback(client: Client, callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        dish_id = int(callback_query.data.split("_")[1])
        
        # Добавляем блюдо в избранное
        add_to_favorites(user_id, dish_id)
        
        await callback_query.answer("Блюдо добавлено в избранное!")

async def send_dish_info(client, message, dish, is_edit=False):
    # Формируем текст сообщения
    text = f"**{dish['name']}**\n\n{dish['description']}"
    
    # Создаем клавиатуру
    keyboard = dish_action_keyboard(
        dish_id=dish['id'],
        recipe_url=dish['recipe_url'],
        order_url=dish['order_url']
    )
    
    # Отправляем или редактируем сообщение
    if is_edit:
        await message.edit_text(text, reply_markup=keyboard)
    else:
        # Пытаемся отправить фото, если есть URL изображения
        try:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=dish['image_url'],
                caption=text,
                reply_markup=keyboard
            )
        except Exception:
            # Если не удалось отправить фото, отправляем только текст
            await message.reply(text, reply_markup=keyboard)