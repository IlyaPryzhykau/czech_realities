import { chromium, devices } from 'playwright';

const baseURL = 'http://127.0.0.1:4173';

const svgText = (w, h, color, text) =>
  `<svg xmlns='http://www.w3.org/2000/svg' width='${w}' height='${h}'><rect width='100%' height='100%' fill='${color}'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-size='48' fill='white'>${text}</text></svg>`;

const topicPayload = [
  { id: 1, name: 'Dopravní značky' },
  { id: 2, name: 'Pravidla provozu' },
];

const questionPayload = {
  id: 101,
  topic_id: 1,
  text: 'Test otázka s různými poměry obrázků',
  image_url: '/qa-q-wide.svg',
  answers: [
    { id: 1, text: '', image_url: '/qa-a-wide.svg', is_correct: false },
    { id: 2, text: '', image_url: '/qa-b-tall.svg', is_correct: true },
    { id: 3, text: 'Text + square', image_url: '/qa-c-square.svg', is_correct: false },
    { id: 4, text: 'Без картинки', is_correct: false },
  ],
};

async function setupApiRoutes(page) {
  await page.route('**/topic/', async (route) => route.fulfill({ json: topicPayload }));
  await page.route('**/question/by-topic/**', async (route) => route.fulfill({ json: [questionPayload] }));
  await page.route('**/question/random-one', async (route) => route.fulfill({ json: questionPayload }));
  await page.route('**/question/random-ticket', async (route) =>
    route.fulfill({ json: [questionPayload, questionPayload, questionPayload, questionPayload] }),
  );

  const images = {
    'qa-q-wide.svg': svgText(1200, 260, '#555', 'Q-wide'),
    'qa-a-wide.svg': svgText(1200, 280, '#0ea5e9', 'A-wide'),
    'qa-b-tall.svg': svgText(320, 1200, '#f97316', 'B-tall'),
    'qa-c-square.svg': svgText(600, 600, '#22c55e', 'C-square'),
  };

  await page.route('**/qa-*.svg', async (route) => {
    const url = new URL(route.request().url());
    const fileName = url.pathname.split('/').pop() ?? '';
    const body = images[fileName];
    if (!body) {
      await route.abort();
      return;
    }

    await route.fulfill({
      status: 200,
      contentType: 'image/svg+xml',
      body,
    });
  });
}

async function dismissCookie(page) {
  const btn = page.getByRole('button', { name: /необходимые|nezbytné|necessary/i });
  if (await btn.isVisible().catch(() => false)) await btn.click();
}

async function checkLandingLayout(page) {
  return page.evaluate(() => {
    const container = document.querySelector('.container');
    const shell = document.querySelector('.app-shell');
    const panel = document.querySelector('.telegram-panel');
    const card = document.querySelector('.telegram-card');
    const link = document.querySelector('.telegram-card .telegram-fallback-link');

    const c = container?.getBoundingClientRect();
    const s = shell?.getBoundingClientRect();
    const p = panel?.getBoundingClientRect();
    const cr = card?.getBoundingClientRect();
    const lr = link?.getBoundingClientRect();

    const horizontalOverflow = document.documentElement.scrollWidth > window.innerWidth;

    return {
      viewport: { w: window.innerWidth, h: window.innerHeight },
      containerWidth: c?.width ?? null,
      containerMaxExpected: 980,
      shellWidth: s?.width ?? null,
      telegramPanelWidth: p?.width ?? null,
      telegramCardHeight: cr?.height ?? null,
      telegramLinkHeight: lr?.height ?? null,
      telegramWhiteGapApprox: cr && lr ? Math.max(0, cr.height - lr.height - 22) : null,
      telegramHasImage: Boolean(document.querySelector('.telegram-card img')),
      horizontalOverflow,
    };
  });
}

async function checkQuestionLayoutAndFlow(page) {
  await page.getByRole('button', { name: 'Spustit režim' }).first().click();
  await page.locator('.topic-card').first().click();
  await page.waitForSelector('.option-btn');

  const layout = await page.evaluate(() => {
    const grid = document.querySelector('.options-grid');
    const gridRect = grid?.getBoundingClientRect();
    const cards = [...document.querySelectorAll('.option-btn')];
    const cardRects = cards.map((el) => {
      const r = el.getBoundingClientRect();
      return { x: r.x, y: r.y, right: r.right, bottom: r.bottom, w: r.width, h: r.height };
    });

    const allInside =
      !!gridRect && cardRects.every((r) => r.x >= gridRect.x - 1 && r.right <= gridRect.right + 1);

    const overlaps = cardRects.some((a, i) =>
      cardRects.some((b, j) =>
        i !== j && !(a.right <= b.x || b.right <= a.x || a.bottom <= b.y || b.bottom <= a.y),
      ),
    );

    const imageHeights = [...document.querySelectorAll('.option-image')].map((img) =>
      Math.round(img.getBoundingClientRect().height),
    );

    const imageRatios = [...document.querySelectorAll('.option-image')].map((img) => {
      const w = img.getBoundingClientRect().width;
      const h = img.getBoundingClientRect().height;
      return w > 0 ? Number((h / w).toFixed(3)) : null;
    });

    return {
      optionCount: cards.length,
      gridCols: getComputedStyle(grid).gridTemplateColumns,
      allInside,
      overlaps,
      imageHeights,
      imageRatios,
      horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
    };
  });

  await page.locator('.option-btn').first().click();
  const feedbackVisible = await page.locator('.answer-feedback.bad, .answer-feedback.ok').isVisible().catch(() => false);
  const nextBtn = page.getByRole('button', { name: /Další|Zobrazit výsledek/i });
  const nextVisible = await nextBtn.isVisible().catch(() => false);
  if (nextVisible) await nextBtn.click();
  const stayedInFlow = await page.locator('.question-panel, .result-panel').first().isVisible().catch(() => false);

  return {
    layout,
    flow: {
      feedbackVisible,
      nextVisible,
      stayedInFlow,
      pass: feedbackVisible && nextVisible && stayedInFlow,
    },
  };
}

async function runViewport(browser, mobile = false) {
  const context = await browser.newContext(
    mobile ? { ...devices['iPhone 13'] } : { viewport: { width: 1440, height: 900 } },
  );
  const page = await context.newPage();

  await setupApiRoutes(page);
  await page.goto(baseURL, { waitUntil: 'networkidle' });
  await dismissCookie(page);

  const landing = await checkLandingLayout(page);
  const questionAndFlow = await checkQuestionLayoutAndFlow(page);

  const screenshotPath = mobile ? 'qa-v1.4.1-mobile.png' : 'qa-v1.4.1-desktop.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });

  await context.close();

  const desktopStretchPass =
    landing.containerWidth !== null && landing.containerWidth <= landing.containerMaxExpected + 2 && !landing.horizontalOverflow;

  const telegramPass =
    !landing.telegramHasImage &&
    (landing.telegramWhiteGapApprox === null || landing.telegramWhiteGapApprox <= 20) &&
    !landing.horizontalOverflow;

  const imageLayoutPass =
    questionAndFlow.layout.optionCount >= 4 &&
    !questionAndFlow.layout.horizontalOverflow &&
    questionAndFlow.layout.allInside &&
    !questionAndFlow.layout.overlaps;

  return {
    viewport: mobile ? 'mobile' : 'desktop',
    checks: {
      desktopStretchPass,
      telegramPass,
      imageLayoutPass,
      navigationAndAnswersPass: questionAndFlow.flow.pass,
    },
    landing,
    questionLayout: questionAndFlow.layout,
    answerFlow: questionAndFlow.flow,
  };
}

const browser = await chromium.launch({ headless: true });
const desktop = await runViewport(browser, false);
const mobile = await runViewport(browser, true);
await browser.close();

console.log(JSON.stringify({ desktop, mobile }, null, 2));
