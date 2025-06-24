import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

def parse_stocks_from_page_html(page_html_content):
    """
    단일 페이지의 HTML 내용에서 종목명과 종목코드를 파싱합니다.
    """
    soup = BeautifulSoup(page_html_content, 'html.parser')
    stocks_dict = {}

    target_table = soup.find('table', class_='type_1')

    if not target_table:
        print("페이지 내용에서 class 'type_1' 테이블을 찾지 못했습니다.")
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

def get_kospi200_stocks_with_paging():
    """
    네이버 금융 KOSPI200 페이지에서 모든 편입종목(페이징 처리 포함)의
    종목번호와 종목명을 가져옵니다.
    """
    main_page_url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    base_url = "https://finance.naver.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    all_stocks_dict = {}

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
        print("경고: 메인 페이지 EUC-KR 디코딩 실패. 자동 감지된 인코딩 사용.")
        
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

    # 페이징 처리를 위한 준비
    current_page = 1
    max_page_found = False # 최대 페이지를 동적으로 찾기 위한 플래그

    # 첫 페이지 처리
    try:
        response_page = requests.get(first_iframe_url, headers=headers)
        response_page.raise_for_status()
        
        try:
            page_html_content = response_page.content.decode('euc-kr', 'replace')
        except UnicodeDecodeError:
            page_html_content = response_page.text
            print(f"경고: iframe 페이지 ({first_iframe_url}) EUC-KR 디코딩 실패. 자동 감지된 인코딩 사용.")

        stocks_on_page = parse_stocks_from_page_html(page_html_content)
        all_stocks_dict.update(stocks_on_page)
        print(f"정보: {current_page}페이지에서 {len(stocks_on_page)}개 종목 수집. 총 {len(all_stocks_dict)}개.")

        # 최대 페이지 번호 찾기 (첫 페이지만으로도 가능)
        page_soup = BeautifulSoup(page_html_content, 'html.parser')
        
        # 페이지 네비게이션 영역 찾기 (보통 table.Nnavi 또는 div.pgRR)
        navi_area = page_soup.find('table', class_='Nnavi')
        if not navi_area:
            navi_area = page_soup.find('div', class_='pgRR') # 다른 형태의 페이지네이션
        
        last_page_num = current_page
        if navi_area:
            # '맨뒤' 링크 찾기
            last_page_link = navi_area.find('a', class_='pgRR') 
            if last_page_link and last_page_link.has_attr('href'):
                href = last_page_link['href']
                match = re.search(r'page=(\d+)', href)
                if match:
                    last_page_num = int(match.group(1))
                    print(f"정보: '맨뒤' 링크에서 최대 페이지 번호 {last_page_num} 확인.")
            else:
                # '맨뒤' 링크가 없다면, 숫자 링크 중 가장 큰 것 찾기
                page_links = navi_area.find_all('a', href=re.compile(r'page=\d+'))
                if page_links:
                    for plink in page_links:
                        match = re.search(r'page=(\d+)', plink['href'])
                        if match:
                            num = int(match.group(1))
                            if num > last_page_num:
                                last_page_num = num
                    print(f"정보: 숫자 링크에서 최대 페이지 번호 {last_page_num} 확인.")
                else: # 숫자 링크도 없으면 현재 페이지가 마지막이거나 구조가 매우 다름
                    print("정보: 페이지 네비게이션에서 추가 페이지 링크를 찾지 못했습니다. 현재 페이지가 마지막일 수 있습니다.")
        else:
            print("정보: 페이지 네비게이션 영역을 찾을 수 없습니다. 단일 페이지로 간주합니다.")
            last_page_num = 1 # 페이지 네비게이션이 없으면 1페이지로 가정

        max_page_found = True

    except requests.exceptions.RequestException as e:
        print(f"iframe 첫 페이지 요청 오류 ({first_iframe_url}): {e}")
        return all_stocks_dict # 현재까지 수집된 것만 반환

    # 나머지 페이지 처리
    if max_page_found and last_page_num > 1:
        parsed_url = urlparse(first_iframe_url)
        base_query_params = parse_qs(parsed_url.query)

        for page_num in range(2, last_page_num + 1):
            current_page = page_num
            query_params = base_query_params.copy()
            query_params['page'] = [str(current_page)] # page 파라미터 업데이트
            
            # 새 URL 생성 (path는 그대로, query만 변경)
            next_page_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
            print(f"정보: {current_page}페이지 요청 중... URL: {next_page_url}")

            try:
                response_page = requests.get(next_page_url, headers=headers)
                response_page.raise_for_status()

                try:
                    page_html_content = response_page.content.decode('euc-kr', 'replace')
                except UnicodeDecodeError:
                    page_html_content = response_page.text
                    print(f"경고: iframe 페이지 ({next_page_url}) EUC-KR 디코딩 실패. 자동 감지된 인코딩 사용.")

                stocks_on_page = parse_stocks_from_page_html(page_html_content)
                all_stocks_dict.update(stocks_on_page)
                print(f"정보: {current_page}페이지에서 {len(stocks_on_page)}개 종목 수집. 총 {len(all_stocks_dict)}개.")
                
                if not stocks_on_page and current_page < last_page_num : # 페이지에 종목이 없으면 중단 (예외 상황)
                    print(f"경고: {current_page}페이지에서 종목을 찾지 못했습니다. (최대 페이지: {last_page_num})")
                    break

            except requests.exceptions.RequestException as e:
                print(f"iframe {current_page}페이지 요청 오류 ({next_page_url}): {e}")
                continue # 다음 페이지 시도 또는 여기서 중단 결정 가능
            except Exception as e_parse:
                print(f"{current_page}페이지 파싱 중 오류: {e_parse}")
                continue

    return all_stocks_dict


if __name__ == "__main__":
    kospi200_stocks = get_kospi200_stocks_with_paging()

    if kospi200_stocks:
        for code, name in kospi200_stocks.items(): # 너무 많아서 일부만 출력하거나 생략
            print(f"{code}: {name}")
            
        print("\nKOSPI 200 편입종목 (종목번호: 종목명)")
        print(f"\n총 {len(kospi200_stocks)}개의 종목을 찾았습니다.")
    else:
        print("KOSPI 200 편입종목을 가져오지 못했습니다.")