import aiohttp
import asyncio
import time
import os

server_url = 'http://192.168.1.65:8080'
frequency = 1  # how often to query in seconds

async def get_cpu_temp():
    """Returns the CPU temp in celsius. """
    return os.popen("/opt/vc/bin/vcgencmd measure_temp").read().replace("=", " ")[5:-3]

async def get_gpu_temp():
    """Returns the GPU temp in celsius. """
    return "25"

async def commands():
    print('Commands loop starting. ')
    while True:
        command = input('> ')
        if command.startswith('r'):
            print('Resetting lcd...', end='')
            async with session.get(server_url + '/restart'):
                print('Done. ')
        elif command.startswith('c'):
            print('Clearing lcd...', end='')
            async with session.get(server_url + '/clear'):
                print('Done. ')
    

async def main():
    while True:
        start = time.time()
        cpu = await get_cpu_temp()
        gpu = await get_gpu_temp()
        params = {'cpu': cpu, 'gpu': gpu}
        async with session.get(server_url + '/set', params=params) as r:
            #await r.text()
            print(await r.text())
        taken = time.time() - start
        if taken < frequency:
            time.sleep(frequency - taken) # only sleeps for time
            # still left before next request
    
if __name__ == "__main__":
    try:
        session = aiohttp.ClientSession()
        loop = asyncio.get_event_loop()
        loop.create_task(commands())
        loop.run_until_complete(main())
    finally:
        asyncio.get_event_loop().run_until_complete(session.close())
