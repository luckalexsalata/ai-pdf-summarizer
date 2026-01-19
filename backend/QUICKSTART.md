# Швидкий старт (без Docker)

## Покрокова інструкція для локального запуску

### 1. Перевірка системних залежностей

Спочатку встановіть системні бібліотеки для роботи з PDF та OCR:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-eng python3-pip python3-venv
```

**macOS:**
```bash
brew install poppler tesseract
```

**Windows:**
- Завантажте poppler: https://github.com/oschwartz10612/poppler-windows/releases/
- Завантажте tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Додайте їх до PATH

### 2. Перехід у папку backend

```bash
cd backend
```

### 3. Створення віртуального середовища

```bash
# Створити віртуальне середовище
python3 -m venv venv

# Активація (Linux/macOS)
source venv/bin/activate

# Активація (Windows)
# venv\Scripts\activate
```

### 4. Встановлення Python залежностей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Налаштування змінних оточення

Створіть файл `.env` в папці `backend/`:

```bash
# Вручну створити або скопіювати приклад
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
SAVE_PDF_FILES=false
EOF
```

**Важливо:** Замініть `your_openai_api_key_here` на ваш реальний API ключ з OpenAI!

### 6. Запуск сервера

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Перевірка роботи

Відкрийте в браузері:
- **API документація**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## Вирішення проблем

### Помилка "ModuleNotFoundError"
```bash
# Переконайтеся що віртуальне середовище активоване
# та залежності встановлені
pip install -r requirements.txt
```

### Помилка "OPENAI_API_KEY not set"
```bash
# Переконайтеся що файл .env існує та містить OPENAI_API_KEY
cat .env
```

### Помилка "poppler not found" або "tesseract not found"
```bash
# Встановіть системні залежності (див. крок 1)
# Перевірте що вони в PATH:
which pdftoppm  # для poppler
which tesseract  # для tesseract
```

### Помилка "aiosqlite could not be resolved" (лише попередження IDE)
Це нормально - IDE може не бачити пакет, але він працюватиме після встановлення.

## Зупинка сервера

Натисніть `Ctrl+C` в терміналі де запущений сервер.

## Деактивація віртуального середовища

```bash
deactivate
```
