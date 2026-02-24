# QA Report — Legal / Cookie / Footer / QR / Regression

- **Project:** Czech Realities frontend
- **Date (UTC):** 2026-02-23
- **Environment:** local Vite dev (`http://127.0.0.1:4173`)
- **Browsers:** Playwright Chromium
- **Viewports:** Desktop 1440x900, Mobile iPhone 13

## Scope
1. Legal pages are accessible
2. Cookie banner works: closes and remembers choice
3. Footer links work
4. Telegram bot QR block is visible on landing and looks clean on desktop/mobile
5. No regressions in question modes

---

## Test Result Summary

| Area | Result |
|---|---|
| Legal pages accessibility | ✅ PASS |
| Cookie banner (close + persist) | ✅ PASS |
| Footer links | ✅ PASS |
| QR Telegram block on landing | ✅ PASS |
| Desktop/Mobile layout sanity | ✅ PASS |
| Regression in question modes (mock data) | ✅ PASS |
| Regression in question modes (real API in this local env) | ⚠️ BLOCKED by backend availability |

---

## Detailed Checks

### 1) Legal pages available
- Footer contains legal navigation buttons: **Privacy / Terms / Cookies**.
- Clicking each button opens **Legal** section and corresponding content.
- Verified all three legal sections are reachable from landing.

**Status:** ✅ PASS

### 2) Cookie banner behavior
- On first page load banner is shown.
- Clicking "Только необходимые" closes banner.
- After reload banner does **not** reappear (choice persisted in localStorage).

**Status:** ✅ PASS

### 3) Footer links
- Footer exists on landing.
- Footer buttons are clickable and route user to legal content.

**Status:** ✅ PASS

### 4) Telegram QR block (landing)
- Landing page has visible **Telegram bot** block.
- QR image (`telegram-bot-qr.jpg`) is rendered.
- On desktop and mobile block is visible and no horizontal overflow detected.

**Status:** ✅ PASS

### 5) Question modes regression

#### With mock client (`VITE_USE_MOCK=true`)
- Classic mode: starts, topic opens, answer selection works, feedback appears.
- Timed mode: starts, answer selection works, feedback appears.
- Debate mode: starts, answer selection works, feedback appears.

**Status:** ✅ PASS

#### With real API config (`VITE_USE_MOCK=false` in repo `.env`)
- In this local run, modes did not proceed due unavailable questions/topics from backend endpoint.
- This is environmental/backend availability issue in local context, not a confirmed frontend regression.

**Status:** ⚠️ BLOCKED (needs integration check against available backend)

---

## Artifacts
- `frontend/qa-results-mock.json`
- `frontend/qa-results.json`
- `frontend/qa-desktop.png`
- `frontend/qa-mobile.png`

---

## Conclusion
Implementation for **legal/cookie/footer/QR** is working and visually stable on desktop/mobile in local smoke testing. Frontend question-mode regressions were **not found** under mock data. Real-API mode requires backend availability for final integration confirmation.
