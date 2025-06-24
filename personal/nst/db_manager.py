# db_manager.py
import sqlite3
from datetime import datetime

DB_NAME = 'kospi200.sq3'

def get_db_connection():
    """SQLite 데이터베이스 연결을 생성하고 반환합니다."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # 컬럼명으로 접근 가능하도록 설정
    return conn

def create_table_if_not_exists():
    """kospi200_stocks 테이블이 없으면 생성합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kospi200_stocks (
            stock_code TEXT PRIMARY KEY NOT NULL,
            stock_name TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            removed_at TIMESTAMP NULL
        )
    ''')
    # updated_at 컬럼 자동 업데이트를 위한 트리거 (선택 사항, SQLite 3.38.0+ 필요)
    # 아래 트리거는 SQLite 버전이 낮으면 오류 발생 가능. 그럴 경우 Python 코드에서 updated_at을 직접 관리.
    try:
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_kospi200_stocks_updated_at
            AFTER UPDATE ON kospi200_stocks
            FOR EACH ROW
            BEGIN
                UPDATE kospi200_stocks SET updated_at = CURRENT_TIMESTAMP
                WHERE stock_code = OLD.stock_code;
            END;
        ''')
    except sqlite3.OperationalError as e:
        if "no such module: FTS5" not in str(e) and "syntax error" not in str(e).lower(): # FTS5 관련 오류는 무시할 수 있음
            print(f"경고: updated_at 트리거 생성 중 오류 발생 (SQLite 버전 문제일 수 있음): {e}")
        else:
            print("정보: updated_at 트리거는 SQLite 버전 제약으로 생성되지 않을 수 있습니다.")


    conn.commit()
    conn.close()
    print("DB 테이블 확인/생성 완료.")

def get_all_active_stocks_from_db():
    """DB에서 현재 활성화된(is_active=1) 모든 종목을 가져옵니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stock_code, stock_name FROM kospi200_stocks WHERE is_active = 1")
    rows = cursor.fetchall()
    conn.close()
    return {row['stock_code']: row['stock_name'] for row in rows}

def get_stock_by_code(stock_code):
    """특정 종목 코드로 DB에서 종목 정보를 가져옵니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kospi200_stocks WHERE stock_code = ?", (stock_code,))
    row = cursor.fetchone()
    conn.close()
    return row

def add_stock(stock_code, stock_name):
    """새로운 종목을 DB에 추가합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now()
    try:
        cursor.execute('''
            INSERT INTO kospi200_stocks (stock_code, stock_name, is_active, created_at, updated_at)
            VALUES (?, ?, 1, ?, ?)
        ''', (stock_code, stock_name, now, now))
        conn.commit()
        print(f"종목 추가: {stock_code} - {stock_name}")
    except sqlite3.IntegrityError:
        print(f"오류: 종목 코드 {stock_code}는 이미 존재합니다. 추가하지 않습니다.")
    finally:
        conn.close()

def update_stock_name(stock_code, new_stock_name):
    """기존 종목의 이름을 업데이트합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_for_update = datetime.now() # 트리거가 없다면 직접 업데이트
    # 트리거가 있다면 updated_at은 자동으로 설정됨
    cursor.execute('''
        UPDATE kospi200_stocks
        SET stock_name = ?, updated_at = ?
        WHERE stock_code = ?
    ''', (new_stock_name, now_for_update, stock_code))
    conn.commit()
    conn.close()
    print(f"종목명 업데이트: {stock_code} -> {new_stock_name}")

def deactivate_stock(stock_code):
    """종목을 비활성화(편출) 처리합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now()
    now_for_update = datetime.now() # 트리거가 없다면 직접 업데이트
    cursor.execute('''
        UPDATE kospi200_stocks
        SET is_active = 0, removed_at = ?, updated_at = ?
        WHERE stock_code = ?
    ''', (now, now_for_update, stock_code))
    conn.commit()
    conn.close()
    print(f"종목 비활성화 (편출): {stock_code}")

def reactivate_stock(stock_code, stock_name):
    """비활성화된 종목을 다시 활성화(재편입)하고, 필요한 경우 종목명을 업데이트합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_for_update = datetime.now() # 트리거가 없다면 직접 업데이트
    cursor.execute('''
        UPDATE kospi200_stocks
        SET stock_name = ?, is_active = 1, removed_at = NULL, updated_at = ?
        WHERE stock_code = ?
    ''', (stock_name, now_for_update, stock_code))
    conn.commit()
    conn.close()
    print(f"종목 재활성화 (재편입): {stock_code} - {stock_name}")

def sync_stocks_with_db(crawled_stocks_dict):
    """크롤링한 종목 정보와 DB를 동기화합니다."""
    print("\nDB와 크롤링 데이터 동기화 시작...")
    db_active_stocks = get_all_active_stocks_from_db()

    crawled_codes = set(crawled_stocks_dict.keys())
    db_codes = set(db_active_stocks.keys())

    # 1. 새로 추가된 종목 (크롤링 O, DB X 또는 DB에 있지만 비활성)
    newly_added_codes = crawled_codes - db_codes
    for code in newly_added_codes:
        existing_stock = get_stock_by_code(code)
        if existing_stock: # DB에 존재하지만 is_active=0 인 경우 (재편입)
            if existing_stock['is_active'] == 0:
                reactivate_stock(code, crawled_stocks_dict[code])
            elif existing_stock['stock_name'] != crawled_stocks_dict[code]: # 활성 상태지만 이름이 다른 경우
                update_stock_name(code, crawled_stocks_dict[code])
        else: # DB에 아예 없는 경우 (신규 편입)
            add_stock(code, crawled_stocks_dict[code])

    # 2. 편출된 종목 (크롤링 X, DB O)
    removed_codes = db_codes - crawled_codes
    for code in removed_codes:
        deactivate_stock(code)

    # 3. 유지되는 종목 (크롤링 O, DB O) - 종목명 변경 가능성 확인
    maintained_codes = crawled_codes.intersection(db_codes)
    for code in maintained_codes:
        if db_active_stocks[code] != crawled_stocks_dict[code]:
            update_stock_name(code, crawled_stocks_dict[code])
        else:
            # 이름이 같으면 updated_at만 갱신 (선택사항, 데이터 변경이 없으면 안해도 됨)
            # 트리거가 없다면 여기서 명시적으로 updated_at을 갱신할 수 있음
            # conn = get_db_connection()
            # cursor = conn.cursor()
            # cursor.execute("UPDATE kospi200_stocks SET updated_at = CURRENT_TIMESTAMP WHERE stock_code = ?", (code,))
            # conn.commit()
            # conn.close()
            pass


    print("DB 동기화 완료.")

# 초기 테이블 생성 실행
if __name__ == '__main__':
    create_table_if_not_exists()
    # 테스트용 데이터 추가 예시
    # add_stock('999999', '테스트종목')
    # print(get_all_active_stocks_from_db())
    # deactivate_stock('999999')
    # print(get_stock_by_code('999999')['is_active'])
    # reactivate_stock('999999', '테스트종목활성')
    # print(get_stock_by_code('999999')['is_active'])