from aiohttp import web
import asyncio
import math
from RPLCD import CharLCD
from RPi import GPIO

async def hello_world(request):
    return web.Response(text='Hello world')

async def c_to_f(celsius):
    return 9.0/5.0 * celsius + 32

async def setup_lcd():
    global lcd
    lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35,
              pins_data=[33, 31, 29, 23])
    lcd.create_char(0, (
        0b01111,
        0b01001,
        0b01001,
        0b01111,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
    ))  # degree symbol
    lcd.write_string('Server Ready! ')

async def reset(request):
    GPIO.cleanup()
    await setup_lcd()
    return web.Response(text='Success')

async def format_line(line, gpu_temp='', mem_use='', gpu_use='', cpu_use=''):
    if line == 'CPU:{cpu_use:.1f}%MEM{mem_use:.1f}%':
        try:
            cpu_use = float(cpu_use)
        except:
            pass
        if type(cpu_use) is float and cpu_use < 10:
            line = line[:18] + ' ' + line[18:]
    return line.format(gpu_temp=gpu_temp, mem_use=mem_use, cpu_use=cpu_use, gpu_use=gpu_use, drg=chr(0))

async def set_temps(request):
    global lcd
    reset = request.query.get('reset', None)
    if reset is not None:
        await reset(None)
    gpu_temp = float(request.query.get('gpu_temp', "-1"))
    gpu_use = float(request.query.get('gpu_load', '-1'))
    cpu_use = float(request.query.get('cpu_load', "-1"))
    mem_use = float(request.query.get('mem_use', "-1"))
    line1 = (await format_line(u'GPU:{gpu_temp:.2f}C {gpu_use:.1f}%',
                               gpu_temp=gpu_temp, gpu_use=gpu_use))[:16]
    line2 = (await format_line(u'CPU:{cpu_use:.1f}%MEM{mem_use:.1f}%', cpu_use=cpu_use, mem_use=mem_use))[:16]
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1)
    lcd.crlf()
    lcd.write_string(line2)
    print(line1 + '\n' + line2)
    return web.Response(text=line1 + '\n' + line2)

async def custom_message(request):
    global lcd
    lcd.write_string(request.query.get('msg', ''))

async def clear(request):
    global lcd
    lcd.clear()
    return web.Response(text="Success")

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(setup_lcd())
        app = web.Application()
        app.add_routes([web.get('/', hello_world),
                        web.get('/set', set_temps),
                        web.get('/clear', clear),
                        web.get('/reset', reset)])
        web.run_app(app)
    finally:
        print('GPIO cleaned up. ')
