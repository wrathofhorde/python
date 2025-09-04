from src.const import wait_timeout, waiting_for_input

async def xrpscan(page, site_url, exchanges, /): 
    await page.goto(site_url, timeout=wait_timeout)
    print(f"'{await page.title()}' 페이지에 성공적으로 접속했습니다.")

    for exchange in exchanges:
        print(f"{exchange["name"]} 검색 중....")
        
        search_form = page.locator('form.search-wrapper.form-inline')
        search_input = search_form.locator('input.react-autosuggest__input')

        await search_input.fill(exchange["input"])
        await page.wait_for_timeout(waiting_for_input)
        current_value = await search_input.input_value()
        print(f"입력된 값: '{current_value}'")

        suggestions_div = search_form.locator('#react-autowhatever-1')
        suggestion_items = suggestions_div.locator('ul > li')
        all_texts = await suggestion_items.all_inner_texts()

        print("\n--- 자동 완성 제안 목록 ---")
        for text in all_texts:
            search_form = page.locator('form.search-wrapper.form-inline')
            search_input = search_form.locator('input.react-autosuggest__input')
