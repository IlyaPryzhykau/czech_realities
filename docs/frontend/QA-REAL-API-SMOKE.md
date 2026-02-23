# QA Smoke Report — Frontend + Real API Integration

**Project:** `czech_realities`  
**Date (UTC):** 2026-02-23 22:47–22:49  
**Tester:** QA subagent

## Scope
Smoke after "real API integration" for frontend:
1. Загрузка тем
2. `random-one`
3. `by-topic`
4. `random-ticket`
5. Ответы
6. Изображения
7. Обработка пустых/ошибок

## Test Environment
- Backend: `http://localhost:8010` (`czech_realities_backend`, running)
- Frontend: Vite dev server `http://localhost:4173`
- Branch: `feat/frontend-mvp-modern`

## What was actually tested
### A) Real backend API health (curl / JSON checks)
- `GET /topic/` → **200**, список тем возвращается (30 тем)
- `GET /question/random-one` → **200**, возвращает вопрос + `topic` + `answers`
- `GET /question/by-topic/{id}` → **200**, список вопросов по теме возвращается
- `GET /question/random-ticket` → **200**, возвращает набор вопросов (по одному на тему)
- Ошибочный `topic_id`:
  - `GET /question/by-topic/999999` → **404** (корректная ошибка)

### B) Frontend integration check (code + runtime smoke)
- В `frontend/src/App.tsx` подключен **`mockClient`**, а не real HTTP client:
  - `const api = createApiClient(mockClient);`
- В frontend отсутствуют HTTP вызовы (`fetch/axios`) к backend API.
- Следовательно, UI работает на моках и **не использует** `random-one`, `by-topic`, `random-ticket` реального API.

## Results by requested scenario
| Scenario | Backend API | Frontend (real API path) | Verdict |
|---|---:|---:|---|
| Загрузка тем | ✅ PASS (`/topic/`) | ❌ FAIL (используются моки) | **FAIL (integration gap)** |
| `random-one` | ✅ PASS | ❌ FAIL (не вызывается фронтом) | **FAIL (integration gap)** |
| `by-topic` | ✅ PASS | ❌ FAIL (не вызывается фронтом) | **FAIL (integration gap)** |
| `random-ticket` | ✅ PASS | ❌ FAIL (не вызывается фронтом) | **FAIL (integration gap)** |
| Ответы | ✅ PASS (в ответах есть `answers[]`) | ⚠️ Частично (рендерит только мок-структуру) | **PARTIAL** |
| Изображения | ✅ PASS (в БД есть вопросы с `image_url != null`) | ⚠️ Частично (рендер зависит от моков; нет проверки real API изображений) | **PARTIAL** |
| Пустые/ошибки | ✅ PASS для 404 (`by-topic/999999`) | ❌ FAIL (в UI нет явной обработки API errors/empty-state для real API) | **FAIL** |

## Key findings
1. **Критический блокер:** реальная интеграция frontend↔backend не подключена в текущем состоянии ветки.
2. Backend endpoints для требуемых сценариев работают и отдают валидные данные.
3. Smoke «после интеграции real API» по фронту сейчас не может быть зачтен, т.к. фронт работает через `mockClient`.

## Recommendation
1. Реализовать `httpClient` (или аналог) в `frontend/src/api/` с вызовами:
   - `/topic/`
   - `/question/random-one`
   - `/question/by-topic/{topic_id}`
   - `/question/random-ticket`
2. Переключить App на real client вместо `mockClient`.
3. Добавить в UI явные состояния:
   - loading
   - empty list / no questions
   - error (network/5xx/404) с retry.
4. После переключения на real API — повторить smoke и обновить этот отчет со скрин/лог-доказательствами.

## Evidence (commands run)
- `curl -sS http://localhost:8010/topic/`
- `curl -sS http://localhost:8010/question/random-one`
- `curl -sS http://localhost:8010/question/by-topic/1`
- `curl -sS http://localhost:8010/question/random-ticket`
- `curl -sS -o /dev/null -w "%{http_code}" http://localhost:8010/question/by-topic/999999`
- Frontend code inspection: `frontend/src/App.tsx`, `frontend/src/api/client.ts`, `frontend/src/api/mockClient.ts`
