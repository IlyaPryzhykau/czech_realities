# Czech Realities Frontend MVP

Современный frontend MVP для проекта **Czech Realities** на базе **React + Vite + TypeScript**.

## Что реализовано

- ✅ **Landing** с 3 режимами:
  - Classic
  - Blitz (timed)
  - Debate
- ✅ **Topic picker** (карточки тем)
- ✅ **Question view**:
  - текст вопроса
  - изображение
  - варианты ответа
- ✅ **Mockable API client слой**:
  - интерфейс `ApiClient`
  - текущая реализация: `mockClient`
  - легко заменить на реальный backend
- ✅ **Современный UI**:
  - glass cards
  - soft gradients / glowing orbs
  - аккуратная типографика
  - переключатель **dark/light theme**
- ✅ **Адаптивность под mobile**

## Структура

```bash
frontend/
  src/
    api/
      client.ts       # интерфейс API слоя
      mockClient.ts   # мок-реализация
    types.ts          # общие типы
    App.tsx           # основной UI + экраны
    App.css           # дизайн-система/стили
```

## Запуск локально

```bash
cd frontend
npm install
npm run dev
```

По умолчанию Vite поднимает dev-сервер на `http://localhost:5173`.

## Build

```bash
npm run build
npm run preview
```

## Как подключить реальный backend

1. Реализовать `ApiClient`:
   - `getTopics(mode)`
   - `getNextQuestion(topicId, mode)`
2. Заменить `mockClient` в `src/App.tsx` на ваш real client.

Пример направления:

```ts
// src/api/httpClient.ts
import type { ApiClient } from './client';

export const httpClient: ApiClient = {
  async getTopics(mode) {
    const res = await fetch(`/api/topics?mode=${mode}`);
    return res.json();
  },
  async getNextQuestion(topicId, mode) {
    const res = await fetch(`/api/questions/next?topicId=${topicId}&mode=${mode}`);
    return res.json();
  },
};
```
