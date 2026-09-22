"""
Armazenamento simples em JSON para alertas de preço e assinantes do resumo diário.
"""
import json
import os

CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "dados.json")


def _carregar():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return {"alertas": [], "assinantes": []}
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar(dados):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def adicionar_alerta(chat_id, moeda, valor_alvo, direcao):
    dados = _carregar()
    dados["alertas"].append({
        "chat_id": chat_id,
        "moeda": moeda,
        "valor_alvo": valor_alvo,
        "direcao": direcao,
    })
    _salvar(dados)


def listar_alertas():
    return _carregar()["alertas"]


def remover_alerta(chat_id, moeda):
    dados = _carregar()
    dados["alertas"] = [
        a for a in dados["alertas"]
        if not (a["chat_id"] == chat_id and a["moeda"] == moeda)
    ]
    _salvar(dados)


def adicionar_assinante(chat_id):
    dados = _carregar()
    if chat_id not in dados["assinantes"]:
        dados["assinantes"].append(chat_id)
        _salvar(dados)


def remover_assinante(chat_id):
    dados = _carregar()
    if chat_id in dados["assinantes"]:
        dados["assinantes"].remove(chat_id)
        _salvar(dados)


def listar_assinantes():
    return _carregar()["assinantes"]