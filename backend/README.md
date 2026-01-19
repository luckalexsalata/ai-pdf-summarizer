# PDF Summary AI - Backend

FastAPI backend для завантаження та резюмування PDF документів з використанням OpenAI API.

## Особливості

- ✅ Завантаження PDF файлів (до 50MB)
- ✅ Парсинг PDF з підтримкою тексту, таблиць та зображень (OCR)
- ✅ Генерація резюме через OpenAI API
- ✅ Історія останніх 5 оброблених документів
- ✅ Docker підтримка

## Технології

- **FastAPI** - веб-фреймворк
- **pdfplumber** - парсинг PDF текстів та таблиць
- **pdf2image + pytesseract** - OCR для зображень в PDF
- **OpenAI API** - генерація резюме
- **SQLite** - персистентне зберігання історії документів
- **Docker** - контейнеризація

## Встановлення

### Локальне встановлення

1. Встановіть системні залежності:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-eng

# macOS
brew install poppler tesseract
```

2. Створіть віртуальне середовище:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# або
venv\Scripts\activate  # Windows
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

4. Створіть файл `.env`:
```bash
cp .env.example .env
# Відредагуйте .env та додайте ваш OPENAI_API_KEY
# SAVE_PDF_FILES=true - якщо хочете зберігати PDF файли на диску
```

5. Запустіть сервер:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

1. Створіть файл `.env` в корені проекту:
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

2. Запустіть через docker-compose:
```bash
docker-compose up --build
```

## API Документація

Після запуску сервера, документація доступна за адресою:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

#### `POST /api/v1/upload`
Завантажити PDF файл та отримати резюме.

**Request:**
- `file`: PDF файл (multipart/form-data)

**Response:**
```json
{
  "filename": "document.pdf",
  "summary": "Резюме документа...",
  "uploaded_at": "2024-01-01T12:00:00"
}
```

#### `GET /api/v1/history`
Отримати історію останніх 5 оброблених документів.

**Response:**
```json
[
  {
    "filename": "document.pdf",
    "summary": "Резюме...",
    "uploaded_at": "2024-01-01T12:00:00",
    "file_size_mb": 2.5
  }
]
```

#### `GET /health`
Перевірка стану сервера.

#### `GET /`
Інформація про API та версію.

## Структура проекту

```
backend/
├── main.py                    # Точка входу FastAPI
├── app/
│   ├── api/                   # API layer
│   │   └── routes/
│   │       ├── documents.py   # Документи (upload, history)
│   │       └── health.py      # Health check
│   ├── core/                  # Ядро додатку
│   │   ├── config.py          # Налаштування (з .env)
│   │   └── dependencies.py    # Dependency injection
│   ├── models/                # Database models (domain models)
│   │   └── document.py        # Document model (DB structure)
│   ├── schemas/               # API schemas (DTO - Data Transfer Objects)
│   │   └── documents.py       # SummaryResponse, HistoryItem (API I/O)
│   └── services/              # Бізнес-логіка
│       ├── pdf_parser.py      # Парсинг PDF
│       ├── openai_service.py  # Інтеграція з OpenAI
│       └── storage.py         # Зберігання історії (SQLite)
├── requirements.txt
├── Dockerfile
└── README.md
```

### Архітектура

Проект організований за принципами **Clean Architecture** та **Separation of Concerns**:

- **`app/api/routes/`** - HTTP endpoints, обробка запитів
- **`app/core/`** - Конфігурація та dependency injection
- **`app/models/`** - Доменні моделі (представлення даних з БД)
- **`app/schemas/`** - Pydantic схеми для API (request/response DTO)
- **`app/services/`** - Бізнес-логіка, незалежна від API

### Різниця між Models та Schemas

- **`app/models/`** - внутрішні моделі даних, що представляють структуру БД та доменну логіку
  - Використовуються всередині сервісів
  - Можуть містити додаткову логіку валідації
  - Приклад: `Document` - повна модель з БД (id, file_path, тощо)

- **`app/schemas/`** - моделі для API, що визначають формат запитів/відповідей
  - Використовуються в routes для валідації HTTP запитів/відповідей
  - Можуть бути спрощеними версіями models (без внутрішніх полів)
  - Приклад: `HistoryItem` - тільки те, що потрібно клієнту (без id, file_path)

## Обробка PDF

Парсер підтримує:
1. **Текст** - пряме витягування тексту з PDF
2. **Таблиці** - автоматичне розпізнавання та форматування таблиць
3. **Зображення** - OCR через Tesseract для PDF зі сканованими сторінками

## Налаштування

### Змінні оточення

- `OPENAI_API_KEY` (обов'язково) - API ключ OpenAI
- `OPENAI_MODEL` (опціонально) - модель OpenAI (за замовчуванням: `gpt-4o-mini`)
- `SAVE_PDF_FILES` (опціонально) - зберігати PDF файли на диску (`true`/`false`, за замовчуванням: `false`)

## Зберігання даних

### Система зберігання

- **SQLite база даних** (`documents.db`) - зберігає метадані документів (filename, summary, uploaded_at, file_size_mb)
- **Папка `uploads/`** (опціонально) - зберігає PDF файли, якщо `SAVE_PDF_FILES=true`
- **Персистентність** - дані зберігаються між перезапусками сервера
- **Автоматичне очищення** - старі документи (понад 5) автоматично видаляються

### Що зберігається

1. **Завжди зберігається:**
   - Назва файлу
   - Згенероване резюме
   - Дата завантаження
   - Розмір файлу

2. **Опціонально зберігається:**
   - Оригінальний PDF файл (якщо `SAVE_PDF_FILES=true`)

## Обмеження

- Максимальний розмір файлу: 50MB
- Максимальна кількість сторінок: 100 (рекомендовано)
- Історія: останні 5 документів (зберігаються в SQLite)

## Розробка

Для розробки з автоматичним перезавантаженням:
```bash
uvicorn main:app --reload
```
