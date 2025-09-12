from src.const import *
from icecream import ic

async def xrpscan(page, site_url, exchanges, /): 
    await page.goto(site_url, timeout=wait_timeout)
    print(f"'{await page.title()}' 페이지에 성공적으로 접속했습니다.")


    for exchange in exchanges:
        print(f"{exchange["name"]} 검색 중....")
        
        search_form = page.locator('form.search-wrapper.form-inline')
        search_input = search_form.locator('input.react-autosuggest__input')

        await search_input.type(exchange["input"])
        current_value = await search_input.input_value()
        print(f"입력된 값: '{current_value}'")
        
        await page.wait_for_timeout(waiting_for_data)
        
        suggestions_div = search_form.locator('#react-autowhatever-1')
        suggestion_items = suggestions_div.locator('ul > li')
        all_texts = await suggestion_items.all_inner_texts()
        
        ic(all_texts)

        print("\n--- 자동 완성 제안 목록 ---")
        for i, text in all_texts:
            print(i, text)
            await suggestions_div.press('ArrowDown')
            await page.wait_for_timeout(waiting_for_data)
            input_element = search_form.locator("div > input")
            active_item_id = await input_element.get_attribute('aria-activedescendant')
            print(active_item_id)
            break

