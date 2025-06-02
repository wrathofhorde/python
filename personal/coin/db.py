import sqlite3

from datetime import datetime
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
		self.conn.commit()
		return cursor

	def fetchall(self, query: str, params: SQLParameters = (), /) -> list[Any]:
		return self.execute(query, params).fetchall()

	def fetchone(self, query: str, params: SQLParameters = (), /) -> Any:
		return self.execute(query, params).fetchone()

	def close(self):
		if self.conn:
			self.conn.close()


majorcoin_table: str = "major_coins"
class CoinPriceDb(Sqlite):
	def __init__(self, db_name):
		super().__init__(db_name)

	def create_major_coins_table(self, table: str = majorcoin_table, /) -> None:
		query: str = f'''
			CREATE TABLE IF NOT EXISTS {table} (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			date TEXT UNIQUE,
			btc INTEGER,
			eth INTEGER,
			xrp INTEGER
			);
		'''
		super().execute(query)

	def count(self, table: str = majorcoin_table, /) -> int:
		key = 'COUNT(*)'
		result = super().fetchone(f"SELECT {key} FROM {table};")
		# COUNT(*)는 'COUNT(*)'라는 이름의 칼럼으로 반환될 수도 있고, 단순히 첫 번째 인덱스(0)로 접근할 수도 있습니다.
		# sqlite3.Row를 사용했기 때문에 'COUNT(*)' 또는 'count(*)'로 접근 가능합니다.
		total_rows = result[key] if key in result.keys() else result[0]

		return total_rows
 
	def insert_major_coin_prices(self, params: SQLParameters, table: str = majorcoin_table, /) -> sqlite3.Cursor:
		query: str = f'''
			INSERT INTO {table} (date, btc, eth, xrp) 
			VALUES (?, ?, ?, ?);
		'''
		return super().excutemany(query, params)
  
	def select_major_coins_prices(self, start_day: str, end_day: str, table: str = majorcoin_table, /) -> list[Any]:
		query: str = f'''
			SELECT date, btc, eth, xrp 
			FROM {table} 
			WHERE date BETWEEN ? AND ? 
			ORDER BY date;
		'''
		rows = super().fetchall(query, (start_day, end_day))

		prices = []

		if rows:
			for row in rows:
				prices.append([row["date"], row["btc"], row["eth"], row["xrp"]])

		return prices
  
	def select_major_coins_data(self, start_day: str, end_day: str, table: str = majorcoin_table, /) -> tuple[Any]:
		query: str = f'''
			SELECT date, btc, eth, xrp 
			FROM {table} 
			WHERE date BETWEEN ? AND ? 
			ORDER BY date;
		'''
		rows = super().fetchall(query, (start_day, end_day))

		if rows:
			date = [datetime.strptime(row["date"], "%Y-%m-%d") for row in rows]
			btc = [row["btc"] for row in rows]
			eth = [row["eth"] for row in rows]
			xrp = [row["xrp"] for row in rows]

			return (date, btc, eth, xrp)

		return ()

	def select_columm_data(self, column: str, start_day: str, end_day: str, table: str = majorcoin_table, /) -> list[Any]:
		query: str = f'''
			SELECT {column}
			FROM {table}
			WHERE date BETWEEN ? AND ? 
			ORDER BY date;
		'''

		rows = super().fetchall(query, (start_day, end_day))
		data = []

		if rows:
			for row in rows:
				data.append(row[column])

		return data
    
	def select_prices_at(self, day:str, table: str = majorcoin_table, /) -> tuple:
		row = super().fetchone(f'''
			SELECT date, btc, eth, xrp 
			FROM {table} 
			WHERE date = "{day}";
		''')

		result = (row["date"], row["btc"], row["eth"], row["xrp"]) if row else ()
		return result

	def select_last_update_major_coins(self, table: str = majorcoin_table, /) -> str:
		key = "MAX(date)"
		result = super().fetchone(f"SELECT {key} FROM {table}")
		lastupdate: str = result[key] if key in result.keys() else result[0]
		return lastupdate

	def select_major_coins_average_price(self, start_day: str, end_day: str, table: str = majorcoin_table, /) -> tuple[int]:
		query: str = f'''
			SELECT 
			AVG(btc) AS avg_btc,
			AVG(eth) AS avg_eth,
			AVG(xrp) AS avg_xrp
			FROM {table} 
			WHERE date BETWEEN ? AND ? ORDER BY date;
		'''
		result = super().fetchone(query, (start_day, end_day))
		return (
			int(round(result["avg_btc"])), 
			int(round(result["avg_eth"])),
			int(round(result["avg_xrp"]))
		)

	def select_major_coins_min_max_avg(self, start_day: str, end_day: str, table: str = majorcoin_table, /) -> tuple[Any]:
		query: str = f'''
			SELECT 
			AVG(btc) AS avg_btc, MAX(btc) AS max_btc, MIN(btc) AS min_btc,
			AVG(eth) AS avg_eth, MAX(eth) AS max_eth, MIN(eth) AS min_eth,
			AVG(xrp) AS avg_xrp, MAX(xrp) AS max_xrp, MIN(xrp) AS min_xrp
			FROM {table} 
			WHERE date BETWEEN ? AND ? 
			ORDER BY date;
		'''

		results = super().fetchone(query, (start_day, end_day))
		print(results)

		return (
			int(round(results["min_btc"])), int(round(results["max_btc"])), int(round(results["avg_btc"])), 
			int(round(results["min_eth"])), int(round(results["max_eth"])), int(round(results["avg_eth"])), 
			int(round(results["min_xrp"])), int(round(results["max_xrp"])), int(round(results["avg_xrp"])), 
		)

def test_crud():
	db = CoinPriceDb("example.db")
	db.create_major_coins_table()

	today_date = "25-05-29"
	btc_price = 70000
	eth_price = 3800 
	xrp_price = 1
	insert_cursor = db.insert_major_coin_prices(
		[(today_date, btc_price, eth_price, xrp_price)]
	)

	print(f"데이터가 성공적으로 삽입되었습니다. ID: {insert_cursor.lastrowid}")

	db.insert_major_coin_prices(
		[
			["25-05-28", 69500, 3750, 0]
		]
	)
	db.insert_major_coin_prices(
		[
			("25-05-27", 69500, 3750, 0),
			("25-05-26", 69500, 3750, 0)
		]
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
