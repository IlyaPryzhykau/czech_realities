# QA Report — v1.4.3 Width Final Fix

Date (UTC): 2026-02-24  
Scope:
- desktop 1440px: content column width is constrained (~860–980px), not edge-to-edge
- mobile layout remains OK
- smoke: Telegram block and question flow are not broken

## Environment
- Project: `projects/czech_realities/frontend`
- Build: `VITE_USE_MOCK=true npm run build` (PASS)
- Preview: `vite preview --host 127.0.0.1 --port 4173`
- QA runner: `frontend/qa-v1.4.3-width-final.mjs`
- Artifacts:
  - `frontend/qa-v1.4.3-results.json`
  - `frontend/qa-v1.4.3-desktop.png`
  - `frontend/qa-v1.4.3-mobile.png`

## Results

### 1) Desktop width constraint @ 1440px
**Status: PASS**

Measured:
- viewport width: **1440px**
- `.container` width: **960px**
- left/right position: **240px / 1200px** (centered)
- check range 860–980px: **PASS**
- edge-to-edge check: **PASS**

Conclusion: content column is clearly constrained and centered; no edge-to-edge stretch on desktop.

---

### 2) Mobile layout
**Status: PASS**

Measured on 390x844:
- container width: **362px**
- document scrollWidth: **390px**
- horizontal overflow: **false**

Conclusion: mobile layout remains stable.

---

### 3) Telegram block smoke
**Status: PASS**

Validated:
- `.telegram-panel` exists
- `.telegram-fallback-link` exists

---

### 4) Question flow smoke
**Status: PASS**

Validated:
- classic mode: topic click + answer feedback visible
- timed mode: answer feedback visible + next/result button visible
- debate mode: answer feedback visible + next/result button visible
- runtime errors: none

## Overall verdict
**PASS (4/4 checks)**

v1.4.3 final width fix is verified: desktop content width is properly constrained (~960px at 1440 viewport), mobile layout is OK, and smoke checks for Telegram block + question flow passed.
