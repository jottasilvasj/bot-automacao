import sys

from src.scraper import obter_cotacoes
from src.api import enviar_notificacao
from src.bot import main as iniciar_bot_telegram


def executar_bot_uma_vez():
    """Fluxo original: consulta as cotações uma única vez e imprime no terminal."""
    print("Iniciando o bot de cotações...")
    dados_cotacoes = obter_cotacoes()
    if dados_cotacoes:
        enviar_notificacao(dados_cotacoes)
        print("fluxo executado com sucesso!")
    else:
        print("Falha ao obter cotações. Notificação não enviada.")


if __name__ == "__main__":
    if "--once" in sys.argv:
        executar_bot_uma_vez()
    else:
        iniciar_bot_telegram()