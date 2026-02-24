import { chromium, devices } from 'playwright';

const baseURL = 'http://127.0.0.1:4173';
const botLinkPattern = /t\.me\/CZECH_REALITIES_BOT|@CZECH_REALITIES_BOT/i;

const svg = (w, h, color, text) =>
  `data:image/svg+xml;utf8,${encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='${w}' height='${h}'><rect width='100%' height='100%' fill='${color}'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-size='48' fill='white'>${text}</text></svg>`)}`;

const questionPayload = {
  id: 101,
  topic_id: 1,
  text: 'Test otázka s různými poměry obrázků',
  image_url: svg(1200, 260, '#555', 'Q-wide'),
  answers: [
    { id: 1, text: '', image_url: svg(1200, 300, '#0ea5e9', 'wide'), is_correct: false },
    { id: 2, text: '', image_url: svg(300, 1200, '#f97316', 'tall'), is_correct: true },
    { id: 3, text: 'Text + square', image_url: svg(600, 600, '#22c55e', 'square'), is_correct: false },
    { id: 4, text: 'Bez obrázku', is_correct: false },
  ],
};

async function setupApiRoutes(page) {
  await page.route('**/topic/', async (route) => {
    await route.fulfill({ json: [{ id: 1, name: 'QA Topic' }] });
  });
  await page.route('**/question/by-topic/**', async (route) => {
    await route.fulfill({ json: [questionPayload] });
  });
  await page.route('**/question/random-one', async (route) => {
    await route.fulfill({ json: questionPayload });
  });
  await page.route('**/question/random-ticket', async (route) => {
    await route.fulfill({ json: [questionPayload, questionPayload, questionPayload, questionPayload] });
  });
}

async function dismissCookie(page) {
  const banner = page.locator('.cookie-banner');
  if (await banner.isVisible().catch(() => false)) {
    await page.getByRole('button', { name: /необходимые|nezbytné|necessary/i }).click();
  }
}

async function runViewport(browser, mobile = false) {
  const context = await browser.newContext(
    mobile ? { ...devices['iPhone 13'] } : { viewport: { width: 1440, height: 900 } },
  );
  const page = await context.newPage();

  await setupApiRoutes(page);
  await page.goto(baseURL, { waitUntil: 'networkidle' });
  await dismissCookie(page);

  // QR checks normal state
  const qrImageVisible = await page.locator('.telegram-card img').isVisible().catch(() => false);
  const fallbackLinkVisibleNormal = await page.getByRole('link', { name: botLinkPattern }).isVisible().catch(() => false);

  // QR fallback check with broken image
  await page.route('**/telegram-bot-qr.jpg**', (route) => route.abort());
  await page.reload({ waitUntil: 'networkidle' });
  await dismissCookie(page);
  const qrImageAfterBlock = await page.locator('.telegram-card img').isVisible().catch(() => false);
  const qrImageLoadedAfterBlock = await page
    .locator('.telegram-card img')
    .evaluate((img) => img.complete && img.naturalWidth > 0)
    .catch(() => false);
  const fallbackLinkVisibleBroken = await page.getByRole('link', { name: botLinkPattern }).isVisible().catch(() => false);

  // Go to classic mode and validate layout + flow
  await page.getByRole('button', { name: 'Spustit režim' }).nth(0).click();
  await page.locator('.topic-card').first().click();
  await page.waitForSelector('.option-btn');

  const layout = await page.evaluate(() => {
    const grid = document.querySelector('.options-grid');
    const cards = [...document.querySelectorAll('.option-btn')];
    const cardRects = cards.map((el) => {
      const r = el.getBoundingClientRect();
      return { x: r.x, y: r.y, w: r.width, h: r.height, right: r.right, bottom: r.bottom };
    });
    const gridRect = grid?.getBoundingClientRect();
    const scrollOverflow = document.documentElement.scrollWidth > window.innerWidth;

    const allInside = gridRect
      ? cardRects.every((r) => r.x >= gridRect.x - 1 && r.right <= gridRect.right + 1)
      : false;

    const overlaps = cardRects.some((a, i) =>
      cardRects.some((b, j) =>
        i !== j && !(a.right <= b.x || b.right <= a.x || a.bottom <= b.y || b.bottom <= a.y),
      ),
    );

    const imageHeights = [...document.querySelectorAll('.option-image')].map((img) =>
      (img).getBoundingClientRect().height,
    );

    return {
      optionCount: cards.length,
      gridCols: getComputedStyle(grid).gridTemplateColumns,
      horizontalOverflow: scrollOverflow,
      allInside,
      overlaps,
      imageHeights,
    };
  });

  // feedback regression: wrong answer -> red feedback + next button; then result exists
  await page.locator('.option-btn').first().click();
  const feedbackBadVisible = await page.locator('.answer-feedback.bad').isVisible().catch(() => false);
  const nextVisible = await page.getByRole('button', { name: /Další|Zobrazit výsledek/i }).isVisible().catch(() => false);
  await page.getByRole('button', { name: /Další|Zobrazit výsledek/i }).click();
  const questionOrResultVisible =
    (await page.locator('.question-panel, .result-panel').first().isVisible().catch(() => false));

  const screenshotPath = mobile ? 'qa-v1.4-mobile.png' : 'qa-v1.4-desktop.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });

  await context.close();

  return {
    viewport: mobile ? 'mobile' : 'desktop',
    qr: {
      qrImageVisible,
      qrImageAfterBlock,
      qrImageLoadedAfterBlock,
      fallbackLinkVisibleNormal,
      fallbackLinkVisibleBroken,
      pass: qrImageVisible || fallbackLinkVisibleNormal,
      passBroken: qrImageLoadedAfterBlock || fallbackLinkVisibleBroken,
    },
    imageLayout: {
      ...layout,
      pass: layout.optionCount >= 4 && !layout.horizontalOverflow && layout.allInside && !layout.overlaps,
    },
    answerFlow: {
      feedbackBadVisible,
      nextVisible,
      questionOrResultVisible,
      pass: feedbackBadVisible && nextVisible && questionOrResultVisible,
    },
  };
}

const browser = await chromium.launch({ headless: true });
const desktop = await runViewport(browser, false);
const mobile = await runViewport(browser, true);
await browser.close();

console.log(JSON.stringify({ desktop, mobile }, null, 2));
