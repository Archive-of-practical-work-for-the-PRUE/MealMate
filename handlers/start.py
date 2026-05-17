from pyrogram import Client, filters
from pyrogram.types import Message

def register_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start_command(client: Client, message: Message):
        await message.reply(
            "Привет! Я MEALMATE, твой персональный помощник в выборе блюд! "
            "Я помогу тебе найти идеальный рецепт, учитывая твои вкусы, "
            "диетические ограничения и даже настроение!\n\n"
            "Чтобы узнать, что я умею, отправь команду /help."
        )