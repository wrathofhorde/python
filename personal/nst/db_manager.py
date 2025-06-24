# db_manager.py
import sqlite3
from datetime import datetime

DB_NAME = 'kospi200.sq3'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_kospi200_stocks_table_if_not_exists(): # 함수명 명확히 변경
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kospi200_stocks (
            stock_code TEXT PRIMARY KEY NOT NULL,
            stock_name TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
            updated_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
            removed_at TEXT NULL
        )
    ''')
    try:
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_kospi200_stocks_updated_at
            AFTER UPDATE ON kospi200_stocks
            FOR EACH ROW
            BEGIN
                UPDATE kospi200_stocks SET updated_at = (STRFTIME('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))
                WHERE stock_code = OLD.stock_code;
            END;
        ''')
    except sqlite3.OperationalError as e:
        if "no such module: FTS5" not in str(e) and "syntax error" not in str(e).lower():
             print(f"경고: kospi200_stocks updated_at 트리거 생성 중 오류 발생: {e}")
        else:
             print("정보: kospi200_stocks updated_at 트리거는 SQLite 버전 제약으로 생성되지 않을 수 있습니다.")
    conn.commit()
    conn.close()
    print("kospi200_stocks 테이블 확인/생성 완료.")


def create_daily_prices_table_if_not_exists():
    """daily_stock_prices 테이블이 없으면 생성합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stock_prices (
            stock_code TEXT NOT NULL,
            date TEXT NOT NULL,
            close_price INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
            PRIMARY KEY (stock_code, date),
            FOREIGN KEY (stock_code) REFERENCES kospi200_stocks (stock_code)
                ON DELETE CASCADE ON UPDATE CASCADE  -- kospi200_stocks에서 삭제/업데이트 시 연동 (선택적)
        )
    ''')
    conn.commit()
    conn.close()
    print("daily_stock_prices 테이블 확인/생성 완료.")

def add_daily_prices_batch(stock_code, daily_prices_list):
    """
    여러 개의 일별 시세 데이터를 한 번에 DB에 추가합니다.
    daily_prices_list: [{'date': 'YYYY.MM.DD', 'close_price': 12345}, ...] 형태의 리스트
    """
    if not daily_prices_list:
        return 0

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 날짜 형식을 'YYYY-MM-DD'로 통일 (SQLite가 날짜 함수를 더 잘 다루도록)
    formatted_prices = []
    for price_data in daily_prices_list:
        try:
            # 네이버 날짜 형식 'YYYY.MM.DD'를 'YYYY-MM-DD'로 변환
            standard_date = price_data['date'].replace('.', '-')
            # 종가에서 콤마 제거 및 정수 변환
            close_price = int(str(price_data['close_price']).replace(',', ''))
            formatted_prices.append((stock_code, standard_date, close_price))
        except Exception as e:
            print(f"Error formatting price data {price_data} for {stock_code}: {e}")
            continue

    if not formatted_prices:
        conn.close()
        return 0

    # `INSERT OR IGNORE`를 사용하여 중복된 (stock_code, date)는 무시하고 새 데이터만 추가
    # 또는 `INSERT OR REPLACE`를 사용하면 기존 데이터를 새 데이터로 대체
    # 여기서는 새로운 데이터만 추가하는 `INSERT OR IGNORE` 사용
    try:
        cursor.executemany('''
            INSERT OR IGNORE INTO daily_stock_prices (stock_code, date, close_price)
            VALUES (?, ?, ?)
        ''', formatted_prices)
        conn.commit()
        inserted_rows = cursor.rowcount # executemany에서 INSERT OR IGNORE의 rowcount는 정확하지 않을 수 있음
                                      # 정확한 개수를 원하면 SELECT COUNT(*) 등으로 확인 필요
        print(f"{stock_code}: {len(formatted_prices)}개 중 실제 추가/영향 받은 일별 시세 데이터 수 (추정): {inserted_rows if inserted_rows != -1 else '확인필요'}")
        return len(formatted_prices) # 실제 시도한 데이터 개수 반환
    except sqlite3.Error as e:
        print(f"DB 오류 (일별 시세 추가 중 - {stock_code}): {e}")
        return 0
    finally:
        conn.close()

def get_latest_stored_date_for_stock(stock_code):
    """특정 종목의 DB에 저장된 가장 최근 일별 시세 날짜를 가져옵니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date) FROM daily_stock_prices WHERE stock_code = ?", (stock_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else None


# kospi200_stocks 관련 함수들은 이전과 동일 (add_stock, update_stock_name 등)
# ... (이전 db_manager.py의 나머지 함수들) ...
def get_all_active_stocks_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stock_code, stock_name FROM kospi200_stocks WHERE is_active = 1")
    rows = cursor.fetchall()
    conn.close()
    return {row['stock_code']: row['stock_name'] for row in rows}

def get_stock_by_code(stock_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kospi200_stocks WHERE stock_code = ?", (stock_code,))
    row = cursor.fetchone()
    conn.close()
    return row

def add_stock(stock_code, stock_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] # 밀리초 포함
    try:
        cursor.execute('''
            INSERT INTO kospi200_stocks (stock_code, stock_name, is_active, created_at, updated_at)
            VALUES (?, ?, 1, ?, ?)
        ''', (stock_code, stock_name, now_str, now_str))
        conn.commit()
        print(f"종목 추가: {stock_code} - {stock_name}")
    except sqlite3.IntegrityError:
        print(f"오류: 종목 코드 {stock_code}는 이미 존재합니다. 추가하지 않습니다.")
    finally:
        conn.close()

def update_stock_name(stock_code, new_stock_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str_for_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    cursor.execute('''
        UPDATE kospi200_stocks
        SET stock_name = ?, updated_at = ? 
        WHERE stock_code = ?
    ''', (new_stock_name, now_str_for_update, stock_code))
    conn.commit()
    conn.close()
    print(f"종목명 업데이트: {stock_code} -> {new_stock_name}")

def deactivate_stock(stock_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    now_str_for_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    cursor.execute('''
        UPDATE kospi200_stocks
        SET is_active = 0, removed_at = ?, updated_at = ?
        WHERE stock_code = ?
    ''', (now_str, now_str_for_update, stock_code))
    conn.commit()
    conn.close()
    print(f"종목 비활성화 (편출): {stock_code}")

def reactivate_stock(stock_code, stock_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str_for_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    cursor.execute('''
        UPDATE kospi200_stocks
        SET stock_name = ?, is_active = 1, removed_at = NULL, updated_at = ?
        WHERE stock_code = ?
    ''', (stock_name, now_str_for_update, stock_code))
    conn.commit()
    conn.close()
    print(f"종목 재활성화 (재편입): {stock_code} - {stock_name}")

def sync_stocks_with_db(crawled_stocks_dict):
    print("\nDB와 크롤링 데이터 동기화 시작...")
    db_active_stocks = get_all_active_stocks_from_db()
    crawled_codes = set(crawled_stocks_dict.keys())
    db_codes = set(db_active_stocks.keys())
    newly_added_codes = crawled_codes - db_codes
    for code in newly_added_codes:
        existing_stock = get_stock_by_code(code)
        if existing_stock:
            if existing_stock['is_active'] == 0:
                reactivate_stock(code, crawled_stocks_dict[code])
            elif existing_stock['stock_name'] != crawled_stocks_dict[code]:
                update_stock_name(code, crawled_stocks_dict[code])
        else:
            add_stock(code, crawled_stocks_dict[code])
    removed_codes = db_codes - crawled_codes
    for code in removed_codes:
        deactivate_stock(code)
    maintained_codes = crawled_codes.intersection(db_codes)
    for code in maintained_codes:
        if db_active_stocks[code] != crawled_stocks_dict[code]:
            update_stock_name(code, crawled_stocks_dict[code])
    print("DB 동기화 완료.")


if __name__ == '__main__':
    create_kospi200_stocks_table_if_not_exists()
    create_daily_prices_table_if_not_exists()