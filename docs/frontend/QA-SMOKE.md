# QA Smoke Report — Frontend

**Project:** `czech_realities`  
**Date (UTC):** 2026-02-23 22:29–22:31  
**Tester:** QA subagent

## Scope
Smoke checks requested:
1. Navigation across 3 modes
2. Question render with image / without image
3. Answer selection
4. Responsive behavior on mobile widths
5. Theme toggle

## Test Environment
- Frontend started locally via Vite:
  - `npm install`
  - `npm run dev -- --host 0.0.0.0 --port 4173`
- URL: `http://localhost:4173/`
- Build under test: current `frontend/src/App.tsx`

## Actual UI Observed
Current app is the default Vite+React template (`Vite + React` header, counter button, logos). Domain features for exam/training flow are not yet implemented in this build.

## Results
| Check | Status | Notes |
|---|---|---|
| Navigation across 3 modes | ❌ FAIL / BLOCKED | No mode navigation UI present. |
| Question render (without image) | ❌ FAIL / BLOCKED | No question component/view present. |
| Question render (with image) | ❌ FAIL / BLOCKED | No question component/view present. |
| Answer selection | ❌ FAIL / BLOCKED | No answers/options UI present. |
| Responsive on mobile widths | ⚠️ N/A for target features | Only template page exists; target user flow absent, cannot validate feature-level responsive behavior. |
| Theme toggle | ❌ FAIL / BLOCKED | No theme switcher/toggle in UI. |

## Blocking Findings
1. Frontend does not yet contain the required product UI for smoke scenarios.
2. `src/App.tsx` is still a starter template.

## Recommendation
Implement MVP screens/components first (3 modes navigation, question card with optional image, answer options, theme toggle). After that, rerun smoke and update this report with pass/fail evidence per scenario and breakpoints (e.g., 375px / 390px / 768px).
