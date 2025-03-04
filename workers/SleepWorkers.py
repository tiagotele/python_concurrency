import threading
import time


class SleepWorker(threading.Thread):
    def __init__(self, seconds, **kwargs):
        super(SleepWorker, self).__init__(**kwargs)
        self._seconds = seconds
        self.daemon = False
        self.start()

    def _sleep_a_little(self):
        time.sleep(self._seconds)

    def run(self):
        self._sleep_a_little()
