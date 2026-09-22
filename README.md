# Bot de Automação de Cotações

Bot em Python para consultar cotações de dólar, euro e bitcoin em relação ao real e enviar notificações automáticas por Telegram. O projeto também inclui alertas de preço, conversão de moedas, histórico de variação e resumo diário para usuários assinados.

> Status: projeto funcional e em evolução, com integração ativa com Telegram e armazenamento local para alertas e assinantes.

## Funcionalidades

- Consulta as cotações atuais de `USD-BRL`, `EUR-BRL` e `BTC-BRL` via AwesomeAPI.
- Formata mensagens legíveis com os valores em reais.
- Envia mensagens diretamente para o Telegram.
- Possui menu interativo com botões no Telegram.
- Permite conversão de valor entre moeda e reais.
- Cria alertas de preço para dólar, euro e bitcoin.
- Exibe variação diária das moedas.
- Permite assinatura de resumo diário às 9h.
- Persiste alertas e assinantes em `dados.json`.
- Suporta execução em modo único (`--once`) para uso rápido em terminal.

## Tecnologias

- Python 3.10+
- `requests` — requisições HTTP
- `python-dotenv` — leitura de variáveis de ambiente
- `python-telegram-bot` — integração com Telegram
- `beautifulsoup4` — suporte para coleta futura ou extensão de rotinas
- `AwesomeAPI` — fonte pública das cotações

## Estrutura do projeto

```text
.
├── .env                 # variáveis de ambiente do Telegram
├── .gitignore           # regras locais do repositório
├── dados.json           # alertas e assinantes persistidos
├── main.py              # ponto de entrada do projeto
├── requirements.txt     # dependências Python
├── README.md            # documentação do projeto
└── src/
    ├── __init__.py
    ├── api.py           # formatação e envio de mensagens
    ├── armazenamento.py # persistência de alertas e assinantes
    ├── bot.py           # comandos e lógica do bot do Telegram
    ├── historico.py     # variação diária das cotações
    ├── scraper.py       # consulta das cotações na API
    └── utils.py         # espaço reservado para utilitários adicionais
```

## Pré-requisitos

- Python 3.10 ou superior
- Acesso à internet para consultar a API de cotações
- Token do bot e ID do chat do Telegram

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/jottasilvasj/bot-automacao.git
cd bot-automacao
```

2. Crie e ative um ambiente virtual:

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente no arquivo `.env`:

```dotenv
TELEGRAM_TOKEN=seu_token_do_bot
TELEGRAM_CHAT_ID=seu_chat_id
```

- `TELEGRAM_TOKEN` é obrigatório para o bot funcionar.
- `TELEGRAM_CHAT_ID` é usado pelo envio direto de mensagens da API e pode ser necessário em rotinas específicas.
- O arquivo `.env` não deve ser versionado em ambientes reais com dados sensíveis.

## Execução

### Bot do Telegram

```bash
python main.py
```

Ao iniciar, o bot fica aguardando comandos no Telegram.

### Modo de execução única

```bash
python main.py --once
```

Esse modo executa uma consulta única e imprime a mensagem no terminal, sem iniciar o bot interativo.

## Comandos do bot

O bot disponibiliza os seguintes comandos:

- `/start` — consulta as cotações atuais
- `/menu` — abre menu com botões de consulta
- `/converter <quantidade> <moeda>` — converte valor em reais
- `/alerta <moeda> <valor>` — cria um alerta de preço
- `/meusalertas` — lista alertas ativos
- `/cancelaralerta <moeda>` — remove um alerta
- `/historico` — mostra variação do dia
- `/assinar` — assina o resumo diário às 9h
- `/cancelar` — cancela a assinatura
- `/ajuda` — exibe a lista de comandos

Exemplos:

```text
/converter 100 USD
/alerta dolar 5.30
/cancelaralerta euro
```

## Como o fluxo funciona

1. `main.py` inicia o bot ou executa o fluxo único.
2. `src/scraper.py` consulta a API da AwesomeAPI:

```text
https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL
```

3. A resposta JSON é convertida em dicionário com as chaves `dolar`, `euro` e `bitcoin`.
4. `src/api.py` formata uma mensagem pronta para envio.
5. `src/bot.py` adiciona comandos, validações e jobs periódicos.
6. `src/armazenamento.py` salva alertas e assinantes em `dados.json`.
7. O bot verifica alertas a cada 5 minutos e envia o resumo diário conforme agendamento.

## Persistência de dados

O arquivo `dados.json` armazena:

```json
{
  "alertas": [],
  "assinantes": []
}
```

- `alertas`: lista de alertas de preço por chat.
- `assinantes`: lista de chats inscritos para o resumo diário.

## Solução de problemas

### `ModuleNotFoundError`

Verifique se o ambiente virtual está ativo e se as dependências foram instaladas:

```bash
pip install -r requirements.txt
```

### Falha ao consultar cotações

Confirme sua conexão com a internet e a disponibilidade da AwesomeAPI. A aplicação usa timeout de 10 segundos e retorna erro caso a API não responda corretamente.

### Bot não responde no Telegram

Verifique se:

- o token do bot foi configurado corretamente no `.env`;
- o bot foi iniciado com `python main.py`;
- o bot já foi criado no Telegram e o token corresponde ao bot correto.

### Mensagem não enviada

Se o valor do `TELEGRAM_TOKEN` ou do `TELEGRAM_CHAT_ID` estiver ausente ou incorreto, a aplicação não conseguirá enviar mensagens.

## Melhorias e próximos passos

- adicionar logs mais estruturados;
- revisar e separar melhor o fluxo de envio direto do fluxo do bot Telegram;
- criar testes automatizados para scraper e formatação de mensagens;
- permitir configuração de moedas e horários por ambiente;
- expandir o suporte para outros canais de notificação além do Telegram;
- criar um padrão de `env.example` para facilitar onboarding de novos colaboradores.

## Licença

Este repositório não possui licença definida no momento. Antes de reutilizar ou redistribuir o código, consulte o proprietário do projeto.
