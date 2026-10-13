// node render.js jobs.json   jobs: [[in.svg, out.png, w, h, transparent], ...]  以 2 倍像素渲染
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ deviceScaleFactor: 2 });
  for (const [inp, out, w, h, tr] of jobs) {
    const page = await ctx.newPage({ viewport: { width: w, height: h } });
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(inp, 'utf8')}</body></html>`);
    await page.screenshot({ path: out, omitBackground: !!tr, clip: { x: 0, y: 0, width: w, height: h } });
    await page.close();
  }
  await browser.close();
})();
