"""
Consulta de variação diária das cotações via AwesomeAPI.
"""
import requests

URL_BASE = "https://economia.awesomeapi.com.br/json"


def obter_variacao_diaria():
    """Retorna valor atual e variação percentual do dia para dólar, euro e bitcoin."""
    try:
        resposta = requests.get(f"{URL_BASE}/last/USD-BRL,EUR-BRL,BTC-BRL", timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        return {
            "dolar": {
                "valor": float(dados["USDBRL"]["bid"]),
                "variacao_pct": float(dados["USDBRL"]["pctChange"]),
            },
            "euro": {
                "valor": float(dados["EURBRL"]["bid"]),
                "variacao_pct": float(dados["EURBRL"]["pctChange"]),
            },
            "bitcoin": {
                "valor": float(dados["BTCBRL"]["bid"]),
                "variacao_pct": float(dados["BTCBRL"]["pctChange"]),
            },
        }
    except requests.RequestException:
        return None