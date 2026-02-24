# QA Report — v1.3.1 Dark Theme Readability (Hotfix)

**Project:** Czech Realities frontend  
**Date (UTC):** 2026-02-23

## What was fixed

1. Improved dark theme readability for landing/intro blocks:
   - updated dark palette variables (`--bg-main`, `--text-main`, `--text-soft`, `--card-bg`, `--card-border`)
   - added dark-specific styles for `.kpi-card` and `.kpi-label`
2. Removed excessive multicolor look in dark mode for topic cards:
   - added dark-specific uniform tone for `.topic-card`
   - kept high-contrast text in dark mode
3. Improved dark-mode badges for better readability:
   - added dark-specific `.badge` colors
4. Light/warm theme styles were not changed (no regression expected for light visuals).

## WCAG AA contrast spot-check (core text)

Calculated contrast ratios for key dark pairs:

- `#f2f5fb` on `#1f2433` → **14.16:1** ✅
- `#d2d9e7` on `#1f2433` → **10.91:1** ✅
- `#f2f5fb` on `#1d2331` → **14.38:1** ✅
- `#d2d9e7` on `#1d2331` → **11.08:1** ✅
- `#eef3ff` on `#263041` (badge) → **11.95:1** ✅

All checked pairs are above WCAG AA threshold for normal text (4.5:1).

## Build/deploy verification

- `npm run build` ✅
- deployed `frontend/dist` to `/var/www/czechrealities` via rsync ✅

## Notes

- Hotfix scope intentionally limited to dark theme readability and visual consistency.
- Functional logic (`App.tsx`) was not modified in this patch.
