# QA v1.1 Feedback Smoke — Frontend

**Date (UTC):** 2026-02-23  
**QA:** subagent `qa-cz-v1.1-answer-feedback-smoke`  
**Scope:** Проверка фиксов v1.1: immediate feedback, показ правильного ответа, блокировка перехода без ответа, счетчик correct/total, completion flow (topic=10, ticket=all), экран итогов, регрессия random-one и темы.

## Environment

- Frontend: `projects/czech_realities/frontend`
- API base: `https://czechrealities.cz/api` (`VITE_USE_MOCK=false`)
- Browser automation in this session: **unavailable** (OpenClaw browser control service недоступен), поэтому выполнен кодовый + API smoke.

## Pre-check (API)

Проверено через live API:

- `GET /topic/` → **200**, `len=30`
- `GET /question/by-topic/{id}` (topic id=1) → **200**, `len=10`
- `GET /question/random-one` → **200**, объект вопроса
- `GET /question/random-ticket` → **200**, `len=30`
- В ответах `answers[]` присутствует `is_correct` (данные для feedback доступны на уровне API)

---

## Smoke results (v1.1)

### 1) Immediate feedback (correct/incorrect)
- **Expected:** после выбора ответа сразу показывается корректно/некорректно.
- **Actual:** в `src/App.tsx` выбор ответа только выставляет `selectedOption`; логика проверки `isCorrect`/`correct` в UI отсутствует.
- **Result:** ❌ **FAIL**

### 2) Показ правильного ответа
- **Expected:** после ответа отображается правильный вариант.
- **Actual:** UI не использует `option.isCorrect`/`option.correct`; подсветки/лейбла правильного ответа нет.
- **Result:** ❌ **FAIL**

### 3) Блокировка перехода без ответа
- **Expected:** нельзя перейти к следующему вопросу, если ответ не выбран.
- **Actual:** кнопка `Další otázka` disabled только при `isLoading`; при `selectedOption=null` переход разрешён.
- **Result:** ❌ **FAIL**

### 4) Счетчик correct/total
- **Expected:** отображается прогресс и число верных (например `3/10`, `correct/total`).
- **Actual:** состояния для score/progress в `App.tsx` отсутствуют.
- **Result:** ❌ **FAIL**

### 5) Completion flow: topic=10 вопросов
- **Expected:** тема проходит фиксированный набор (10), затем завершение.
- **Actual:** API отдаёт 10 вопросов по теме (OK), но во frontend после конца очереди вызывается повторный `getQuestionsByTopic(...)` и цикл начинается заново; состояния завершения нет.
- **Result:** ❌ **FAIL**

### 6) Completion flow: ticket=все вопросы
- **Expected:** ticket проходит все вопросы билета и завершает сессию.
- **Actual:** API ticket возвращает 30 вопросов (OK), но после последнего вопроса frontend снова вызывает `getRandomTicket()` и перезапускает поток; завершения нет.
- **Result:** ❌ **FAIL**

### 7) Экран итогов
- **Expected:** финальный экран с результатами.
- **Actual:** отдельный view/state для результатов отсутствует (`View = 'landing' | 'topics' | 'question'`).
- **Result:** ❌ **FAIL**

### 8) Регрессия random-one
- **Expected:** режим работает как раньше.
- **Actual:** API `/question/random-one` доступен, в `startMode('timed')` и `nextQuestion()` вызывается корректно, вопрос загружается как одиночный queue.
- **Result:** ✅ **PASS** (по коду + API)

### 9) Регрессия темы (classic)
- **Expected:** загрузка тем и вопросов по теме работает.
- **Actual:** `getTopics()` и `getQuestionsByTopic(topic.id)` используются корректно; API отвечает 200.
- **Result:** ✅ **PASS** (по коду + API)

---

## Summary

- **Passed:** 2
- **Failed:** 7
- **Blocked:** 0

Критические фичи v1.1 (feedback/validation/scoring/completion/results) во frontend сейчас **не реализованы** либо не подключены в UI.

## Notes for fix verification (next run)

В повторной проверке после доработок обязательно перепроверить:
1. disable `Další otázka` до выбора ответа;
2. мгновенный статус ответа + подсветка правильного варианта;
3. учет `correct/total` и отображение прогресса;
4. переход на итоговый экран после topic(10) и ticket(все);
5. отсутствие авто-ресета в бесконечный цикл после последнего вопроса.
