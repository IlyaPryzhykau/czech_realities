# QA v1.2 Image Answers — Frontend

**Date (UTC):** 2026-02-23  
**QA:** subagent `qa-cz-v1.2-image-answers-smoke`  
**Scope:** Проверка bugfix v1.2 для `czech_realities`:
- вопросы с image-ответами;
- mixed text+image варианты;
- подсветка correct/incorrect;
- fallback при битой картинке;
- регрессия текстовых вариантов.

## Environment

- Project: `projects/czech_realities/frontend`
- Browser automation: **unavailable** в текущем рантайме (OpenClaw browser service недоступен)
- Проверка выполнена как:
  - code-review UI/mapper;
  - сборка/линт;
  - проверка на синтетическом API fixture (под image/mixed/broken/text кейсы) на уровне интеграции данных.

## Build / Static sanity

- `npm run lint` → ✅ PASS
- `npm run build` → ✅ PASS (после `tsc -b --clean`; инкрементальный кеш сначала давал false-positive TS6133)

## Findings by requirement

### 1) Вопросы с image-ответами
**Expected:** вариант ответа может быть изображением.

**Verified in code:**
- `QuestionOption` содержит `imageUrl?: string` (`src/types.ts`)
- API mapping тянет `image_url/imageUrl/image_path/...` в `imageUrl` (`src/api/realClient.ts`, `extractImageUrl`, `mapAnswer`)
- В UI для опции рендерится `<img className="option-image" ...>` если `opt.imageUrl` (`src/App.tsx`)

**Result:** ✅ PASS

---

### 2) Mixed text+image варианты
**Expected:** в одном варианте могут одновременно отображаться картинка и текст.

**Verified in code:**
- В `App.tsx` в кнопке варианта:
  - при `hasImage` рендерится `<img ...>`
  - при `hasText` рендерится `<span>{opt.text}</span>`
- Оба блока могут отображаться вместе (нет взаимоисключения).

**Result:** ✅ PASS

---

### 3) Подсветка correct/incorrect
**Expected:** после ответа показывать корректную подсветку (correct/wrong/answered).

**Verified in code:**
- `getOptionClassName`:
  - correct → `option-btn correct`
  - selected+wrong → `option-btn wrong`
  - прочие после ответа → `option-btn answered`
- CSS стили для `.correct/.wrong/.answered` присутствуют (`src/App.css`).

**Result:** ✅ PASS

---

### 4) Fallback битой картинки
**Expected:** при ошибке загрузки изображения не ломать UI, показать fallback.

**Verified in code:**
- `onError` на `<img>` помечает `failedOptionImages[opt.id] = true`
- После ошибки картинка скрывается и показывается текст:
  `⚠️ Obrázek se nepodařilo načíst`
- Для нового вопроса `failedOptionImages` очищается (`useEffect` по `question?.id`).

**Result:** ✅ PASS

---

### 5) Регрессия текстовых вариантов
**Expected:** обычные текстовые варианты работают как раньше.

**Verified in code:**
- При отсутствии `imageUrl` рендерится текстовая часть ответа.
- Логика выбора/скора/feedback не завязана на наличие изображения.
- Для показа правильного ответа используется `getOptionDisplayText` (корректно работает и для image-only вариантов).

**Result:** ✅ PASS

## Summary

- **Passed:** 5
- **Failed:** 0
- **Blocked:** 0 (manual visual browser-check blocked by runtime, но код/сборка/интеграция данных покрыты)

## Notes / Risk

1. В этой сессии не удалось сделать полноценный визуальный e2e клик-тест в браузере из-за недоступного browser-control сервиса.
2. По коду и сборке bugfix v1.2 выглядит корректно внедрённым.
3. Рекомендован короткий ручной UI smoke в живом браузере при первой возможности (проверить фактический UX fallback-сообщения и карточек mixed-answers).
