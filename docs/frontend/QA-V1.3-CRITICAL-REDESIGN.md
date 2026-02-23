# QA Report — v1.3 CRITICAL REDESIGN

**Project:** Czech Realities (frontend)  
**Date (UTC):** 2026-02-23  
**QA:** subagent `qa-cz-v1.3-critical-fix-redesign`

## Scope requested
Проверка после v1.3:
- а) кейс `question-text + image answers` (верхняя картинка не показывается)
- б) intro-блок на главной присутствует и читаем
- в) все UI тексты на чешском
- г) визуал соответствует warm-beige style
- д) регрессии навигации режимов/ответов/результатов

## Test approach
Из-за недоступности Browser Control Service (OpenClaw browser) проверка выполнена как **code-level QA** по текущему состоянию `frontend/src/App.tsx` и `frontend/src/App.css` + логике клиентов.

---

## Results summary

| Check | Status | Severity |
|---|---|---|
| а) `question-text + image answers`: верхняя картинка | ❌ FAIL | **Critical** |
| б) Intro-блок на главной: присутствует и читаем | ✅ PASS | Minor note |
| в) Все UI тексты на чешском | ⚠️ PARTIAL FAIL | Major |
| г) Визуал соответствует warm-beige style | ❌ FAIL | **Critical** |
| д) Регрессии навигации режимов/ответов/результатов | ✅ PASS (code-flow) | Medium confidence |

---

## Detailed findings

### а) `question-text + image answers` — верхняя картинка
**Status:** ❌ FAIL (Critical)

В `App.tsx` верхняя иллюстрация вопроса рендерится только при условии:

```tsx
{question?.imageUrl && !hasImageOptions && (
  <img src={question.imageUrl} alt="Ilustrace otázky" className="question-image" />
)}
```

Где `hasImageOptions = !!question?.options?.some((opt) => !!opt.imageUrl)`.

Следствие: если у ответа есть изображения (`image answers`), верхняя картинка вопроса **принудительно скрывается**, даже если `question.imageUrl` задан. Это полностью совпадает с reported issue.

---

### б) Intro-блок на главной
**Status:** ✅ PASS

На `view === 'landing'` присутствует `section.intro-panel` с:
- заголовком (`Databanka testových úloh z českých reálií`),
- приветственным абзацем,
- двумя информационными колонками (`intro-grid`).

Тексты структурированы, читаемость на уровне кода хорошая (иерархия `h2/h3 + ul`).

**Note:** присутствуют техничные пункты (`endpoint`, `client`, `Base URL`) — это не мешает читаемости, но влияет на языковую/UX-консистентность.

---

### в) Все UI тексты на чешском
**Status:** ⚠️ PARTIAL FAIL (Major)

Большинство интерфейса на чешском, но есть явные не-чешские элементы:
- `Data source`
- `Base URL`
- badges: `random-one`, `random-ticket`
- runtime labels: `mockClient`, `realApiClient`

Вывод: требование «все UI тексты на чешском» не выполнено полностью.

---

### г) Warm-beige style
**Status:** ❌ FAIL (Critical)

Текущий визуальный язык не warm-beige:
- дефолтная тема — тёмная (`theme` по умолчанию `dark`),
- light theme: сине-фиолетовая гамма (`#e2ebff`, `#eef2ff`, `#4f46e5`),
- акценты/орбы: cyan/purple/green,
- glassmorphism + холодные оттенки.

Это визуально расходится с warm-beige direction.

---

### д) Регрессии навигации режимов/ответов/результатов
**Status:** ✅ PASS (code-flow)

По логике переходов в `App.tsx` критичных регрессий не выявлено:
- Landing → выбор режима (`classic/timed/debate`) корректно
- `classic`: загрузка тем (`topics`) → выбор темы → `question`
- `timed`: `question` с подгрузкой следующего вопроса после ответа
- `debate`: пакет вопросов → итоговый экран `result`
- Back-переходы/смена темы/выход на главную предусмотрены
- Подсчёт результата и `scorePercent` консистентны

**Confidence note:** без browser-e2e это оценка уровня code-path, не пиксель/клик runtime.

---

## Final verdict
Версия v1.3 **не проходит критический QA-гейт** по двум блокирующим критериям:
1. **Critical bug:** скрытие верхнего изображения в кейсе `question-text + image answers`.
2. **Critical mismatch:** визуал не соответствует warm-beige redesign.

Дополнительно:
- языковая локализация UI неполная (Major).

## Recommended release decision
**NO-GO** до устранения critical issues.
