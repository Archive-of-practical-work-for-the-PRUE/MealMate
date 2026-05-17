import os
from pyrogram import Client
from handlers import start, help, taste_settings, choice, favorites

# Проверяем наличие файла .env для загрузки переменных окружения
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Получаем данные для авторизации из переменных окружения
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Создаем экземпляр клиента Pyrogram
app = Client(
    "mealmate_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Регистрируем обработчики команд
start.register_handlers(app)
help.register_handlers(app)
taste_settings.register_handlers(app)
choice.register_handlers(app)
favorites.register_handlers(app)

# Запускаем бота
if __name__ == "__main__":
    print("Бот MealMate запущен!")
    app.run()