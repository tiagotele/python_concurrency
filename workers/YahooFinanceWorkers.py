import datetime
from queue import Empty
import random
import threading
import time

import requests
from lxml import html

class YahooFinanceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        super(YahooFinanceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]
        self._output_queues = temp_queue
        self.start()
        
    def run(self):
        while True:
            try:
                val = self._input_queue.get(timeout=10)
            except Empty:
                print("Yahoo scheduler queue is empty")
            if val == "DONE":
                for output_queue in self._output_queues:
                    output_queue.put("DONE")
                break
            
            yahooFinancePriceWorker = YahooFinanceWorkers(symbol=val)
            price = yahooFinancePriceWorker.get_price()
            for output_queue in self._output_queues:
                values = (val, price, datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S'))
                output_queue.put(values)
            # print(price)
            time.sleep(random.random())

class YahooFinanceWorkers():
    
    def __init__(self, symbol):
        super(YahooFinanceWorkers, self).__init__()
        self._symbol = symbol
        base_url = 'https://finance.yahoo.com/quote/'
        self._url = f'{base_url}{self._symbol}'
    
    
    def get_price(self):
        print(f"request to = {self._url}")
        time.sleep(25 * random.random())
        r = requests.get(self._url, headers= {'User-agent': 'your bot 0.1'})
        if r.status_code != 200:
            print(f"status code = {r.status_code}")
            return
        page_contents = html.fromstring(r.text)
        price = -1
        if len(page_contents.xpath('//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/div[1]/span')) > 0:
            price = float(page_contents.xpath('//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/div[1]/span')[0].text)
        return price

if __name__ == "__main__":
    y = YahooFinanceWorkers(symbol="AOS")
    # y.join()