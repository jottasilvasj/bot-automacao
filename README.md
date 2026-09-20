# Bot de Automação de Cotações

Bot em Python que consulta cotações de dólar, euro e Bitcoin em relação ao real brasileiro e gera uma mensagem de notificação com os valores obtidos.

> **Status:** projeto em desenvolvimento. Atualmente, a notificação é exibida no terminal; não há integração configurada com um serviço externo de mensagens.

## Funcionalidades

- Consulta as cotações de `USD-BRL`, `EUR-BRL` e `BTC-BRL`.
- Consome a API pública [AwesomeAPI](https://economia.awesomeapi.com.br/).
- Converte os valores recebidos para números com duas casas decimais.
- Formata uma mensagem em português com as cotações.
- Trata erros de rede e evita o envio da notificação quando a consulta falha.

## Tecnologias

- Python 3.10 ou superior recomendado
- `requests` — requisições HTTP
- `beautifulsoup4` — disponível nas dependências para futuras rotinas de coleta
- `python-dotenv` — disponível para configuração por variáveis de ambiente

## Estrutura do projeto

```text
.
├── main.py              # Ponto de entrada e orquestração do fluxo
├── requirements.txt     # Dependências Python
└── src/
    ├── __init__.py
    ├── api.py            # Formatação e saída da notificação
    ├── scraper.py        # Consulta e interpretação das cotações
    └── utils.py           # Utilitários (reservado para extensões)
```

## Pré-requisitos

- Python instalado — confirme com `python --version` ou `python3 --version`.
- Acesso à internet para consultar a AwesomeAPI.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/jottasilvasj/bot-automacao.git
   cd bot-automacao
   ```

2. Crie e ative um ambiente virtual:

   **Linux/macOS**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows (PowerShell)**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Execução

Para executar o fluxo completo:

```bash
python main.py
```

Saída esperada em caso de sucesso:

```text
Iniciando o bot de cotações...

--- [MENSAGEM DE NOTIFICAÇÃO GERADA] ---
Cotações atuais:
Dólar: R$ 5.25
Euro: R$ 6.10
Bitcoin: R$ 250000.0
Enviado automaticamente pelo bot
-------------------------------------------

fluxo executado com sucesso!
```

Os valores são dinâmicos e podem variar conforme o mercado e o momento da consulta.

## Como o fluxo funciona

1. `main.py` chama `obter_cotacoes()`.
2. `src/scraper.py` faz uma requisição `GET` para:

   ```text
   https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL
   ```

3. A resposta JSON é convertida para um dicionário com as chaves `dolar`, `euro` e `bitcoin`.
4. `src/api.py` formata os dados em uma mensagem.
5. A mensagem é impressa no terminal por `enviar_notificacao()`.

A requisição possui timeout de 10 segundos. Em caso de falha HTTP ou de conexão, o bot informa o erro e não tenta gerar uma notificação com dados inválidos.

## Uso dos módulos

Consulta direta das cotações:

```python
from src.scraper import obter_cotacoes

cotacoes = obter_cotacoes()
print(cotacoes)
```

Formatação de uma mensagem:

```python
from src.api import formatar_mensagem

mensagem = formatar_mensagem({
    "dolar": 5.25,
    "euro": 6.10,
    "bitcoin": 250000.00,
})
print(mensagem)
```

## Configuração

O projeto contém um arquivo `.env`, mas a versão atual não depende de variáveis de ambiente para executar a consulta ou gerar a notificação. Caso seja adicionada uma integração externa — por exemplo, Telegram, WhatsApp, e-mail ou Discord — recomenda-se armazenar tokens e chaves no `.env` e nunca versionar credenciais.

Exemplo de configuração futura:

```env
NOTIFICATION_TOKEN=seu-token-aqui
NOTIFICATION_CHAT_ID=seu-destino-aqui
```

## Desenvolvimento e melhorias planejadas

- Integrar a notificação com um canal externo.
- Adicionar testes automatizados para o scraper e o formatador.
- Validar alterações no formato da resposta da API.
- Adicionar logging estruturado no lugar de `print`.
- Permitir configurar moedas, destino da mensagem e intervalo de execução.
- Criar uma execução agendada com cron, Task Scheduler ou GitHub Actions.
- Adicionar um ` .gitignore` com ambiente virtual, cache do Python e arquivos de configuração local, caso ainda não exista uma política equivalente no projeto.

## Solução de problemas

### `ModuleNotFoundError`

Verifique se o ambiente virtual está ativo e instale as dependências:

```bash
pip install -r requirements.txt
```

### Falha ao obter cotações

Confirme sua conexão com a internet e se a AwesomeAPI está acessível. A aplicação usa timeout de 10 segundos e retorna `None` quando ocorre um erro de requisição.

### A mensagem não é enviada para um aplicativo

Esse comportamento é esperado na implementação atual: `enviar_notificacao()` apenas imprime a mensagem no terminal. É necessário implementar um cliente para o serviço escolhido.

## Licença

Nenhuma licença foi definida no repositório até o momento. Consulte o proprietário antes de reutilizar ou distribuir o código em outros projetos.
