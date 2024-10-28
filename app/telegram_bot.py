import logging

from aiogram import Bot, Dispatcher, filters, types
from aiogram.fsm.storage.memory import MemoryStorage

from app.settings import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


@dp.message(filters.Command('start'))
async def start_command(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    print(f"Пользователь {username} ({chat_id}) начал взаимодействие с ботом.")
    await message.answer(
        f"Приветствую, {username}! "
        f"\nЗдесь ты будешь получать уведомления о новых сообщениях если ты не в сети."
        f"\nТвой telegram_id: {chat_id}, введи его на сайте при регистрации"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    print("Бот запущен. Ожидаю команды...")
    asyncio.run(main())
