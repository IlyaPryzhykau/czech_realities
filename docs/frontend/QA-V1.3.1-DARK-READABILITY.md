# QA Report — v1.3.1 Dark Theme Readability

**Project:** Czech Realities frontend  
**Date (UTC):** 2026-02-23  
**QA focus:**
- readability in **dark theme** for landing intro, cards, topic list
- text contrast in key UI blocks
- regression check for navigation / modes / question flow

---

## Scope & method

1. Code review of `frontend/src/App.tsx` and `frontend/src/App.css`.
2. Build + lint smoke:
   - `npm run build` ✅
   - `npm run lint` ✅
3. Contrast audit for core color pairs (WCAG-based ratio calculations from current CSS variables and fixed colors).

> Note: browser automation service was unavailable in this environment, so final verdict is based on CSS/logic audit + build/lint smoke.

---

## Summary

**Result: FAILED (dark readability)**  
Found multiple contrast/readability issues in dark theme caused by light card backgrounds with light text and non-theme-aware accent blocks.

**Regression status (navigation/modes/question flow): PASS (code-level smoke)**
- No obvious state-flow regressions found in `App.tsx`.
- Landing → modes → topics/question/result transitions remain consistent.
- Classic/timed/debate branching logic is coherent.

---

## Findings

### 1) Landing intro KPI cards: very low contrast in dark theme
- **Area:** `.kpi-card` inside landing intro panel
- **Current CSS:**
  - `.kpi-card` background uses light gradient (`rgba(255,245,237,0.8)` etc.) for all themes
  - text in cards inherits dark-theme text colors (`--text-main: #f8ece4`, `--text-soft: #d1b6ae`)
- **Impact:** dark-theme users get light text on near-light card background (hard to read).
- **Measured ratios (approx):**
  - `#f8ece4` on KPI bg ≈ **1.35:1** ❌
  - `#d1b6ae` on KPI bg ≈ **1.22:1** ❌
  - KPI label `#b47d70` on KPI bg ≈ **2.20:1** ❌

**Severity:** High

---

### 2) Topic list cards: likely unreadable text in dark theme
- **Area:** `.topic-card` in topics view
- **Current CSS:**
  - background is color-mixed with white + translucent white
  - text color forced to `var(--text-main)` (dark theme = very light)
- **Impact:** on bright/saturated card colors in dark mode, light text has poor contrast.
- **Measured ratios against first gradient stop (approx by topic color):**
  - history ≈ **2.27:1** ❌
  - cities ≈ **1.64:1** ❌
  - food ≈ **1.80:1** ❌
  - nature ≈ **1.57:1** ❌

**Severity:** High

---

### 3) Mode badge contrast below threshold
- **Area:** `.badge` on mode cards
- **Current CSS:** fixed text/background tones not adapted for dark palette
- **Measured ratio (approx):** badge text `#9c5f53` on badge background ≈ **2.23:1** ❌

**Severity:** Medium

---

## Blocks checked as acceptable in dark theme

- Base text on standard dark panels (`--text-main` / `--text-soft` over `--card-bg`) — acceptable.
- Ghost buttons and option buttons over dark surfaces — acceptable.
- Answer feedback blocks (`ok`/`bad`) with main text — acceptable contrast.

---

## Navigation / modes / question flow regression check

Checked in `App.tsx` state transitions and mode branches:
- `startMode('classic')` → topics view + load topics ✅
- `startMode('timed'|'debate')` → question view + load content ✅
- `pickTopic(...)` resets session and opens question queue ✅
- answer lock / scoring / next-question behavior preserved ✅
- end-of-session transition to result view preserved ✅
- back actions (`← Zpět`, `Změnit téma`, `Na úvod`) present and coherent ✅

**Status:** No functional regressions detected in audited flow logic.

---

## Recommended fixes (for v1.3.2)

1. Add explicit dark-theme variants for:
   - `.kpi-card`, `.kpi-label`
   - `.topic-card` (either darker background in dark theme, or dark text color per card)
   - `.badge`
2. Keep contrast targets:
   - normal text: **≥ 4.5:1**
   - large/bold text: **≥ 3:1**
3. Re-run visual QA in real browser after style patch.

---

## Final verdict

- **Dark theme readability:** ❌ Not ready (contrast defects in key landing/topics blocks)
- **Navigation/modes/question flow regressions:** ✅ Not found in current code-level smoke
