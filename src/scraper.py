import requests

def obter_cotacoes():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()  # Levanta um erro se a resposta não for bem-sucedida   
        dados = resposta.json()

        cotacoes = {
            "dolar": round(float(dados["USDBRL"]["bid"]), 2),
            "euro": round(float(dados["EURBRL"]["bid"]), 2),
            "bitcoin": round(float(dados["BTCBRL"]["bid"]), 2)
        }
        return cotacoes

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter cotações: {e}")
        return None

    if __name__ == "__main__":
        resultado = obter_cotacoes()
        print ("Cotações obtidas extraidas com sucesso:")
        print(resultado)