import psutil
import platform
from datetime import datetime
import time
import asyncio
import json

async def main():
    # it = 0
    while True:
        # cpu_contagem = psutil.cpu_count(logical=False)
        # cpu_nucleos = psutil.cpu_count(logical=True)
        # dict_cpu = {"contagem": cpu_contagem, "nucleos": cpu_nucleos,
        #             "porcentagem": cpu_porcentagem}
        cpu_porcentagem = psutil.cpu_percent()
        dict_cpu = {"porcentagem": cpu_porcentagem * 10.}
        yield {
            "event": "msg_cpu",
            "retry": 3000, # tempo de reconexão - 3000 ms
            "data": json.dumps(dict_cpu),
        }
        await asyncio.sleep(0.5)