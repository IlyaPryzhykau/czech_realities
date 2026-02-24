# QA Report — v1.4 Image Layout / QR / Regressions

**Date (UTC):** 2026-02-24  
**Environment:** local frontend (`vite`), Playwright (Chromium, headless)  
**URL:** `http://127.0.0.1:4173`  
**Data mode for image stress-check:** `VITE_USE_MOCK=false` + mocked API routes in Playwright to force mixed image aspect ratios

## Scope
1. Stability of layout for different image sizes (question/options) on **desktop/mobile**.
2. QR block behavior: QR image visible OR fallback bot link shown.
3. No regressions in answer flow / feedback.

---

## Test approach
- Script: `frontend/qa-v1.4-image-layout-qr.mjs`
- Output: `frontend/qa-v1.4-results.json`
- Screenshots:
  - `frontend/qa-v1.4-desktop.png`
  - `frontend/qa-v1.4-mobile.png`

### Image stress dataset (mocked API)
- Question image: ultra-wide.
- Answer options:
  - wide image,
  - tall portrait image,
  - square image + text,
  - text-only option.

This validates that different source image dimensions are normalized in UI and do not break grid flow.

---

## Results summary

### 1) Image layout stability (desktop/mobile)
**Status: PASS ✅**

- Desktop:
  - 4 options rendered, 2-column grid (`gridTemplateColumns`: `669px 669px` in current viewport).
  - No horizontal overflow.
  - All cards inside grid bounds.
  - No overlapping cards.
- Mobile:
  - 4 options rendered, 1-column grid (`316px`).
  - No horizontal overflow.
  - All cards inside grid bounds.
  - No overlaps.
- Option images from very different aspect ratios were visually normalized by CSS (`object-fit: cover`, bounded max-height), grid remained stable.

### 2) QR block: image or fallback link
**Status: PARTIAL / FAIL for fallback path ❌**

- Normal state: QR image is visible (PASS).
- Broken-image simulation (`/telegram-bot-qr.jpg` aborted):
  - image element remains in DOM but **image did not load** (`naturalWidth = 0`),
  - **no fallback link** to bot detected (`@CZECH_REALITIES_BOT` / `t.me/...`).

**Conclusion:** requirement “shows image or fallback bot link” is not fully met for failure scenario.

### 3) Regression: answer flow / feedback
**Status: PASS ✅**

- Selecting wrong answer shows negative feedback block (`.answer-feedback.bad`).
- “Další / Zobrazit výsledek” navigation appears and works.
- Flow continues to next question or result screen without breakage.

---

## Final verdict
- **Image layout (question/options): PASS** on desktop + mobile.
- **Answer flow/feedback regression: PASS.**
- **QR fallback behavior: FAIL** (no fallback bot link when QR image is unavailable).

## Recommendation (for fix)
In Telegram section, add explicit fallback CTA/link rendered when QR fails, e.g.:
- visible text link `https://t.me/CZECH_REALITIES_BOT` (or `@CZECH_REALITIES_BOT`),
- optionally switch on `<img onError>` to show fallback block.
