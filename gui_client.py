from guizero import App, Text, PushButton
from get_temps import *
import os
import sys
import time
import threading
import traceback as tb
import requests # *sigh* async guis are just too hard

server_url = 'http://192.168.1.65:8080'
frequency = 1 # how often to set in seconds
paused = False
running = True
s = requests.Session()

def main(mtext):
    global paused
    try:
        while running:
            if paused:
                if time.time() < paused:
                    mtext.value = 'PAUSED'
                    time.sleep(0.1)
                else:
                    paused = False
                continue
            start = time.time()
            cpu = get_cpu_temp()
            gpu = get_gpu_temp()
            params = {'cpu': cpu.get_temp(), 'gpu': gpu.get_temp()}
            r = s.get(server_url + '/set', params=params)
            mtext.value = r.text
            taken = time.time() - start
            print('Request took ' + str(taken))
            if taken < frequency:
                time.sleep(frequency - taken) # only sleeps for time
                # still left before next request
    except:
        print('Caugth exception in thread, exiting...')
        tb.print_exc()
        sys.exit(1)

def clear_after(item, seconds):
    time.sleep(seconds)
    item.value = ''

app = App(title="LCD Temperature", layout="auto", bg="white", width="750")
rtext = Text(app, text="", size=10, color="black")
mtext = Text(app, text="", size=10, color="black")
def reset_lcd():
    paused = time.time() + float('inf') # sleep until we reset
    r = s.get(server_url + '/reset')
    rtext.value = 'Reset LCD, message was "' + r.text + '"'
    paused = time.time() + 0.3 # sleep for 0.3 more seconds
    threading.Thread(target=clear_after, args=(rtext, 1.5)).start()

def start_stop():
    global paused
    if paused:
        try:
            start_stop_button.text = 'Stop'
        except:
            pass
        paused = False
    elif not paused:
        try:
            start_stop_button.text = 'Start'
        except:
            pass
        paused = True

reset_button = PushButton(app, command=reset_lcd, text="Reset LCD")
start_stop_button = PushButton(app, command=start_stop, text='Stop')
thread = threading.Thread(target=main, args=(mtext,))
thread.start()
app.display()
