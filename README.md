## Realtime Log Streaming with FastAPI and Server-Sent Events

Artigo original:
https://amittallapragada.github.io/docker/fastapi/python/2020/12/23/server-side-events.html


Este projeto utiliza a https://developer.mozilla.org/pt-BR/docs/Web/API/EventSource

A interface EventSource é usada para receber eventos enviados pelo servidor (server-sent events). Ele se conecta via HTTP em um servidor e recebe eventos com o formato text/event-stream. A conexão permanece aberta até ser fechada chamando EventSource.close() (en-US).

Assim que a conexão estiver aberta, mensagens recebidas do servidor são entregues para o seu código na forma de eventos message.

Ao contrário dos WebSockets, server-sent events são unidirecionais; ou seja, mensagens são entregues em uma direção, do servidor para o cliente (por exemplo, um navegador web). Isso torna-os uma excelente escolha quando **não há** necessidade de enviar mensagens do cliente para o servidor.


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
python server/program.py
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