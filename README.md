# Ghost AI Core — автономный PR-ИИ-агент

**Новость живёт всего 3 часа? Продли жизнь инфоповодам с помощью ИИ!**

Этот проект разработан в рамках конкурса МПИТ.

### Описание
Цифровое эхо бренда: агент автоматически парсит статью по ссылке, извлекает факты/цитаты/цифры, генерирует посты в разных стилях (Telegram — коротко, VK — дружелюбно с эмодзи, бизнес-блог — профессионально), создаёт креативные изображения (Kandinsky/Stable Diffusion) и планирует публикации по таймингу.

### Функционал
- Парсинг статей (BeautifulSoup + Selenium)
- LLM (YandexGPT / GigaChat / Ollama)
- Генерация постов с разными TONами
- Медиаплан с таймингом (сразу / +3ч / утро)
- Автопостинг в Telegram и VK
- Генерация изображений

### Структура
- `/frontend` — React + Vite + TailwindCSS
- `/backend` — FastAPI с Dockerfile

### Как запустить локально
**Backend:**
```bash
cd backend
cp .env.example .env  # заполни ключи API
docker build -t ghost-ai-backend .
docker run -d -p 8000:8000 --env-file .env ghost-ai-backend
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
