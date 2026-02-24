# Czech Realities Frontend MVP

React + Vite + TypeScript frontend для тренажёра по чешским реалиям.

## Что теперь поддерживается

- 3 рабочих режима с реальным API:
  - **Klasický** → загрузка тем (`/topic/`) + вопросы по теме (`/question/by-topic/{id}`)
  - **Náhodná otázka** → одна случайная (`/question/random-one`)
  - **Náhodný testový lístek** → пакет случайных (`/question/random-ticket`)
- Переключение **mock / real** через env
- Маппинг backend-ответов в frontend domain-модели:
  - `image_url | imageUrl | image_path | imagePath` → `imageUrl`
  - `answers[]` → `options[]`
  - `topic.id | topic_id` → `topicId`

## API client слой

```bash
src/api/
  client.ts      # интерфейс ApiClient
  mockClient.ts  # локальные моки
  realClient.ts  # реальный HTTP client к backend
```

## Переменные окружения

Создай `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Доступные переменные:

- `VITE_API_BASE_URL` — базовый URL backend (например `http://localhost:8000`)
- `VITE_USE_MOCK`:
  - `true` (по умолчанию) — mock client
  - `false` — real API client

### Прод-режим (без моков)

```env
VITE_USE_MOCK=false
VITE_API_BASE_URL=https://your-backend-host
```

## Локальный запуск

```bash
cd frontend
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```
