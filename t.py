import time
import threading
from workers.SleepWorkers import SleepWorker
from workers.SquareSumWorkers import SquareSumWorkers

def main():
    calc_start_time = time.time()

    calculate_threads = []
    for seconds in range(5):
        maximum_value = (seconds + 1) * 1000
        squareSumWorker = SquareSumWorkers(n=maximum_value)
        calculate_threads.append(squareSumWorker)
    
    for seconds in range(len(calculate_threads)):
        calculate_threads[seconds].join()


    print("Calculating sum of squares took: ", round(time.time() - calc_start_time, 1))
    
    sleep_threads = []
    sleep_start_time = time.time()
    for seconds in range(1,6):
        sleepWorker = SleepWorker(seconds=seconds)
        sleep_threads.append(sleepWorker)
    
    
    for sp in range(len(sleep_threads)):
        sleep_threads[sp].join()
        
    print("Sleeping took: ", round(time.time() - sleep_start_time, 1))


if __name__ == "__main__":
    main()
