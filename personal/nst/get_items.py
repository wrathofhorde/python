import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def parse_stocks_from_iframe_html(iframe_html_content):
    """
    iframe의 HTML 내용에서 종목명과 종목코드를 파싱합니다.
    """
    soup = BeautifulSoup(iframe_html_content, 'html.parser')
    stocks_dict = {}

    # 디버깅: 수신된 iframe HTML의 시작 부분 출력
    # print("\n--- iframe HTML 내용 (처음 3000자) ---")
    # print(iframe_html_content[:3000])
    # print("--- iframe HTML 내용 끝 ---\n")

    # 1. 테이블 찾기 (class="type_1" 테이블)
    #    가장 바깥쪽 테이블을 찾도록 시도
    target_table = soup.find('table', class_='type_1')

    if not target_table:
        print("iframe 내용에서 class 'type_1' 테이블을 찾지 못했습니다.")
        # 테이블을 못 찾으면, HTML 전체에서 a 태그 중 code=xxxxxx 패턴을 가진 것을 모두 찾아보는 예외 처리도 고려 가능
        # 하지만 지금은 테이블 구조가 있다고 가정하고 진행
        return {}
    
    # 디버깅: 찾은 테이블 HTML 일부 출력
    # print("\n--- 찾은 target_table HTML (일부) ---")
    # print(target_table.prettify()[:1000]) # 테이블 구조 확인
    # print("--- target_table HTML 끝 ---\n")

    # 2. 종목 행(tr) 찾기
    #    tbody 유무에 관계없이 table 바로 아래 tr[onmouseover]를 찾거나, 모든 tr을 대상으로 함
    stock_rows = target_table.select('tr[onmouseover]') # tbody를 명시하지 않음
    
    if not stock_rows:
        print("정보: table > tr[onmouseover]를 찾지 못했습니다. table > tr 전체를 시도합니다.")
        stock_rows = target_table.find_all('tr') # a 태그가 있는 tr만 필터링 필요
        if not stock_rows:
            print("iframe 테이블 내에서 종목 행(tr)을 찾을 수 없습니다.")
            return {}

    # print(f"정보: {len(stock_rows)}개의 행(tr)을 찾았습니다.")

    for i, row in enumerate(stock_rows):
        # 헤더 행(th 포함)은 건너뛰기
        if row.find('th'): 
            # print(f"정보: {i+1}번째 행은 헤더로 추정되어 건너뜁니다.")
            continue

        # 종목명과 링크는 보통 td.tltle a 에 있습니다.
        link_tag = row.select_one('td.tltle a')
        
        # 만약 td.tltle a 로 못찾는 경우, 첫번째 td > a 를 시도 (보다 일반적)
        if not link_tag:
            first_td = row.find('td')
            if first_td:
                link_tag = first_td.find('a', href=re.compile(r"code=\d{6}")) # href에 code 패턴이 있는 a만
        
        if link_tag: # link_tag.has_attr('href')는 위에서 re.compile로 이미 검사됨
            stock_name = link_tag.get_text(strip=True)
            href_value = link_tag['href'] # 이미 href 속성이 있음이 보장됨
            
            match = re.search(r"code=(\d{6})", href_value) # 여기서 한 번 더 확인 (사실상 불필요하나 안전장치)
            if match:
                stock_code = match.group(1)
                if stock_name and stock_code:
                    stocks_dict[stock_code] = stock_name
                    # print(f"추출 성공: {stock_code} - {stock_name}")
            # else: # 이 경우는 거의 발생하지 않아야 함
                # print(f"경고 (iframe): {stock_name} ({href_value}) 에서 종목 코드를 추출하지 못했습니다 (정규식 불일치).")
        # elif row.find('td'): # td는 있지만 링크를 못찾는 경우 (데이터가 없는 행 등)
            # print(f"경고 (iframe): {i+1}번째 행에서 유효한 종목 링크를 찾지 못했습니다: {row.text.strip()[:100]}...")
            # pass

    if not stocks_dict:
        print("경고: 종목을 하나도 추출하지 못했습니다. iframe HTML 및 파싱 로직을 확인해주세요.")

    return stocks_dict

def get_kospi200_stocks():
    """
    네이버 금융 KOSPI200 페이지에서 편입종목의 종목번호와 종목명을 가져옵니다.
    편입종목 정보는 iframe에 있으므로, iframe의 src를 찾아 해당 URL로 다시 요청합니다.
    """
    main_page_url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    base_url = "https://finance.naver.com" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

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
    iframe_full_url = urljoin(base_url, iframe_src_relative)
    
    print(f"정보: 편입종목 iframe URL 발견 - {iframe_full_url}")

    try:
        response_iframe = requests.get(iframe_full_url, headers=headers)
        response_iframe.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"iframe 페이지 요청 오류 ({iframe_full_url}): {e}")
        return {}

    try:
        iframe_html_content = response_iframe.content.decode('euc-kr', 'replace')
    except UnicodeDecodeError:
        iframe_html_content = response_iframe.text
        print(f"경고: iframe 페이지 ({iframe_full_url}) EUC-KR 디코딩 실패. 자동 감지된 인코딩 사용.")

    return parse_stocks_from_iframe_html(iframe_html_content)

if __name__ == "__main__":
    kospi200_stocks = get_kospi200_stocks()

    if kospi200_stocks:
        print("\nKOSPI 200 편입종목 (종목번호: 종목명)")
        for code, name in kospi200_stocks.items():
            print(f"{code}: {name}")
        print(f"\n총 {len(kospi200_stocks)}개의 종목을 찾았습니다.")
    else:
        print("KOSPI 200 편입종목을 가져오지 못했습니다.")