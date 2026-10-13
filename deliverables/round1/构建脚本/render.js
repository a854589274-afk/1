// usage: node render.js in.svg out.png width height [transparent]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [,, inp, out, w, h, transp] = process.argv;
  const svg = fs.readFileSync(inp, 'utf8');
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' in {} ? undefined : undefined });
  const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await page.screenshot({ path: out, omitBackground: transp === '1', clip: { x: 0, y: 0, width: +w, height: +h } });
  await browser.close();
})();
