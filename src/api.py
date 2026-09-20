def formatar_mensagem(cotacoes):
   if not cotacoes:
         return "Não foi possível obter as cotações no momento."

   mensagem = (
        "Cotações atuais:\n"
        f"Dólar: R$ {cotacoes['dolar']}\n"
        f"Euro: R$ {cotacoes['euro']}\n"
        f"Bitcoin: R$ {cotacoes['bitcoin']}\n"
        "Enviado automaticamente pelo bot\n"

    )
   return mensagem

def enviar_notificacao(cotacoes):
     mensagem = formatar_mensagem(cotacoes)
     print("\n--- [MENSAGEM DE NOTIFICAÇÃO GERADA] ---")
     print(mensagem)
     print("-------------------------------------------\n")
     return True

if __name__ == "__main__":
     dados_teste = {
         "dolar": 5.25,
         "euro": 6.10,
         "bitcoin": 250000.00
     }