import time
from core.utils import escrever_texto
from core.menu import limpar_tela

# Dicionário mestre contendo todas as habilidades do jogo
CATALOGO_HABILIDADES = {
    "Golpe Pesado": {
        "tipo": "fisico",
        "custo_mp": 15,
        "descricao": "Aplica toda a sua força na arma. Causa 150% do dano base.",
        "multiplicador_dano": 1.5,
    },
    "Chama Sombria": {
        "tipo": "magico",
        "custo_mp": 20,
        "descricao": "Conjura chamas mágicas. Causa 25 de dano mágico fixo (Ignora Defesa).",
        "dano_fixo": 25,
    },
    "Fôlego Renovado": {
        "tipo": "cura",
        "custo_mp": 25,
        "descricao": "Canaliza energia vital. Recupera 35 de HP.",
        "cura": 35,
    },
}


def menu_arvore_habilidades(heroi):
    while True:
        limpar_tela()
        print("\n" + "=" * 50)
        print("              ÁRVORE DE HABILIDADES            ")
        print("=" * 50)
        print(f" Pontos de Habilidade (PH) Disponíveis: {heroi.pontos_habilidade}")
        print(
            f" {heroi.nome} | Level: {heroi.level} | MP: {heroi.mana}/{heroi.mana_maxima}"
        )
        print("=" * 50)
        print("Habilidades Aprendidas:")
        if not heroi.habilidades:
            print("- Nenhuma habilidade aprendida ainda.")
        else:
            for hab in heroi.habilidades:
                print(f"- {hab}")
        print("=" * 50)

        # Lista as habilidades dinamicamente para o menu
        chaves_habilidades = list(CATALOGO_HABILIDADES.keys())

        for i, nome_hab in enumerate(chaves_habilidades):
            custo = CATALOGO_HABILIDADES[nome_hab]["custo_mp"]
            tipo = CATALOGO_HABILIDADES[nome_hab]["tipo"].upper()
            status = "[COMPRADA]" if nome_hab in heroi.habilidades else "[Custo: 1 PH]"
            print(f"{i + 1}. {nome_hab} ({tipo}) - {custo} MP {status}")

        print(f"{len(chaves_habilidades) + 1}. Voltar")
        print("=" * 50)

        escolha = input(
            "\nDigite o número da habilidade para aprender/ver detalhes (ou voltar): "
        )

        if escolha.isdigit():
            indice = int(escolha) - 1

            # Se for a opção de voltar
            if indice == len(chaves_habilidades):
                break

            # Se for uma habilidade válida
            if 0 <= indice < len(chaves_habilidades):
                nome_escolhido = chaves_habilidades[indice]
                detalhes = CATALOGO_HABILIDADES[nome_escolhido]

                limpar_tela()
                print("\n" + "-" * 40)
                print(f" {nome_escolhido.upper()} ")
                print("-" * 40)
                print(f"Custo de Conjuração: {detalhes['custo_mp']} MP")
                print(f"Descrição: {detalhes['descricao']}")
                print("-" * 40)

                if nome_escolhido in heroi.habilidades:
                    print("\nVocê já domina esta habilidade.")
                    input("\n(Pressione ENTER para voltar)")
                else:
                    if heroi.pontos_habilidade > 0:
                        confirma = input(
                            "\nDeseja gastar 1 PH para aprender esta habilidade? (s/n): "
                        ).lower()
                        if confirma == "s":
                            heroi.habilidades.append(nome_escolhido)
                            heroi.pontos_habilidade -= 1
                            print(f"\nVocê aprendeu a habilidade {nome_escolhido}!")
                    else:
                        print(
                            "\nVocê não tem Pontos de Habilidade (PH) suficientes. Suba de nível para ganhar mais."
                        )
                    input("\n(Pressione ENTER para continuar)")
            else:
                print("Opção inválida.")
                time.sleep(1)
