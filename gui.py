from guizero import App, Text, PushButton
import os
import time
import threading
import requests # *sigh* async guis are just too hard

server_url = 'http://192.168.1.65:8080'
frequency = 1 # how often to set in seconds
s = requests.Session()

def get_cpu_temp():
    """Returns the CPU temp in celsius. """
    return os.popen("/opt/vc/bin/vcgencmd measure_temp").read().replace("=", " ")[5:-3]

def get_gpu_temp():
    """Returns the GPU temp in celsius. """
    return "25"

def main(mtext):
    while True:
        start = time.time()
        cpu = get_cpu_temp()
        gpu = get_gpu_temp()
        params = {'cpu': cpu, 'gpu': gpu}
        r = s.get(server_url + '/set', params=params)
        mtext.value = r.text
        taken = time.time() - start
        print('Request took ' + str(taken))
        if taken < frequency:
            time.sleep(frequency - taken) # only sleeps for time
            # still left before next request



app = App(title="LCD Temperature", layout="auto", bg="white", width="750")
rtext = Text(app, text="", size=10, color="black")
mtext = Text(app, text="", size=10, color="black")
def reset_lcd():
    r = s.get(server_url + '/reset')
    rtext.value = 'Reset LCD, message was "' + r.text + '"'

button = PushButton(app, command=reset_lcd, text="Reset LCD")
thread = threading.Thread(target=main, args=(mtext,))
thread.start()
app.display()

