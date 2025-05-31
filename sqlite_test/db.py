import sqlite3
from typing import Any, List, Tuple, TypeAlias, Union

SQLParameters: TypeAlias = Union[Tuple[Any, ...], List[Any]]

class Sqlite:
  def __init__(self, db_name:str):
    # 파일 기반 데이터베이스 연결 (파일이 없으면 생성됨)
    self.conn = sqlite3.connect(db_name)
    # 쿼리 결과의 각 행이 인덱스(숫자)뿐만 아니라 칼럼 이름으로도 접근 가능한 객체로 반환
    # 딕셔너리처럼 작동하여 row['id'] 또는 row['name']과 같이 칼럼 이름으로 데이터에 접근
    self.conn.row_factory = sqlite3.Row

  def execute(self, query: str, params: SQLParameters = (), /) -> sqlite3.Cursor:
    # 반환된 Cursor 객체를 사용하여 다음과 같은 작업을 수행할 수 있습니다.
    # SELECT 쿼리의 결과를 가져옵니다 (fetchone(), fetchall(), fetchmany()).
    # INSERT, UPDATE, DELETE 쿼리가 영향을 미친 행의 수를 확인합니다 (rowcount).
    # INSERT 쿼리로 삽입된 마지막 행의 ID를 얻습니다 (lastrowid).
    cursor: sqlite3.Cursor = self.conn.execute(query, params)
    self.conn.commit()
    return cursor
  
  def excutemany(self, query: str, params : List[SQLParameters], /) -> sqlite3.Cursor:
    cursor: sqlite3.Cursor = self.conn.executemany(query, params)
    self.conn.commit
    return cursor

  def fetchall(self, query: str, params: SQLParameters = (), /):
    cursor = self.execute(query, params)
    return cursor.fetchall()
  
  def fetchone(self, query: str, params: SQLParameters = (), /):
    cursor = self.execute(query, params)
    return cursor.fetchone()
  
  def count(self, table: str):
    result = self.fetchone(f"SELECT COUNT(*) FROM {table}")
    print(type(result))
    # COUNT(*)는 'COUNT(*)'라는 이름의 칼럼으로 반환될 수도 있고, 단순히 첫 번째 인덱스(0)로 접근할 수도 있습니다.
    # sqlite3.Row를 사용했기 때문에 'COUNT(*)' 또는 'count(*)'로 접근 가능합니다.
    total_rows = result['COUNT(*)'] if 'COUNT(*)' in result.keys() else result[0]
    
    return total_rows
  
  def close(self):
    if self.conn:
      self.conn.close()

def test_crud():
  db = Sqlite("example.db")
  db.execute('''
      CREATE TABLE IF NOT EXISTS major_coins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        btc INTEGER,
        eth INTEGER,
        xrp INTEGER
      );
  ''')

  today_date = "25-05-29"
  btc_price = 70000
  eth_price = 3800 
  xrp_price = 1
  insert_cursor = db.execute(
          "INSERT INTO major_coins (date, btc, eth, xrp) VALUES (?, ?, ?, ?);",
          (today_date, btc_price, eth_price, xrp_price)
      )

  print(f"데이터가 성공적으로 삽입되었습니다. ID: {insert_cursor.lastrowid}")

  db.execute(
      "INSERT INTO major_coins (date, btc, eth, xrp) VALUES (?, ?, ?, ?);",
      ["25-05-28", 69500, 3750, 0]
  )
  print("추가 데이터 삽입 완료.")

  print("\n--- 삽입된 데이터 확인 ---")
  rows = db.execute("SELECT * FROM major_coins;").fetchall()
  if rows:
      for row in rows:
          # sqlite3.Row 덕분에 칼럼 이름으로 접근 가능
          print(f"ID: {row['id']}, 날짜: {row['date']}, BTC: {row['btc']}, ETH: {row['eth']}, XRP: {row['xrp']}")
  else:
      print("데이터가 없습니다.")

  db.close()
  print("\n데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
  try:
    test_crud()
  except Exception as e:
    print(f"데이터베이스 오류 발생: {e}")
