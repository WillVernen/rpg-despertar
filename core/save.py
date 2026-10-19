import json
import os
from core.entidades import Jogador

ARQUIVO_SAVE = "savegame.json"


def salvar_jogo(heroi, sala_atual):
    """Salva os dados do herói e a sala em que ele estava."""
    dados = {"heroi": heroi.to_dict(), "sala_atual": sala_atual}

    # Abre (ou cria) o arquivo em modo de escrita ('w')
    with open(ARQUIVO_SAVE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    return True


def carregar_jogo():
    """Lê o arquivo JSON e recria o herói e a sala."""
    if not os.path.exists(ARQUIVO_SAVE):
        return None, None

    # Abre o arquivo em modo de leitura ('r')
    with open(ARQUIVO_SAVE, "r", encoding="utf-8") as f:
        dados = json.load(f)

    heroi = Jogador.from_dict(dados["heroi"])
    sala_atual = dados.get("sala_atual", "bifurcacao")

    return heroi, sala_atual
