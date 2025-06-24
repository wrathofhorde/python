# crawler.py
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import time
from datetime import datetime, timedelta # timedelta는 이번 수정에서 직접 사용하지 않지만 날짜 비교시 유용

# ... (get_kospi200_stocks_with_paging 및 parse_stocks_from_page_html 함수는 이전과 동일) ...
# parse_stocks_from_page_html 함수는 이전과 동일
def parse_stocks_from_page_html(page_html_content):
    soup = BeautifulSoup(page_html_content, 'html.parser')
    stocks_dict = {}
    target_table = soup.find('table', class_='type_1')
    if not target_table:
        return {}
    stock_rows = target_table.select('tr[onmouseover]')
    if not stock_rows:
        stock_rows = target_table.find_all('tr')
    for row in stock_rows:
        if row.find('th'):
            continue
        link_tag = row.select_one('td.tltle a')
        if not link_tag:
            first_td = row.find('td')
            if first_td:
                link_tag = first_td.find('a', href=re.compile(r"code=\d{6}"))
        if link_tag:
            stock_name = link_tag.get_text(strip=True)
            href_value = link_tag['href']
            match = re.search(r"code=(\d{6})", href_value)
            if match:
                stock_code = match.group(1)
                if stock_name and stock_code:
                    stocks_dict[stock_code] = stock_name
    return stocks_dict

# get_kospi200_stocks_with_paging 함수는 이전과 동일
def get_kospi200_stocks_with_paging(delay_seconds=1):
    main_page_url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    base_url = "https://finance.naver.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    all_stocks_dict = {}
    print(f"정보: 메인 페이지 요청 시작 - {main_page_url}")
    try:
        response_main = requests.get(main_page_url, headers=headers)
        response_main.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"메인 페이지 요청 오류 ({main_page_url}): {e}")
        return {}
    try:
        main_html_content = response_main.content.decode('euc-kr', 'replace')
    except UnicodeDecodeError:
        main_html_content = response_main.text
    soup_main = BeautifulSoup(main_html_content, 'html.parser')
    iframe_tag = soup_main.find('iframe', {'title': '편입종목상위 영역'})
    if not iframe_tag:
        iframe_tag = soup_main.find('iframe', src=re.compile(r'/sise/entryJongmok\.naver.*type=KPI200'))
    if not iframe_tag or not iframe_tag.has_attr('src'):
        print("편입종목 정보를 담고 있는 iframe을 찾을 수 없습니다.")
        return {}
    iframe_src_relative = iframe_tag['src']
    first_iframe_url = urljoin(base_url, iframe_src_relative)
    print(f"정보: 첫 번째 편입종목 iframe URL 발견 - {first_iframe_url}")
    current_page = 1
    max_page_found = False
    print(f"정보: 첫 번째 iframe ({current_page}페이지) 요청 시작...")
    try:
        time.sleep(delay_seconds) 
        response_page = requests.get(first_iframe_url, headers=headers)
        response_page.raise_for_status()
        try:
            page_html_content = response_page.content.decode('euc-kr', 'replace')
        except UnicodeDecodeError:
            page_html_content = response_page.text
        stocks_on_page = parse_stocks_from_page_html(page_html_content)
        all_stocks_dict.update(stocks_on_page)
        print(f"정보: {current_page}페이지에서 {len(stocks_on_page)}개 종목 수집. 총 {len(all_stocks_dict)}개.")
        page_soup = BeautifulSoup(page_html_content, 'html.parser')
        navi_area = page_soup.find('table', class_='Nnavi')
        if not navi_area: navi_area = page_soup.find('div', class_='pgRR') 
        last_page_num = current_page
        if navi_area:
            last_page_link = navi_area.find('a', class_='pgRR') 
            if last_page_link and last_page_link.has_attr('href'):
                href = last_page_link['href']
                match = re.search(r'page=(\d+)', href)
                if match: last_page_num = int(match.group(1))
            else:
                page_links = navi_area.find_all('a', href=re.compile(r'page=\d+'))
                if page_links:
                    for plink in page_links:
                        match = re.search(r'page=(\d+)', plink['href'])
                        if match: 
                            num = int(match.group(1))
                            if num > last_page_num: last_page_num = num
        print(f"정보: 최대 페이지 번호 {last_page_num} 확인.")
        max_page_found = True
    except requests.exceptions.RequestException as e:
        print(f"iframe 첫 페이지 요청 오류 ({first_iframe_url}): {e}")
        return all_stocks_dict 
    if max_page_found and last_page_num > 1:
        parsed_url = urlparse(first_iframe_url)
        base_query_params = parse_qs(parsed_url.query)
        for page_num in range(2, last_page_num + 1):
            current_page = page_num
            query_params = base_query_params.copy()
            query_params['page'] = [str(current_page)] 
            next_page_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
            print(f"정보: {current_page}페이지 요청 중... URL: {next_page_url}")
            try:
                print(f"정보: 다음 페이지 요청 전 {delay_seconds}초 대기...")
                time.sleep(delay_seconds) 
                response_page = requests.get(next_page_url, headers=headers)
                response_page.raise_for_status()
                try:
                    page_html_content = response_page.content.decode('euc-kr', 'replace')
                except UnicodeDecodeError:
                    page_html_content = response_page.text
                stocks_on_page = parse_stocks_from_page_html(page_html_content)
                all_stocks_dict.update(stocks_on_page)
                print(f"정보: {current_page}페이지에서 {len(stocks_on_page)}개 종목 수집. 총 {len(all_stocks_dict)}개.")
                if not stocks_on_page and current_page < last_page_num : 
                    print(f"경고: {current_page}페이지에서 종목을 찾지 못했습니다.")
                    break
            except requests.exceptions.RequestException as e:
                print(f"iframe {current_page}페이지 요청 오류 ({next_page_url}): {e}")
                time.sleep(delay_seconds * 2)
                continue 
            except Exception as e_parse:
                print(f"{current_page}페이지 파싱 중 오류: {e_parse}")
                continue
    return all_stocks_dict

# --- 특정 종목의 일별 시세 크롤링 함수 (증분 업데이트 로직 추가) ---
def get_daily_prices_for_stock(stock_code, latest_stored_date_str_db=None, days_to_collect_if_new=120, delay_seconds=1.3):
    """
    특정 종목의 일별 시세를 네이버 금융에서 크롤링합니다.
    DB에 저장된 마지막 날짜 이후의 데이터만 가져오거나, 데이터가 없으면 최근 N일치를 가져옵니다.

    Args:
        stock_code (str): 종목 코드
        latest_stored_date_str_db (str, optional): DB에 저장된 해당 종목의 마지막 날짜 (YYYY-MM-DD 형식).
            None이면 days_to_collect_if_new 만큼 수집.
        days_to_collect_if_new (int): 신규 수집 시 가져올 거래일 수.
        delay_seconds (float): 페이지 요청 간 지연 시간.
    Returns:
        list: [{'date': 'YYYY.MM.DD', 'close_price': 12345}, ...] 형태의 리스트 (새로운 데이터만)
    """
    if latest_stored_date_str_db:
        print(f"\n종목 [{stock_code}] 증분 업데이트 시작 (DB 마지막 날짜: {latest_stored_date_str_db})...")
        latest_stored_date_dt = datetime.strptime(latest_stored_date_str_db, '%Y-%m-%d')
    else:
        print(f"\n종목 [{stock_code}] 신규 데이터 수집 시작 (최근 {days_to_collect_if_new} 거래일 목표)...")
        latest_stored_date_dt = None # 이 경우, days_to_collect_if_new 만큼 수집

    daily_prices_to_add = []
    # 네이버 일별 시세는 한 페이지에 10개씩 보여줌
    # 증분 업데이트 시 얼마나 많은 페이지를 봐야 할지 예측하기 어려우므로,
    # 충분히 많은 페이지를 보되, DB 마지막 날짜 이전 데이터가 나오면 중단.
    # 신규 수집 시에는 days_to_collect_if_new 만큼 수집되면 중단.
    max_pages_to_check = (days_to_collect_if_new // 10) + 5 if not latest_stored_date_dt else 20 # 증분시엔 더 넉넉히
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    collected_new_data_count = 0
    stop_crawling_for_this_stock = False

    for page in range(1, max_pages_to_check + 1):
        if stop_crawling_for_this_stock:
            break
        
        # 신규 수집 시, 목표 개수 달성하면 중단
        if not latest_stored_date_dt and collected_new_data_count >= days_to_collect_if_new:
            print(f"  {stock_code} - 신규 수집 목표({days_to_collect_if_new}일) 달성하여 중단합니다.")
            break

        url = f"https://finance.naver.com/item/sise_day.naver?code={stock_code}&page={page}"
        print(f"  {stock_code} - 일별 시세 {page}페이지 요청: {url}")

        try:
            if page > 1 :
                time.sleep(delay_seconds)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"  오류: {stock_code} - 일별 시세 {page}페이지 요청 실패: {e}")
            break 

        try:
            html_content = response.content.decode('euc-kr', 'replace')
        except UnicodeDecodeError:
            html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        price_table = soup.find('table', class_="type2")
        if not price_table:
            print(f"  {stock_code} - {page}페이지에서 일별 시세 테이블(type2)을 찾을 수 없습니다.")
            if page == 1 and not daily_prices_to_add:
                return []
            break

        rows = price_table.find_all('tr')
        data_found_on_page = False

        for row_idx, row in enumerate(rows):
            if stop_crawling_for_this_stock: break # 내부 루프 즉시 탈출

            tds = row.find_all('td')
            if len(tds) == 7 and tds[0].get_text(strip=True):
                date_str_on_page = tds[0].get_text(strip=True) # YYYY.MM.DD 형식
                close_price_str = tds[1].get_text(strip=True)

                if not date_str_on_page or not close_price_str: continue
                if not re.match(r"^\d{4}\.\d{2}\.\d{2}$", date_str_on_page): continue

                try:
                    current_crawled_date_dt = datetime.strptime(date_str_on_page, "%Y.%m.%d")

                    if latest_stored_date_dt: # 증분 업데이트 로직
                        if current_crawled_date_dt <= latest_stored_date_dt:
                            # 현재 크롤링한 날짜가 DB의 마지막 날짜보다 이전이거나 같으면,
                            # 이 행 및 이후 행, 그리고 다음 페이지들은 더 볼 필요가 없음.
                            print(f"  {stock_code} - DB 마지막 저장일({latest_stored_date_str_db}) 이전/같은 데이터({date_str_on_page})에 도달. 증분 업데이트 중단.")
                            stop_crawling_for_this_stock = True # 모든 루프 중단 플래그
                            break # 현재 페이지의 나머지 row 처리 중단
                        else:
                            # DB 마지막 날짜보다 최신 데이터이므로 추가 대상
                            daily_prices_to_add.append({'date': date_str_on_page, 'close_price': close_price_str})
                            collected_new_data_count += 1
                            data_found_on_page = True
                    else: # 신규 수집 로직
                        daily_prices_to_add.append({'date': date_str_on_page, 'close_price': close_price_str})
                        collected_new_data_count += 1
                        data_found_on_page = True
                        if collected_new_data_count >= days_to_collect_if_new:
                            stop_crawling_for_this_stock = True # 목표 달성, 모든 루프 중단
                            break # 현재 페이지의 나머지 row 처리 중단
                
                except ValueError:
                    print(f"  경고: {stock_code} - 날짜 형식 오류: {date_str_on_page}")
                    continue
            
        if not data_found_on_page and page > 1:
            print(f"  {stock_code} - {page}페이지에서 더 이상 유효한 데이터를 찾지 못했습니다.")
            break
            
    if latest_stored_date_dt:
        print(f"종목 [{stock_code}] 증분 업데이트 완료. 총 {len(daily_prices_to_add)}개 신규 데이터 수집.")
    else:
        print(f"종목 [{stock_code}] 신규 데이터 수집 완료. 총 {len(daily_prices_to_add)}일 데이터 수집.")
    
    # daily_prices_to_add는 시간 순서의 역순 (최신 날짜가 먼저)으로 수집됨.
    # DB에 저장할 때 순서는 크게 중요하지 않지만, 필요하면 여기서 reverse() 가능.
    return daily_prices_to_add