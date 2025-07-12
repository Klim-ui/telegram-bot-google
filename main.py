import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import aiosqlite
from gdrive_service import GoogleDriveService
from ai_service import AIService

load_dotenv("config.env")
TOKEN = os.getenv("TELEGRAM_TOKEN")

ALLOWED_USERS = set()  # Будет наполняться из БД
DB_PATH = "users.db"

# Инициализация сервисов
gdrive_service = GoogleDriveService()
ai_service = AIService()

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                tg_id INTEGER UNIQUE,
                name TEXT,
                department TEXT,
                role TEXT
            )
        """)
        await db.commit()
        # Пример: добавим админа (замени на свой Telegram ID)
        await db.execute("INSERT OR IGNORE INTO users (tg_id, name, department, role) VALUES (?, ?, ?, ?)",
                         (123456789, "Admin", "IT", "admin"))
        await db.commit()
        async with db.execute("SELECT tg_id FROM users") as cursor:
            async for row in cursor:
                ALLOWED_USERS.add(row[0])

async def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if not await is_authorized(message.from_user.id):
        await message.answer("⛔️ Нет доступа. Обратитесь к администратору.")
        return
    await message.answer("✅ Привет! Я бот для работы с корпоративными документами.\n\n"
                        "📋 Доступные команды:\n"
                        "/help — список команд\n"
                        "/docs — список документов\n"
                        "/search — поиск по документам\n"
                        "/myid — узнать свой Telegram ID")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    if not await is_authorized(message.from_user.id):
        return
    await message.answer("📋 Команды бота:\n\n"
                        "/start — начать работу\n"
                        "/help — эта справка\n"
                        "/docs — показать список документов\n"
                        "/search — поиск по документам (напиши вопрос)\n"
                        "/myid — узнать свой Telegram ID\n\n"
                        "💡 Просто напиши свой вопрос, и я найду ответ в документах!")

@dp.message(Command("myid"))
async def cmd_myid(message: Message):
    await message.answer(f"Твой Telegram ID: {message.from_user.id}")

@dp.message(Command("docs"))
async def cmd_docs(message: Message):
    if not await is_authorized(message.from_user.id):
        return
    
    try:
        await message.answer("📚 Загружаю список документов...")
        
        documents = gdrive_service.get_documents()
        
        if not documents:
            await message.answer("📭 Документы не найдены. Проверьте настройки Google Drive.")
            return
        
        docs_list = "📚 Доступные документы:\n\n"
        for i, doc in enumerate(documents[:10], 1):  # Показываем первые 10
            docs_list += f"{i}. {doc['name']}\n"
            docs_list += f"   Тип: {doc['mimeType']}\n"
            docs_list += f"   Ссылка: {doc['webViewLink']}\n\n"
        
        if len(documents) > 10:
            docs_list += f"... и еще {len(documents) - 10} документов"
        
        await message.answer(docs_list)
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при загрузке документов: {str(e)}")

@dp.message(Command("search"))
async def cmd_search(message: Message):
    if not await is_authorized(message.from_user.id):
        return
    
    await message.answer("🔍 Напиши свой вопрос, и я найду ответ в документах!\n\n"
                        "Примеры вопросов:\n"
                        "• Как подать заявку на отпуск?\n"
                        "• Какие документы нужны для оформления?\n"
                        "• Где найти шаблон отчета?")

@dp.message()
async def handle_search_query(message: Message):
    """Обработка поисковых запросов"""
    if not await is_authorized(message.from_user.id):
        return
    
    # Игнорируем команды
    if message.text.startswith('/'):
        return
    
    try:
        await message.answer("🔍 Ищу ответ в документах...")
        
        # Получаем документы
        documents = gdrive_service.get_documents()
        
        if not documents:
            await message.answer("📭 Документы не найдены.")
            return
        
        # Загружаем содержимое документов
        docs_with_content = []
        for doc in documents[:5]:  # Ограничиваем количество для производительности
            content = gdrive_service.get_document_content(doc['id'], doc['mimeType'])
            docs_with_content.append({
                'name': doc['name'],
                'content': content,
                'link': doc['webViewLink']
            })
        
        # Ищем ответ с помощью AI
        response = ai_service.search_documents(message.text, docs_with_content)
        
        # Формируем ответ
        answer = f"🤖 Ответ на ваш вопрос:\n\n{response}\n\n"
        answer += "📄 Источники:\n"
        for doc in docs_with_content:
            answer += f"• {doc['name']}: {doc['link']}\n"
        
        await message.answer(answer)
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при поиске: {str(e)}")

async def main():
    await init_db()
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 