from guizero import App, Text, PushButton
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

class Temperature:
    """Represents a temperature in celsius. """
    def __init__(self, f=None, c=None):
        if f is None and c is None:
            raise TypeError('Either fahrenheit or celcius should have a value. ')
        elif f is not None and c is not None:
            raise TypeError('Specify a value for eith celsius or fahrenheit, not both. ')
        elif f is not None and c is None:
            self.c = Temperature.f_to_c(float(f))
        elif c is not None and f is None:
            self.c = float(c)
        else:
            raise TypeError('oof f is ' + str(f) + 'c is ' + str(c))
    
    def get_temp(self):
        return float(self.c)
    
    def f_to_c(f):
        return (f - 32) * 5.0/9.0

def get_cpu_temp():
    """Returns the CPU temp in celsius. """
    return Temperature(c=
        os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        .replace("=", " ")[5:-3])

def get_gpu_temp():
    """Returns the GPU temp in celsius. """
    return Temperature(f="80")

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

button = PushButton(app, command=reset_lcd, text="Reset LCD")
thread = threading.Thread(target=main, args=(mtext,))
thread.start()
app.display()

