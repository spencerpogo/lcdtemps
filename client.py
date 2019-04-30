import get_temps as gt
import os
import sys
import time
import threading
import traceback as tb
import requests

server_url = 'http://192.168.1.65:8080'
frequency = 1 # how often to set in seconds
running = True
s = requests.Session()

def main():
    global paused
    while running:
        start = time.time()
        gt.get_cpu_load()
        params = {
            'cpu_load': gt.get_cpu_load(),
            'gpu_temp': gt.get_gpu_temp(),
            'gpu_load': gt.get_gpu_load(),
            'mem_use': gt.get_mem_use()
        }
        r = s.get(server_url + '/set', params=params)
        taken = time.time() - start
        print('Request took ' + str(taken))
        if taken < frequency:
            time.sleep(frequency - taken) # only sleeps for time
            # still left before next request

main()
