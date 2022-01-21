"""
server.py
This script will launch a web server on port 8000 which sends SSE events anytime
logs are added to our log file.
"""

from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from datetime import datetime
from sh import tail
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import asyncio
import uuid

#create our app instance
app = FastAPI()

#add CORS so our web page can connect to our api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = f"{dir_path}/logs/log_gerado.log"

#This async generator will listen to our log file in an infinite while loop (happens in the tail command)
#Anytime the generator detects a new line in the log file, it will yield it.
# Este gerador assincrono fica lendo o arquivo log infinitamente
# Assim que o gerador detecta uma nova linha ele irá produzí-la
async def leitor_de_logs(request, close_by_server: False):
    tempo_de_reconexao = 3000 # 3s
    count = 0
    for line in tail("-f", LOGFILE, _iter=True):
        if await request.is_disconnected():
            print("="*80)
            print("client disconnected!!!")
            print("="*80)
            break
        count += 1
        yield line

        if count == 2:
            yield {
                "event": "evento_avisar",
                "retry": tempo_de_reconexao,
                "data": "Segunda Iteração! Exemplo de Evento!",
            }

        if close_by_server:
            if count == 50:
                yield {"event": "closed", "data": "Finalizei a leitura do Log"}
                yield {
                    "event": "fechado_pelo_servidor",
                    "retry": tempo_de_reconexao,
                    "data": "Finalizado o envio de mensagem pelo servidor!!",
                }
                # Sai do Loop infinito
                break
        time.sleep(0.5)

# Este gerador assincrono fica produz
# mensagems que serão consumidas pelo Cliente
async def gerador_numeros(minimum, maximum, request):
    tempo_de_reconexao = 3000 # 3s
    for number in range(minimum, maximum + 1):
        yield {
            "event": "message",
            "retry": tempo_de_reconexao,
            "data": number,
        }
        print(f"{number} publicado as {datetime.now()}")
        await asyncio.sleep(0.3)
        if await request.is_disconnected():
            print("="*80)
            print("client disconnected!!!")
            print("="*80)
            break
        if number == maximum:
            yield {
                "event": "closed",
                "retry": tempo_de_reconexao,
                "data": number,
            }
            break

# Esta rota fica lendo os Números e envia para os Clientes
@app.get('/stream-numbers')
async def send_stream_numbers(request: Request):
    evento = gerador_numeros(1, 10, request)
    return EventSourceResponse(evento)


# Esta rota faz a leitura do arquivo de logs
@app.get('/stream-logs')
async def send_stream_log(request: Request):
    event_generator = leitor_de_logs(request, close_by_server=False)
    return EventSourceResponse(event_generator)
