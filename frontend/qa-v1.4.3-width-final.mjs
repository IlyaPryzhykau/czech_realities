import { chromium } from 'playwright';

const baseURL = 'http://127.0.0.1:4173';

async function dismissCookieIfNeeded(page) {
  const banner = page.locator('.cookie-banner');
  if ((await banner.count()) && (await banner.isVisible())) {
    const necessaryBtn = page.getByRole('button', { name: /Только необходимые|necessary|nezbytné/i });
    if (await necessaryBtn.count()) {
      await necessaryBtn.click();
    }
  }
}

const browser = await chromium.launch({ headless: true });
const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 } });

const results = {
  timestampUtc: new Date().toISOString(),
  checks: {},
};

await desktop.goto(baseURL, { waitUntil: 'networkidle' });
await dismissCookieIfNeeded(desktop);

results.checks.desktopWidth = await desktop.evaluate(() => {
  const container = document.querySelector('.container');
  if (!container) return { ok: false, reason: 'missing .container' };
  const rect = container.getBoundingClientRect();
  const centered = Math.abs(rect.left - (window.innerWidth - rect.width) / 2) < 2;
  const inExpectedRange = rect.width >= 860 && rect.width <= 980;
  const notEdgeToEdge = rect.width < window.innerWidth - 200;
  return {
    ok: centered && inExpectedRange && notEdgeToEdge,
    viewportWidth: window.innerWidth,
    containerWidth: rect.width,
    containerLeft: rect.left,
    containerRight: rect.right,
    centered,
    inExpectedRange,
    notEdgeToEdge,
  };
});

results.checks.telegramBlockSmoke = await desktop.evaluate(() => {
  const panel = document.querySelector('.telegram-panel');
  const link = document.querySelector('.telegram-fallback-link');
  return {
    ok: Boolean(panel && link),
    panelExists: Boolean(panel),
    fallbackLinkExists: Boolean(link),
  };
});

const flow = { classic: {}, timed: {}, debate: {}, errors: [] };
const modeButtons = desktop.getByRole('button', { name: 'Spustit režim' });

try {
  await desktop.goto(baseURL, { waitUntil: 'networkidle' });
  await dismissCookieIfNeeded(desktop);
  await modeButtons.nth(0).click();
  await desktop.locator('.topic-card').first().click({ timeout: 10000 });
  await desktop.locator('.option-btn').first().click({ timeout: 10000 });
  flow.classic = {
    topicCardClick: true,
    answerFeedbackVisible: await desktop.locator('.answer-feedback').isVisible({ timeout: 10000 }),
  };
} catch (e) {
  flow.errors.push(`classic: ${e.message}`);
}

try {
  await desktop.goto(baseURL, { waitUntil: 'networkidle' });
  await dismissCookieIfNeeded(desktop);
  await modeButtons.nth(1).click();
  await desktop.locator('.option-btn').first().click({ timeout: 10000 });
  flow.timed = {
    answerFeedbackVisible: await desktop.locator('.answer-feedback').isVisible({ timeout: 10000 }),
    nextButtonVisible: await desktop.getByRole('button', { name: /Další|Zobrazit výsledek/i }).isVisible(),
  };
} catch (e) {
  flow.errors.push(`timed: ${e.message}`);
}

try {
  await desktop.goto(baseURL, { waitUntil: 'networkidle' });
  await dismissCookieIfNeeded(desktop);
  await modeButtons.nth(2).click();
  await desktop.locator('.option-btn').first().click({ timeout: 10000 });
  flow.debate = {
    answerFeedbackVisible: await desktop.locator('.answer-feedback').isVisible({ timeout: 10000 }),
    nextButtonVisible: await desktop.getByRole('button', { name: /Další|Zobrazit výsledek/i }).isVisible(),
  };
} catch (e) {
  flow.errors.push(`debate: ${e.message}`);
}

results.checks.questionFlowSmoke = {
  ...flow,
  ok:
    Boolean(flow.classic?.answerFeedbackVisible) &&
    Boolean(flow.timed?.answerFeedbackVisible) &&
    Boolean(flow.debate?.answerFeedbackVisible) &&
    flow.errors.length === 0,
};

await desktop.goto(baseURL, { waitUntil: 'networkidle' });
await dismissCookieIfNeeded(desktop);
await desktop.screenshot({ path: 'qa-v1.4.3-desktop.png', fullPage: true });

const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
await mobile.goto(baseURL, { waitUntil: 'networkidle' });
await dismissCookieIfNeeded(mobile);

results.checks.mobileLayout = await mobile.evaluate(() => {
  const container = document.querySelector('.container');
  const rect = container?.getBoundingClientRect();
  const horizontalOverflow = document.documentElement.scrollWidth > window.innerWidth;
  return {
    ok: Boolean(container) && !horizontalOverflow,
    viewportWidth: window.innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    containerWidth: rect?.width ?? null,
    horizontalOverflow,
  };
});

await mobile.screenshot({ path: 'qa-v1.4.3-mobile.png', fullPage: true });

await mobile.close();
await desktop.close();
await browser.close();

console.log(JSON.stringify(results, null, 2));
