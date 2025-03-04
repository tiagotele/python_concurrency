import random
import threading
import time
import requests
from lxml import html

class YahooFinanceScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(YahooFinanceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()
        
    def run(self):
        while True:
            val = self._input_queue.get()
            if val == "DONE":
                break
            
            yahooFinancePriceWorker = YahooFinanceWorkers(symbol=val)
            price = yahooFinancePriceWorker.get_price()
            print(price)
            time.sleep(random.random())

class YahooFinanceWorkers():
    
    def __init__(self, symbol, **kwargs):
        super(YahooFinanceWorkers, self).__init__(**kwargs)
        self._symbol = symbol
        base_url = 'https://finance.yahoo.com/quote/'
        self._url = f'{base_url}{self._symbol}'
    
    
    def get_price(self):
        print(f"running, url ={self._url}")
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
    y.join()