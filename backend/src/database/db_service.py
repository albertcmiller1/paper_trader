import sqlite3, os
# from models import Match, Price
# from schemas import PRICE_HISTORY_DB, MATCH_HISTORY_DB

from database.models import Match, Price
from database.schemas import PRICE_HISTORY_DB, MATCH_HISTORY_DB

class DB_Service: 
    def __init__(self):
        working_dir = os.path.dirname(os.path.realpath(__file__))
        self.tables = {
            "PRICE_HISTORY": f"{working_dir}/tables/price_history.db",
            "MATCH_HISTORY": f"{working_dir}/tables/match_history.db"
        }
        self.create_all_tables()
        for table in self.tables: 
            self.truncate_table(table)

    def create_all_tables(self):
        for table_name, schema in [PRICE_HISTORY_DB, MATCH_HISTORY_DB]:
            self.create_table(self.tables[table_name], schema)

    def create_table(self, table_name, schema):
        conn = sqlite3.connect(table_name)
        conn.execute(schema)
        conn.close()

    def truncate_table(self, table_name):
        conn = sqlite3.connect(self.tables[table_name])
        conn.execute(f"DELETE FROM {table_name};")
        conn.close()


    def insert(self, ins_obj):
        table_name, insert_query = self.build_insert_query(ins_obj)
        conn = sqlite3.connect(self.tables[table_name])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e: 
            print(f"Unable to create new record. error: {e}")
        conn.close()

    def build_insert_query(self, insertion_obj):
        if isinstance(insertion_obj, Price):
            return "PRICE_HISTORY", f"INSERT INTO PRICE_HISTORY (TIME,TICKER,PRICE) VALUES ({insertion_obj.time}, '{insertion_obj.ticker}', {insertion_obj.price})"
        elif isinstance(insertion_obj, Match):
            return "MATCH_HISTORY", f"INSERT INTO MATCH_HISTORY (MATCH_ID,BUYER_ORDER_ID,SELLER_ORDER_ID,SALE_QUANTITY,SALE_PRICE) VALUES ({insertion_obj.match_id}, '{insertion_obj.buyer_order_id}', '{insertion_obj.seller_order_id}', {insertion_obj.sale_quantity}, {insertion_obj.sale_price})"
        else: 
            raise ValueError(f"Unknown object type: {type(insertion_obj)}")

    def select(self, table_name):
        # cursor = conn.execute("SELECT id, name, address, salary from COMPANY WHERE id=2")
        conn = sqlite3.connect(self.tables.get(table_name, None))
        cursor = conn.execute(self.build_select_query(table_name))
        arr = [row for row in cursor]
        conn.close()
        return arr

    def build_select_query(self, table):
        if table=="PRICE_HISTORY":
            return f"SELECT time, ticker, price from PRICE_HISTORY"
        elif table=="MATCH_HISTORY":
            return f"SELECT match_id, buyer_order_id, seller_order_id, sale_quantity, sale_price from MATCH_HISTORY"
        else: 
            raise ValueError(f"Unknown table: {table}")

if __name__ == "__main__":
    db = DB_Service()

    p1 = Price(123122242, "AAPL", 100)
    p2 = Price(12346, "AAPL", 199)
    db.insert(p1)
    db.insert(p2)
    db.select("PRICE_HISTORY")

    m1 = Match(123, '02ed979a1f', '1f08f10fe6', 2, 100.2)
    db.insert(m1)
    db.select("MATCH_HISTORY")
