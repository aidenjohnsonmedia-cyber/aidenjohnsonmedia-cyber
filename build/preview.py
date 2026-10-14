import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text().replace('src="assets/', 'src="../assets/')
# crude: just embed the README html as-is (it is html already)
html = f"""<!doctype html><html><body style="background:#0d1117;margin:0;padding:32px;color:#e6edf3;font-family:-apple-system,Segoe UI,sans-serif;font-size:16px">
<div style="max-width:900px;margin:0 auto">{README}</div></body></html>"""
(ROOT / "build" / "preview.html").write_text(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 980, "height": 900})
        await pg.goto(f"file://{ROOT}/build/preview.html")
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=str(ROOT / "build" / "preview.png"), full_page=True)
        await b.close()

asyncio.run(main())
print("ok")
