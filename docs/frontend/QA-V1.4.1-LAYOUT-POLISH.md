# QA Report — v1.4.1 Layout Polish

Date (UTC): 2026-02-24  
Scope:
- a) desktop page should not stretch unnaturally
- b) Telegram block without empty white zone; correct on mobile/desktop
- c) Q/A with different image sizes should render correctly
- d) no regressions in navigation and answer flow

## Environment
- Project: `projects/czech_realities/frontend`
- Build: `npm run build` (success)
- Preview: `vite preview --host 127.0.0.1 --port 4173`
- QA runner: Playwright script `frontend/qa-v1.4.1-layout-polish.mjs`
- Result JSON: `frontend/qa-v1.4.1-layout-results.json`
- Screenshots:
  - `frontend/qa-v1.4.1-desktop.png`
  - `frontend/qa-v1.4.1-mobile.png`

## Test results

### a) Desktop page stretch
**Status: FAIL**

Observed on desktop viewport 1440x900:
- `.container` width = **1360px**
- expected cap from CSS intent = **<= 980px**
- horizontal overflow: none

Conclusion: page content still stretches across desktop more than expected (unnatural wide layout remains).

---

### b) Telegram block (no empty white zone, mobile/desktop)
**Status: PASS**

Checks on desktop + mobile:
- `.telegram-card` no longer contains QR image element (`img` absent)
- CTA link is present and visible
- no extra white empty area detected in card (`telegramWhiteGapApprox = 0`)
- no horizontal overflow

Conclusion: Telegram block is clean and visually compact on both breakpoints.

---

### c) Q/A with different image sizes
**Status: PASS**

Scenario with wide/tall/square answer images:
- 4 options rendered
- no card overlap
- all cards inside grid bounds
- no horizontal overflow
- images render consistently in fixed media frames (uniform displayed height by design)

Conclusion: mixed image source dimensions are handled correctly in layout (no breakage/regression).

---

### d) Navigation and answers regression
**Status: PASS**

Validated flow:
- Landing → Start mode → Topic select → Question
- answer selection shows feedback block
- “Další / Zobrazit výsledek” button appears and works
- app stays in question/result flow (no dead-end)

Conclusion: no regression detected in core navigation + answer cycle.

## Overall verdict
- **3/4 checks passed**
- **Blocking issue remains in (a): desktop container still stretched (1360px at 1440 viewport).**

## Recommendation
Fix desktop width constraint for main content container (likely interaction of `.container { width: min(980px, 100%); }` with `flex: 1` in flex parent), then rerun this QA pack.
