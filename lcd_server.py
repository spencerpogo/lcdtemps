from aiohttp import web
import asyncio
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
    ))

async def reset(request):
    GPIO.cleanup()
    await setup_lcd()
    return web.Response(text='Success')

async def set_temps(request):
    reset = request.query.get('reset', None)
    if reset is not None:
        await reset(None)
    gpu_c = request.query.get('gpu', "?")
    gpu_f = '?'
    cpu_c = request.query.get('cpu', "?")
    gpu_f = '?'
    try:
        gpu_c = float(gpu_c)
        gpu_f = await c_to_f(gpu_c)
    except ValueError:  # catch error and leave values to default
        pass
    try:
        cpu_c = float(cpu_c)
        cpu_f = await c_to_f(cpu_c)
    except ValueError:  # catch error and leave values to default
        pass
    text = u'GPU:{gpu_c:.1f}C {gpu_f:.2f}F\r\nCPU:{cpu_c:.1f}C \
{cpu_f:.2f}F'.format(gpu_c=gpu_c,
                       cpu_c=cpu_c,
                       gpu_f=gpu_f,
                       cpu_f=cpu_f)
    lcd.clear()
    lcd.write_string(text.replace('<o>', chr(0)))
    print(text)
    return web.Response(text=text)

async def clear(request):
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
