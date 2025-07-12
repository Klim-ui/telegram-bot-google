# 🤖 Корпоративный Telegram-бот с ИИ

Интеллектуальный Telegram-бот для работы с корпоративными документами на Google Drive с использованием OpenAI API.

## ✨ Возможности

- 🔐 **Авторизация** по Telegram ID
- 📁 **Интеграция с Google Drive** (Docs, Sheets, PDF)
- 🤖 **ИИ-поиск** по документам через OpenAI
- 🔍 **Семантический поиск** с контекстом
- 📋 **Список документов** с прямыми ссылками
- 🛡️ **Безопасность** - документы не хранятся локально

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/corporate-ai-bot.git
cd corporate-ai-bot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка API ключей

#### Telegram Bot
1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен

#### OpenAI API
1. Зарегистрируйтесь на [OpenAI](https://platform.openai.com/)
2. Получите API ключ

#### Google Drive API
1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Drive API
3. Создайте OAuth 2.0 credentials
4. Скачайте `credentials.json` в корень проекта
5. Создайте папку на Google Drive и получите её ID

### 4. Настройка конфигурации
Создайте файл `config.env`:
```env
TELEGRAM_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id_here
```

### 5. Настройка пользователей
Замените `123456789` в `main.py` на ваш Telegram ID:
```python
await db.execute("INSERT OR IGNORE INTO users (tg_id, name, department, role) VALUES (?, ?, ?, ?)",
                 (YOUR_TELEGRAM_ID, "Admin", "IT", "admin"))
```

### 6. Запуск бота
```bash
python main.py
```

При первом запуске откроется браузер для авторизации в Google Drive.

## 📋 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Начать работу с ботом |
| `/help` | Получить справку |
| `/docs` | Показать список документов |
| `/search` | Начать поиск по документам |
| `/myid` | Узнать свой Telegram ID |
| `/admin` | Админ-панель (только для админов) |
| `/users` | Список пользователей (админы) |

## 💡 Как использовать

1. **Задайте вопрос** боту (например: "Как подать заявку на отпуск?")
2. Бот найдет релевантную информацию в документах Google Drive
3. Получите ответ с ссылками на источники

### Примеры вопросов:
- "Как подать заявку на отпуск?"
- "Какие документы нужны для оформления?"
- "Где найти шаблон отчета?"
- "Как получить доступ к корпоративному Wi-Fi?"

## 📁 Структура проекта

```
corporate-ai-bot/
├── main.py                 # Основной код бота
├── gdrive_service.py       # Работа с Google Drive
├── ai_service.py          # Интеграция с OpenAI
├── config.env             # Конфигурация (не в git)
├── requirements.txt       # Зависимости Python
├── README.md             # Документация
├── demo_documents.md     # Примеры документов
├── .gitignore           # Исключения для git
├── credentials.json     # Google API credentials (не в git)
├── token.pickle         # Google auth token (не в git)
└── users.db            # База пользователей (создается автоматически)
```

## 🔧 Технический стек

- **Python 3.10+** - основной язык
- **aiogram 3.4.1** - Telegram Bot API
- **Google Drive API** - работа с документами
- **OpenAI API** - ИИ-поиск и ответы
- **SQLite** - база пользователей
- **sentence-transformers** - эмбеддинги (для будущего развития)

## 📚 Тестовые документы

Создайте в Google Drive папку с тестовыми документами:
- 📖 Инструкция по работе с ботом
- 👥 HR-регламент
- 📊 Шаблоны отчетов
- ❓ FAQ
- 🔒 Политика безопасности

Примеры документов в `demo_documents.md`

## 🎯 Возможности

✅ **Авторизация** по Telegram ID  
✅ **Разграничение доступа** по отделам  
✅ **Поиск** по документам Google Drive  
✅ **ИИ-ответы** через OpenAI API  
✅ **Админ-панель** для управления пользователями  
✅ **Простой интерфейс**  
✅ **Ссылки на источники**  
✅ **Безопасность** - документы не хранятся локально  

## 🚧 Планы развития

- [ ] Добавить векторную БД для быстрого поиска
- [ ] Улучшить парсинг PDF
- [ ] Добавить логирование
- [ ] Настроить деплой на сервер
- [ ] Веб-интерфейс для администрирования
- [ ] Кэширование для улучшения производительности

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

Если у вас есть вопросы или предложения, создайте [Issue](https://github.com/your-username/corporate-ai-bot/issues) в репозитории.

---

**Создано с ❤️ для автоматизации работы с корпоративными документами** 