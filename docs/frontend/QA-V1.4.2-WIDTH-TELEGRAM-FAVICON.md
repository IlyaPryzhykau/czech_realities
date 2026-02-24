# QA Report — v1.4.2 Width / Telegram / Favicon

Date (UTC): 2026-02-24  
Scope:
- (a) desktop layout no longer edge-to-edge, centered max-width
- (b) Telegram block has no white inner frame/empty area around button
- (c) favicon appears clean in browser tab (no white frame)
- (d) no regressions in mode/theme/question/answer flow

## Environment
- Project: `projects/czech_realities/frontend`
- Build: `npm run build` (PASS)
- Preview: `vite preview --host 127.0.0.1 --port 4173`
- QA runner: `frontend/qa-v1.4.2-width-telegram-favicon.mjs`
- Artifacts:
  - `frontend/qa-v1.4.2-results.json`
  - `frontend/qa-v1.4.2-desktop.png`
  - `frontend/qa-v1.4.2-mobile.png`

## Results by requirement

### (a) Desktop layout max-width + centering
**Status: FAIL**

Observed on 1440x900 viewport:
- measured `.container` width: **1328px**
- left/right margins: **56px / 56px** (centered, but still very wide)
- CSS includes `width: min(860px, 100%)`, but `.container` also has `flex: 1`, which expands element in flex row and effectively breaks intended max-width cap.

Conclusion: layout is centered, but still stretches almost edge-to-edge on desktop. Requirement “centered max-width” is not fully met.

---

### (b) Telegram block without white inner frame/gap
**Status: PASS**

Checks:
- `.telegram-card` wrapper (previous source of white framed empty area) is absent
- CTA button/link is visible and aligned
- no extra white internal block around the button on desktop/mobile screenshots

---

### (c) Favicon without white frame
**Status: PASS**

Checks:
- favicon source: `/favicon.svg` (not default `vite.svg`)
- corner pixel sampling after rasterization: transparent corners (alpha=0), no opaque white border detected

---

### (d) Regressions in mode/theme/question/answer flow
**Status: PASS (functional smoke with mock data)**

Validated:
- classic mode: topic selection works, answering shows feedback
- timed mode: answer feedback + “Další/Зobrazit výsledek” progression works
- debate mode: answer feedback + next progression works
- theme toggle is present and functional visually
- no mobile horizontal overflow detected

Note: repository default `.env` has `VITE_USE_MOCK=false`; for stable frontend regression smoke this QA run used `VITE_USE_MOCK=true` at build time.

## Overall verdict
- **3/4 checks passed**
- **Blocking issue remains in (a)**: desktop content still too wide (1328px on 1440px viewport), so edge-to-edge feel is not fully resolved.

## Recommended fix for (a)
In `.container`, remove or constrain flex growth:
- remove `flex: 1` (preferred for fixed-width centered container), or
- set explicit `max-width: 860px; width: 100%;` and avoid growth in row flex context.

Then rerun this QA pack.