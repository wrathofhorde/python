import asyncio
import json
from playwright.async_api import async_playwright
from src.browser import open_site

async def main():
    try:
        with open('sites.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            sites = data.get("sites", [])
            exchanges = data.get("exchanges", [])

            if not sites:
                print("JSON 파일에 'sites' 목록이 비어 있거나 올바르지 않습니다.")
                return
            
            if not exchanges:
                print("JSON 파일에 'exchanges' 목록이 비어 있거나 올바르지 않습니다.")
                return


    except FileNotFoundError:
        print("sites.json 파일을 찾을 수 없습니다.")
        return
    
    await open_site(data)


if __name__ == "__main__":
    asyncio.run(main())