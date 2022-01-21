## Realtime Log Streaming with FastAPI and Server-Sent Events

Artigo original:
https://amittallapragada.github.io/docker/fastapi/python/2020/12/23/server-side-events.html


Este projeto utiliza a https://developer.mozilla.org/pt-BR/docs/Web/API/EventSource

A interface EventSource é usada para receber eventos enviados pelo servidor (server-sent events). Ele se conecta via HTTP em um servidor e recebe eventos com o formato text/event-stream. A conexão permanece aberta até ser fechada chamando EventSource.close() (en-US).

Assim que a conexão estiver aberta, mensagens recebidas do servidor são entregues para o seu código na forma de eventos message.

Ao contrário dos WebSockets, server-sent events são unidirecionais; ou seja, mensagens são entregues em uma direção, do servidor para o cliente (por exemplo, um navegador web). Isso torna-os uma excelente escolha quando **não há** necessidade de enviar mensagens do cliente para o servidor.


# Referências

https://sysid.github.io/sse/

Os eventos enviados pelo servidor fazem parte do padrão HTML, não HTTP 1 . Eles definem um protocolo que é invisível para a camada HTTP e não interrompe nenhuma das camadas inferiores.

Em sua essência, SSE é apenas um **Content-Type** cabeçalho que informa ao cliente que a **resposta será entregue em partes**. Ele também alerta o navegador que ele deve expor cada parte do código à medida que ele chega, e não esperar pela solicitação completa, como os quadros 2 do WebSocket .

No navegador, isso é implementado com a interface fácil de usar **EventSource** no código do lado do cliente:

```js
var source = new EventSource('updates.cgi');
source.onmessage = function (event) {
  alert(event.data);
}

```

2. https://www.starlette.io/responses/

## StreamingResponse

Takes an async generator or a normal generator/iterator and streams the response body.

```py
from starlette.responses import StreamingResponse
import asyncio


async def slow_numbers(minimum, maximum):
    yield('<html><body><ul>')
    for number in range(minimum, maximum + 1):
        yield '<li>%d</li>' % number
        await asyncio.sleep(0.5)
    yield('</ul></body></html>')


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    generator = slow_numbers(1, 10)
    response = StreamingResponse(generator, media_type='text/html')
    await response(scope, receive, send)

```

3. https://www.abrandao.com/2019/04/html5-eventsource-server-sent-events-tutorial/


4. https://www.html5rocks.com/en/tutorials/eventsource/basics/

> Controlling the Reconnection-timeout
The browser attempts to reconnect to the source roughly 3 seconds after each connection is closed. You can change that timeout by including a line beginning with "retry:", followed by the number of milliseconds to wait before trying to reconnect.
Exemplo:

```py
      tempo_de_reconexao = 3000 # 3s
      yield {
          "event": "close",
          "retry": tempo_de_reconexao,
          "data": number,
      }
```


![Demo](/imgs/app_demo.gif?raw=true "Optional Title")


### Como executa-lo?

Utilizando virtualenv:

Crie o ambiente virtual:

```s
python3 -m venv .venv
```

Ative o ambiente virtual:

```s
source .venv/bin/activate
```
Instale os pacotes no ambiente:

```s
pip install -r requirements.txt
```

ou você pode utilizar o Poetry.

# Instalando com Poetry

Basta ativar o ambiente com o comando:

```s
poetry shell
```

```s
poetry install
```

# Rodando o Código

Abra um terminal (não esqueça de ativar o ambiente virtual) para iniciar o gerador de Logs que ficará escrevendo de 0.3s uma linha
no arquivo teste.log:

```s
python gerador_logs.py
```

Em outro terminal (com o ambiente virtual ativado também) rode:

```s
uvicorn app.main:app --reload
```

E por sua vez, abra a página `client.html` no seu browser e verá os eventos acontecendo.

O Html é bem simples! Ao carregar a página o EvenSource se conecta a rota `http://localhost:8000/stream-logs`
que fica enviando
```html
<body>

<h1>Server Logs:</h1>
<div id="logs">
</div>

<script>
  var source = new EventSource("http://localhost:8000/stream-logs");
  source.onmessage = function(event) {
    document.getElementById("logs").innerHTML += event.data + "<br>";
  };
</script>

</body>
</html>
```

# Como funciona?

O servidor tem uma rota associada ao método logGenerator que por sua
vez utiliza um gerador de eventos do pacote `sh` chamado `tail` cuja função
é ficar lendo o arquivo de log e cada linha adicionada nele ele lê a linha
e dispara um evento.
A rota `stream-logs` então retorna o EventSource. E o HTML fica consumindo
estas informações e apresentando na div logs.

```py
async def logGenerator(request):
    status_stream_retry_timeout = 3000 # 3s
    count = 0
    for line in tail("-f", LOGFILE, _iter=True):
```


# NOVO EXEMPLO

Se abrirmos `client/other_example.html` teremos o mesmo princípio que o outro html
só que agora com um pouco de controle.

Para começarmos a receber as mensagens do servidor foi adicionado um botão `Ler Logs`.
Que abrirá a conexão e começará a receber as mensagens.