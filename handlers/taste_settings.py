from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from keyboards import taste_settings_keyboard, taste_preferences_keyboard, diet_restrictions_keyboard, mood_keyboard
from data.database import save_user_preferences, get_user_preferences

# Словарь для хранения временных данных пользователей
user_temp_data = {}

def register_handlers(app: Client):
    @app.on_message(filters.command("taste_settings"))
    async def taste_settings_command(client: Client, message: Message):
        user_id = str(message.from_user.id)
        
        # Инициализируем временные данные пользователя
        if user_id not in user_temp_data:
            user_temp_data[user_id] = {}
        
        # Загружаем текущие предпочтения пользователя
        current_preferences = get_user_preferences(user_id)
        user_temp_data[user_id] = current_preferences.copy() if current_preferences else {}
        
        await message.reply(
            "Давай настроим твои предпочтения для подбора идеальных блюд!\n\n"
            "Выбери, что ты хочешь настроить:",
            reply_markup=taste_settings_keyboard()
        )
    
    @app.on_callback_query(filters.regex(r"^settings_"))
    async def settings_callback(client: Client, callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        data = callback_query.data
        
        if data == "settings_taste":
            await callback_query.message.edit_text(
                "Выбери свои вкусовые предпочтения (можно выбрать несколько):",
                reply_markup=taste_preferences_keyboard()
            )
        elif data == "settings_diet":
            await callback_query.message.edit_text(
                "Выбери свои диетические ограничения (можно выбрать несколько):",
                reply_markup=diet_restrictions_keyboard()
            )
        elif data == "settings_mood":
            await callback_query.message.edit_text(
                "Выбери своё текущее настроение:",
                reply_markup=mood_keyboard()
            )
        elif data == "settings_done":
            # Сохраняем предпочтения пользователя
            save_user_preferences(user_id, user_temp_data.get(user_id, {}))
            
            await callback_query.message.edit_text(
                "Твои предпочтения сохранены! Теперь ты можешь получить рекомендацию блюда с помощью команды /choice."
            )
    
    @app.on_callback_query(filters.regex(r"^taste_"))
    async def taste_callback(client: Client, callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        data = callback_query.data
        
        if data == "taste_done":
            await callback_query.message.edit_text(
                "Давай настроим твои предпочтения для подбора идеальных блюд!\n\n"
                "Выбери, что ты хочешь настроить:",
                reply_markup=taste_settings_keyboard()
            )
        else:
            # Извлекаем выбранный вкус
            taste = data.split("_")[1]
            
            # Инициализируем список тегов, если его нет
            if "tags" not in user_temp_data.get(user_id, {}):
                user_temp_data[user_id] = user_temp_data.get(user_id, {})
                user_temp_data[user_id]["tags"] = []
            
            # Добавляем или удаляем выбранный вкус
            if taste in user_temp_data[user_id]["tags"]:
                user_temp_data[user_id]["tags"].remove(taste)
                await callback_query.answer(f"Вкус '{taste}' удален из предпочтений")
            else:
                user_temp_data[user_id]["tags"].append(taste)
                await callback_query.answer(f"Вкус '{taste}' добавлен в предпочтения")
    
    @app.on_callback_query(filters.regex(r"^diet_"))
    async def diet_callback(client: Client, callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        data = callback_query.data
        
        if data == "diet_done":
            await callback_query.message.edit_text(
                "Давай настроим твои предпочтения для подбора идеальных блюд!\n\n"
                "Выбери, что ты хочешь настроить:",
                reply_markup=taste_settings_keyboard()
            )
        else:
            # Извлекаем выбранное ограничение
            restriction = data.split("_")[1]
            
            # Инициализируем список ограничений, если его нет
            if "diet_restrictions" not in user_temp_data.get(user_id, {}):
                user_temp_data[user_id] = user_temp_data.get(user_id, {})
                user_temp_data[user_id]["diet_restrictions"] = []
            
            # Если выбрано "без ограничений", очищаем список
            if restriction == "без ограничений":
                user_temp_data[user_id]["diet_restrictions"] = []
                await callback_query.answer("Диетические ограничения сброшены")
            else:
                # Добавляем или удаляем выбранное ограничение
                if restriction in user_temp_data[user_id]["diet_restrictions"]:
                    user_temp_data[user_id]["diet_restrictions"].remove(restriction)
                    await callback_query.answer(f"Ограничение '{restriction}' удалено")
                else:
                    user_temp_data[user_id]["diet_restrictions"].append(restriction)
                    await callback_query.answer(f"Ограничение '{restriction}' добавлено")
    
    @app.on_callback_query(filters.regex(r"^mood_"))
    async def mood_callback(client: Client, callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        data = callback_query.data
        
        if data == "mood_done":
            await callback_query.message.edit_text(
                "Давай настроим твои предпочтения для подбора идеальных блюд!\n\n"
                "Выбери, что ты хочешь настроить:",
                reply_markup=taste_settings_keyboard()
            )
        else:
            # Извлекаем выбранное настроение
            mood = data.split("_")[1]
            
            # Инициализируем список настроений, если его нет
            if "mood" not in user_temp_data.get(user_id, {}):
                user_temp_data[user_id] = user_temp_data.get(user_id, {})
                user_temp_data[user_id]["mood"] = []
            
            # Добавляем или удаляем выбранное настроение
            if mood in user_temp_data[user_id]["mood"]:
                user_temp_data[user_id]["mood"].remove(mood)
                await callback_query.answer(f"Настроение '{mood}' удалено")
            else:
                user_temp_data[user_id]["mood"] = [mood]  # Заменяем список, так как можно выбрать только одно настроение
                await callback_query.answer(f"Настроение установлено: '{mood}'")