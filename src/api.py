import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis definidas no ficheiro .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def formatar_mensagem(cotacoes):
    """
    Formata o dicionário de cotações numa mensagem legível.
    """
    if not cotacoes:
        return "⚠️ Não foi possível obter as cotações no momento."

    mensagem = (
        "📊 *RELATÓRIO DIÁRIO DE COTAÇÕES*\n\n"
        f"💵 *Dólar (USD):* R$ {cotacoes['dolar']:.2f}\n"
        f"💶 *Euro (EUR):* R$ {cotacoes['euro']:.2f}\n"
        f"₿ *Bitcoin (BTC):* R$ {cotacoes['bitcoin']:,.2f}\n\n"
        "🤖 *Enviado automaticamente pelo Bot de Automação*"
    )
    return mensagem

def enviar_notificacao(cotacoes):
    """
    Envia a mensagem formatada diretamente para o Telegram.
    """
    mensagem = formatar_mensagem(cotacoes)
    
    # Valida se as variáveis de ambiente foram carregadas corretamente
    if not TOKEN or not CHAT_ID:
        print("⚠️ Token ou Chat ID do Telegram não configurados no .env")
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }

    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        print("🚀 Notificação enviada para o Telegram com sucesso!")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar mensagem para o Telegram: {e}")
        return False

if __name__ == "__main__":
    dados_teste = {
        "dolar": 5.25,
        "euro": 6.10,
        "bitcoin": 250000.00
    }
    enviar_notificacao(dados_teste)