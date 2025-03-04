import os
import threading

from sqlalchemy import create_engine, text

class PostgresMasterShedulerWorker(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(PostgresMasterShedulerWorker, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()
    
    def run(self):
        while(True):
            val = self._input_queue.get()
            if val == "DONE":
                break
            
            symbol, price, extracted_time = val
            postgresWorker = PostgresWorker(symbol, price, extracted_time)
            postgresWorker.insert_into_db()

class PostgresWorker():
    def __init__(self, symbol, price, extracted_time) -> None:
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time
        
        self._PG_USER = os.getenv("PG_USER")
        self._PG_PW = os.getenv("PG_PW")
        self._PG_HOST = os.getenv("PG_HOST")
        self._PG_DB = os.getenv("PG_DB")
        
        self._engine = create_engine(f'postgresql://{self._PG_USER}:{self._PG_PW}@{self._PG_HOST}/{self._PG_DB}')
    
    def _create_insert_query(self):
        SQL = f"""INSERT INTO prices (symbol, price, extracted_time) VALUES (:symbol, :price, :extracted_time)"""
        return SQL
    
    def insert_into_db(self):
        insert_query = self._create_insert_query()
        
        with self._engine.connect() as conn:
            conn.execute(text(insert_query), { 'symbol': self._symbol,
                                                'price': self._price,
                                                'extracted_time': self._extracted_time})
            conn.commit()
    
if __name__ == "__main__":
    p = PostgresWorker("TEST", 10.12, '2025-03-04 17:52:56')
    print(p._engine)
    p.insert_into_db()
    