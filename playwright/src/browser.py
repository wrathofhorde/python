from src.const import page_waiting
from src.scanner import scan_pages
from playwright.async_api import async_playwright



async def open_site(data, /):
    sites = data.get("sites", [])
    exchanges = data.get("exchanges", [])

    async with async_playwright() as p:
        
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for site in sites:
            site_name = site.get("name", "이름 없음")
            site_url = site.get("url")
            scanner = scan_pages[site_name]

            if not site_url:
                print(f"'{site_name}'에 URL이 정의되어 있지 않습니다. 건너뜁니다.")
                continue

            print(f"'{site_name}'({site_url}) 로 이동 중...")
            
            try:
                await scanner(page, site_url, exchanges)
                await page.wait_for_timeout(page_waiting) # 10초 대기
            except Exception as e:
                print(f"'{site_name}' 접속 중 오류 발생: {e}")
                
        await browser.close()