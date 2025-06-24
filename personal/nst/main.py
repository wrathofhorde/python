# main.py
import crawler
import db_manager
import os
import time # main에서도 time.sleep 사용

def main():
    db_manager.create_kospi200_stocks_table_if_not_exists()
    db_manager.create_daily_prices_table_if_not_exists()

    print("KOSPI200 종목 리스트 크롤링 시작...")
    stock_crawl_delay = 1.3
    crawled_kospi200_list = crawler.get_kospi200_stocks_with_paging(delay_seconds=stock_crawl_delay) 

    if not crawled_kospi200_list:
        print("크롤링된 KOSPI200 종목이 없습니다. 일별 시세 수집을 진행하지 않습니다.")
    else:
        print(f"\nKOSPI200 종목 리스트 크롤링 완료. 총 {len(crawled_kospi200_list)}개 종목.")
        db_manager.sync_stocks_with_db(crawled_kospi200_list)

    active_stocks_for_daily_crawl = db_manager.get_all_active_stocks_from_db()
    
    if not active_stocks_for_daily_crawl:
        print("DB에 활성화된 KOSPI200 종목이 없어 일별 시세 수집을 종료합니다.")
        return

    print(f"\n총 {len(active_stocks_for_daily_crawl)}개 활성 종목에 대해 일별 시세 수집을 시작합니다.")

    days_to_collect_for_new_stock = 120 # 신규 종목일 경우 수집할 과거 일수
    daily_price_crawl_delay = 0.7

    for i, (stock_code, stock_name) in enumerate(active_stocks_for_daily_crawl.items()):
        print(f"\n--- [{i+1}/{len(active_stocks_for_daily_crawl)}] 종목: {stock_name} ({stock_code}) 일별 시세 처리 시작 ---")
        
        # DB에서 해당 종목의 마지막 저장된 날짜 가져오기
        latest_db_date_str = db_manager.get_latest_stored_date_for_stock(stock_code)
        
        daily_prices_data = crawler.get_daily_prices_for_stock(
            stock_code, 
            latest_stored_date_str_db=latest_db_date_str, # DB의 마지막 날짜 전달
            days_to_collect_if_new=days_to_collect_for_new_stock, 
            delay_seconds=daily_price_crawl_delay
        )
        
        if daily_prices_data:
            # DB 저장은 날짜 역순으로 해도 되지만, 사용자 확인 편의를 위해 정순으로 정렬 후 저장 (선택적)
            # daily_prices_data.reverse() # 크롤러에서 최신 날짜가 먼저 오므로, DB 저장시 정순으로 하려면 reverse
            db_manager.add_daily_prices_batch(stock_code, daily_prices_data)
        else:
            print(f"종목 [{stock_code}] {stock_name} - 추가할 신규 일별 시세 데이터가 없습니다.")
        
        # 각 종목 크롤링 후 추가적인 전체 딜레이
        if i < len(active_stocks_for_daily_crawl) - 1 : # 마지막 종목이 아니면 대기
            inter_stock_delay = 1.2
            print(f"정보: 다음 종목 처리 전 {inter_stock_delay}초 대기...")
            time.sleep(inter_stock_delay) 

    print("\n모든 작업 완료.")
    db_file_path = os.path.join(os.getcwd(), db_manager.DB_NAME)
    print(f"데이터베이스 파일 '{db_manager.DB_NAME}'이(가) 현재 디렉토리에 저장/업데이트 되었습니다: {db_file_path}")

if __name__ == "__main__":
    main()