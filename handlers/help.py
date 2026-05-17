from pyrogram import Client, filters
from pyrogram.types import Message
from keyboards import help_keyboard

def register_handlers(app: Client):
    @app.on_message(filters.command("help"))
    async def help_command(client: Client, message: Message):
        await message.reply(
            "Вот список доступных команд:\n\n"
            "/start - Запуск бота и приветственное сообщение.\n"
            "/help - Справка по командам бота.\n"
            "/taste_settings - Настройка вкусовых предпочтений, диетических ограничений и текущего настроения.\n"
            "/choice - Получение рекомендации блюда на основе заданных параметров.\n"
            "/favorites - Просмотр списка сохраненных избранных блюд.\n\n"
            "Рекомендую начать с настройки предпочтений с помощью команды /taste_settings.",
            reply_markup=help_keyboard()
        )