# QA Report — v1.3.2 Topic Cards Cleanup

**Project:** Czech Realities frontend  
**Date (UTC):** 2026-02-23

## Scope

Проверка требований v1.3.2:

1. Light theme: список тем без rainbow-эффекта.
2. На карточке темы только название (без дублирующей строки описания).
3. Dark theme: читаемость сохранена.
4. Нет регрессий в выборе темы.

## Test Method

- Статический аудит кода (`frontend/src/App.tsx`, `frontend/src/App.css`).
- Проверка сборки и линтинга:
  - `npm run build` ✅
  - `npm run lint` ✅

> Примечание: в окружении QA недоступен встроенный browser-control сервис OpenClaw, поэтому визуальная проверка выполнялась по исходникам и стилям.

## Findings

### 1) Light theme topic list без rainbow — ❌ FAIL

Текущий стиль карточки в light theme использует индивидуальный цвет темы и градиент:

- `frontend/src/App.css:274` — `background: linear-gradient(... var(--topic-color) ...)`
- `frontend/src/App.css:275` — `border: 1px solid color-mix(... var(--topic-color) ...)`
- `frontend/src/App.tsx:318` — `style={{ '--topic-color': topic.color }}`

Это сохраняет multicolor/rainbow-подачу списка тем.

### 2) На карточке только название темы — ❌ FAIL

В карточке темы всё ещё рендерится дополнительная строка описания:

- `frontend/src/App.tsx:324` — `<strong>{topic.title}</strong>`
- `frontend/src/App.tsx:325` — `<p>{topic.description}</p>`

Требование «только название темы» не выполнено.

### 3) Dark theme readability сохранена — ✅ PASS (по коду)

В dark theme для `.topic-card` применяются отдельные фон/бордер/цвет текста:

- `frontend/src/App.css:282-286` — тёмный фон и контрастный текст через `var(--text-main)`.

По кодовой конфигурации читаемость сохранена; прямой визуальный smoke в браузере в этом окружении недоступен.

### 4) Нет регрессий в выборе темы — ✅ PASS (по логике)

Логика выбора темы не затронута:

- `frontend/src/App.tsx:136-150` — `pickTopic(topic)` выставляет `selectedTopic`, грузит вопросы через `api.getQuestionsByTopic(topic.id)`, переводит в `question` view.
- Сигнатуры и переходы состояния корректны, сборка/линт без ошибок.

## Summary

Статус v1.3.2 по заявленным критериям: **2/4 выполнено**.

- ✅ Dark readability сохранена.
- ✅ Регрессий в механике выбора темы не выявлено (по коду).
- ❌ Light theme всё ещё rainbow/multicolor.
- ❌ На карточке темы всё ещё есть вторая строка (description).

## Recommended Fixes

1. Убрать зависимость light-card от `--topic-color` (сделать нейтральный единый фон/бордер).
2. Удалить `<p>{topic.description}</p>` из topic-card (оставить только title).
3. После фикса повторить quick visual smoke (light/dark) + проверку клика по теме.
