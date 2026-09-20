from src.scraper import obter_cotacoes
from src.api import enviar_notificacao

def executar_bot():
    print("Iniciando o bot de cotações...")
    dados_cotacoes = obter_cotacoes()
    if dados_cotacoes:
        enviar_notificacao(dados_cotacoes)
        print("fluxo executado com sucesso!")
    else:
        print("Falha ao obter cotações. Notificação não enviada.")

if __name__ == "__main__":
    executar_bot()