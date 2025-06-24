import os
import crawler
import db_manager

def main():
    db_manager.create_table_if_not_exists()
    print("KOSPI200 종목 크롤링 시작...")
    crawled_stocks  = crawler.get_kospi200_stocks_with_paging() 

    if not crawled_stocks:
        print("크롤링된 종목이 없습니다. 프로그램을 종료합니다.")
        return

    print(f"\n크롤링 완료. 총 {len(crawled_stocks)}개의 종목을 가져왔습니다.")

    db_manager.sync_stocks_with_db(crawled_stocks)

    # 4. (선택) 동기화 후 DB 내용 확인
    print("\n동기화 후 DB에 저장된 활성 KOSPI200 종목:")
    final_db_stocks = db_manager.get_all_active_stocks_from_db()
    if final_db_stocks:
        # for code, name in final_db_stocks.items(): # 너무 많으면 일부만 출력
        #     print(f"{code}: {name}")
        print(f"DB에 저장된 활성 종목 수: {len(final_db_stocks)}")
    else:
        print("DB에서 활성 종목을 찾을 수 없습니다.")
    
    db_file_path = os.path.join(os.getcwd(), db_manager.DB_NAME)
    print(f"\n데이터베이스 파일 '{db_manager.DB_NAME}'이(가) 현재 디렉토리에 저장/업데이트 되었습니다: {db_file_path}")



if __name__ == "__main__":
    main()
