# lcdtemps
### Client and server to show temps on an LCD with Raspberry Pi
This is a library I wrote to connect my raspberry pi to show my PC's temps on a 16x2 LCD I had lying around. 
For the wiring,. I used this page http://www.circuitbasics.com/raspberry-pi-lcd-set-up-and-programming-in-python/ which had this diagram for the wiring: 
![Fritzing Wiring Diagram](https://i.imgur.com/y7a0XFB.png)
To setup do the following:
1. Download the lcd_server.py file onto your Raspberry Pi, install the dependencies, run it, and grab its IP address. 
2. Download the gui_client.py onto your PC. 
3. Update the server_url variable in your client with the Pi's IP address. 
4. Update the client's get_cpu_temp and get_gpu_temp functions to suit your machine. 
5. Run the GUI. The temperatures should automatically update every second and if you bump the cable, just hit the Reset LCD button to refresh the GPIO without restarting the server!

Hope this helps!
**Made by [@Scoder12](https://github.com/@Scoder12)**
