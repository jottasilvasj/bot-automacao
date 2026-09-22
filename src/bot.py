"""
Bot do Telegram: cotações, conversor, alertas de preço, botões interativos,
resumo diário automático e histórico de variação.
"""
import logging
import os
from datetime import time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from src.scraper import obter_cotacoes
from src.api import formatar_mensagem
from src.historico import obter_variacao_diaria
from src.armazenamento import (
    adicionar_alerta,
    listar_alertas,
    remover_alerta,
    adicionar_assinante,
    remover_assinante,
    listar_assinantes,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MOEDAS_SUPORTADAS = {
    "usd": "dolar", "dolar": "dolar", "dólar": "dolar",
    "eur": "euro", "euro": "euro",
    "btc": "bitcoin", "bitcoin": "bitcoin",
}


# ---------- Comandos básicos ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await update.message.reply_text("Buscando as cotações, aguarde um instante...")

    dados_cotacoes = obter_cotacoes()
    if dados_cotacoes:
        mensagem = formatar_mensagem(dados_cotacoes)
        await context.bot.send_message(chat_id=chat_id, text=mensagem)
        await context.bot.send_message(
            chat_id=chat_id, text="Digite /ajuda para ver tudo que eu sei fazer."
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Não foi possível obter as cotações no momento. Tente novamente em instantes.",
        )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = (
        "Comandos disponíveis:\n\n"
        "/start - cotações atuais (dólar, euro, bitcoin)\n"
        "/menu - menu com botões\n"
        "/converter quantidade/moedas - ex: /converter 100 USD\n"
        "/alerta moeda/valor - ex: /alerta dolar/5.30\n"
        "/meusalertas - lista seus alertas ativos\n"
        "/cancelaralerta moeda - cancela um alerta\n"
        "/historico - variação de hoje\n"
        "/assinar - recebe o resumo diário às 9h\n"
        "/cancelar - cancela o resumo diário\n"
        "/ajuda - mostra esta mensagem"
    )
    await update.message.reply_text(texto)


# ---------- Menu com botões ----------

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    teclado = [
        [
            InlineKeyboardButton("Dólar (USD)", callback_data="cot_dolar"),
            InlineKeyboardButton("Euro (EUR)", callback_data="cot_euro"),
        ],
        [
            InlineKeyboardButton("Bitcoin (BTC)", callback_data="cot_bitcoin"),
            InlineKeyboardButton("Todas", callback_data="cot_todas"),
        ],
    ]
    await update.message.reply_text(
        "O que você quer consultar?", reply_markup=InlineKeyboardMarkup(teclado)
    )


async def botao_cotacao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    dados_cotacoes = obter_cotacoes()
    if not dados_cotacoes:
        await query.edit_message_text("Não consegui consultar a cotação agora.")
        return

    escolha = query.data.replace("cot_", "")

    if escolha == "todas":
        mensagem = formatar_mensagem(dados_cotacoes)
    else:
        nomes = {"dolar": "Dólar", "euro": "Euro", "bitcoin": "Bitcoin"}
        mensagem = f"{nomes[escolha]}: R$ {dados_cotacoes[escolha]:.2f}"

    await query.edit_message_text(mensagem)


# ---------- Conversor ----------

async def converter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text(
            "Uso: /converter <quantidade> <moeda>\nExemplo: /converter 100 USD"
        )
        return

    quantia_bruta, moeda_bruta = context.args
    moeda = MOEDAS_SUPORTADAS.get(moeda_bruta.lower())

    if not moeda:
        await update.message.reply_text(
            "Moeda não reconhecida. Use: USD, EUR ou BTC."
        )
        return

    try:
        quantia = float(quantia_bruta.replace(",", "."))
    except ValueError:
        await update.message.reply_text("Quantidade inválida. Exemplo: /converter 100 USD")
        return

    dados_cotacoes = obter_cotacoes()
    if not dados_cotacoes:
        await update.message.reply_text("Não consegui consultar a cotação agora. Tente novamente.")
        return

    total_em_reais = quantia * dados_cotacoes[moeda]
    await update.message.reply_text(
        f"{quantia:.2f} {moeda_bruta.upper()} = R$ {total_em_reais:.2f}"
    )


# ---------- Alertas de preço ----------

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    if len(context.args) != 2:
        await update.message.reply_text(
            "Uso: /alerta <moeda> <valor>\nExemplo: /alerta dolar 5.30"
        )
        return

    moeda_bruta, valor_bruto = context.args
    moeda = MOEDAS_SUPORTADAS.get(moeda_bruta.lower())

    if not moeda:
        await update.message.reply_text("Moeda não reconhecida. Use: dolar, euro ou bitcoin.")
        return

    try:
        valor_alvo = float(valor_bruto.replace(",", "."))
    except ValueError:
        await update.message.reply_text("Valor inválido. Exemplo: /alerta dolar 5.30")
        return

    dados_cotacoes = obter_cotacoes()
    if not dados_cotacoes:
        await update.message.reply_text("Não consegui consultar a cotação atual. Tente novamente.")
        return

    preco_atual = dados_cotacoes[moeda]
    direcao = "alta" if valor_alvo >= preco_atual else "baixa"

    adicionar_alerta(chat_id, moeda, valor_alvo, direcao)

    await update.message.reply_text(
        f"Alerta criado! Vou te avisar quando o {moeda} "
        f"{'subir para' if direcao == 'alta' else 'cair para'} R$ {valor_alvo:.2f} "
        f"(preço atual: R$ {preco_atual:.2f})."
    )


async def meus_alertas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    alertas = [a for a in listar_alertas() if a["chat_id"] == chat_id]

    if not alertas:
        await update.message.reply_text("Você não tem alertas ativos.")
        return

    linhas = [
        f"• {a['moeda'].capitalize()}: R$ {a['valor_alvo']:.2f} ({a['direcao']})"
        for a in alertas
    ]
    await update.message.reply_text("Seus alertas ativos:\n" + "\n".join(linhas))


async def cancelar_alerta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    if len(context.args) != 1:
        await update.message.reply_text("Uso: /cancelaralerta <moeda>\nExemplo: /cancelaralerta dolar")
        return

    moeda = MOEDAS_SUPORTADAS.get(context.args[0].lower())
    if not moeda:
        await update.message.reply_text("Moeda não reconhecida.")
        return

    remover_alerta(chat_id, moeda)
    await update.message.reply_text(f"Alerta de {moeda} cancelado, se existia.")


async def checar_alertas(context: ContextTypes.DEFAULT_TYPE) -> None:
    alertas = listar_alertas()
    if not alertas:
        return

    dados_cotacoes = obter_cotacoes()
    if not dados_cotacoes:
        return

    for alerta_item in list(alertas):
        preco_atual = dados_cotacoes[alerta_item["moeda"]]
        atingiu = (
            (alerta_item["direcao"] == "alta" and preco_atual >= alerta_item["valor_alvo"])
            or (alerta_item["direcao"] == "baixa" and preco_atual <= alerta_item["valor_alvo"])
        )
        if atingiu:
            await context.bot.send_message(
                chat_id=alerta_item["chat_id"],
                text=(
                    f"🔔 Alerta disparado! {alerta_item['moeda'].capitalize()} "
                    f"chegou a R$ {preco_atual:.2f} (alvo: R$ {alerta_item['valor_alvo']:.2f})."
                ),
            )
            remover_alerta(alerta_item["chat_id"], alerta_item["moeda"])


# ---------- Histórico ----------

async def historico(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    variacoes = obter_variacao_diaria()
    if not variacoes:
        await update.message.reply_text("Não consegui consultar a variação agora.")
        return

    linhas = []
    for nome, chave in [("Dólar", "dolar"), ("Euro", "euro"), ("Bitcoin", "bitcoin")]:
        dado = variacoes[chave]
        sinal = "🔺" if dado["variacao_pct"] >= 0 else "🔻"
        linhas.append(f"{nome}: R$ {dado['valor']:.2f} ({sinal} {dado['variacao_pct']:.2f}% hoje)")

    await update.message.reply_text("Variação de hoje:\n" + "\n".join(linhas))


# ---------- Resumo diário automático ----------

async def assinar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    adicionar_assinante(update.effective_chat.id)
    await update.message.reply_text("Prontinho! Você vai receber o resumo das cotações todo dia às 9h.")


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    remover_assinante(update.effective_chat.id)
    await update.message.reply_text("Assinatura do resumo diário cancelada.")


async def enviar_resumo_diario(context: ContextTypes.DEFAULT_TYPE) -> None:
    assinantes = listar_assinantes()
    if not assinantes:
        return

    dados_cotacoes = obter_cotacoes()
    if not dados_cotacoes:
        return

    mensagem = "☀️ Bom dia! Resumo das cotações de hoje:\n\n" + formatar_mensagem(dados_cotacoes)
    for chat_id in assinantes:
        await context.bot.send_message(chat_id=chat_id, text=mensagem)


# ---------- Erro global ----------

async def tratar_erro(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Erro não tratado: %s", context.error, exc_info=context.error)


# ---------- Montagem da aplicação ----------

def criar_aplicacao() -> Application:
    if not TELEGRAM_TOKEN:
        raise RuntimeError(
            "TELEGRAM_TOKEN não encontrado. Verifique se o arquivo .env "
            "contém a variável TELEGRAM_TOKEN configurada."
        )

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("converter", converter))
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(CommandHandler("meusalertas", meus_alertas))
    app.add_handler(CommandHandler("cancelaralerta", cancelar_alerta))
    app.add_handler(CommandHandler("historico", historico))
    app.add_handler(CommandHandler("assinar", assinar))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_handler(CallbackQueryHandler(botao_cotacao, pattern="^cot_"))
    app.add_error_handler(tratar_erro)

    app.job_queue.run_repeating(checar_alertas, interval=300, first=10)
    app.job_queue.run_daily(
        enviar_resumo_diario,
        time=time(hour=9, minute=0, tzinfo=ZoneInfo("America/Sao_Paulo")),
    )

    return app


def main() -> None:
    app = criar_aplicacao()
    logger.info("Bot iniciado. Aguardando comandos no Telegram... (Ctrl+C para parar)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()