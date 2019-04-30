# lcdtemps
### Client and server to show temps on an LCD with Raspberry Pi
This is a library I wrote to connect my raspberry pi to show my PC's temps on a 16x2 LCD I had lying around. 
For the wiring,. I used this page http://www.circuitbasics.com/raspberry-pi-lcd-set-up-and-programming-in-python/ which had this diagram for the wiring: 
![Fritzing Wiring Diagram](https://i.imgur.com/y7a0XFB.png)
To setup do the following:
1. Install `aiohttp` and download the lcd_server.py file onto your Raspberry Pi, grab its ip address, and run it. (You may want to put it in `/etc/rc.local` as well so it runs on bootup).
2. Download the `client.py` file and the `requests` module onto your PC. 
3. Update the server_url variable in your client with the Pi's IP address. 
4. Setup your `get_temps.py` file. If you are running windows, use [windows setup instructions](#Windows-setup)
5. Run the client. The temperatures should automatically update every second and if you bump the cable, just hit the Reset LCD button to refresh the GPIO without restarting the server!

#### Windows setup
Just populate the function with a method of retrieving the temperatures for you system. If you are running windows, you can use the provided function without modifing them, but you need to have [Open Hardware Monitor](https://openhardwaremonitor.org/downloads/) running (I'd use minimize to try though) and the `wmi` module to communicate with it. Also only with windows you can use the provided `start.bat` and `stop.bat` file to control it. These use `pythonw` so it is fine to just close the cmd window that opens.
Hope this helps!
**Made by [@Scoder12](https://github.com/@Scoder12)**
