from src.const import wait_timeout

async def ethscan(page, site_url, exchanges, /): 
    await page.goto(site_url, timeout=wait_timeout) # 60초 타임아웃
    print(f"'{await page.title()}' 페이지에 성공적으로 접속했습니다.")