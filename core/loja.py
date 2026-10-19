import time
from core.utils import escrever_texto
from core.menu import limpar_tela


def mercador_floresta(heroi):
    limpar_tela()
    escrever_texto(
        "Uma figura encurvada, coberta por um manto de retalhos, está sentada sobre um tronco."
    )
    escrever_texto(
        "Seu rosto está oculto nas sombras do capuz. Ele expõe algumas mercadorias em um pano velho."
    )
    escrever_texto(
        "- 'Ora, ora... um sobrevivente das profundezas. O que deseja comprar?'"
    )
    time.sleep(5)

    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("           MERCADOR ERRANTE (O COLECIONADOR)       ")
        print("=" * 45)
        print(
            f" Seu dinheiro: {heroi.dinheiro['cobre']} PC | {heroi.dinheiro['prata']} PP | {heroi.dinheiro['ouro']} PO"
        )
        print("=" * 45)
        print("1. Comprar [Poção de Cura] (Recupera 50 HP) - Custo: 20 PC")
        print("2. Comprar [Broquel de Madeira] (Defesa +2) - Custo: 4 PP")

        # O mercador faz uma oferta tentadora pelo anel se o jogador o tiver
        tem_anel = any(
            item["nome"] == "Anel com Emblema Apagado" for item in heroi.inventario
        )
        if tem_anel:
            print(
                "3. Vender [Anel com Emblema Apagado] - Ele oferece: 2 PO (Peças de Ouro)!"
            )

        print("4. Sair da Loja")
        print("=" * 45)

        escolha = input("\nFaça sua escolha: ")

        if escolha == "1":
            if heroi.gastar_dinheiro("cobre", 20):
                heroi.inventario.append(
                    {"nome": "Poção de Cura", "tipo": "cura", "valor": 50}
                )
                print("\nVocê comprou uma Poção de Cura!")
            else:
                print(
                    "\n- 'Sem moedas de cobre suficientes, viajante. Não faço caridade.'"
                )
            input("\n(Pressione ENTER para continuar)")

        elif escolha == "2":
            # Verifica se já não comprou antes para não gastar à toa
            if (
                heroi.armadura_equipada
                and heroi.armadura_equipada["nome"] == "Broquel de Madeira"
            ):
                print("\n- 'Você já comprou o meu único escudo, guerreiro.'")
            elif heroi.gastar_dinheiro("prata", 4):
                heroi.equipar_armadura("Broquel de Madeira", 2)
                print(
                    f"\nVocê equipou o Broquel de Madeira. Sua Defesa subiu para {heroi.calcular_defesa()}!"
                )
            else:
                print("\n- 'Faltam moedas de prata. Volte quando tiver fundos.'")
            input("\n(Pressione ENTER para continuar)")

        elif escolha == "3" and tem_anel:
            limpar_tela()
            escrever_texto(
                "O mercador estica uma mão ossuda e trêmula em direção ao anel."
            )
            escrever_texto(
                "- 'Essa relíquia... não pertence a você. Deixe comigo e seja rico.'"
            )

            confirma = input("\nTem certeza que deseja vender o Anel? (s/n): ").lower()
            if confirma == "s":
                # Remove o anel do inventário
                for i, item in enumerate(heroi.inventario):
                    if item["nome"] == "Anel com Emblema Apagado":
                        heroi.inventario.pop(i)
                        break
                heroi.adicionar_dinheiro("ouro", 2)
                print("\nVocê vendeu o Anel e recebeu 2 Peças de Ouro!")
                escrever_texto("- 'Uma escolha... sábia. Hehehe...'")
            else:
                print("\nVocê recua com o anel. O mercador resmunga em frustração.")
            input("\n(Pressione ENTER para continuar)")

        elif escolha == "4":
            escrever_texto("\n- 'Até a próxima... se houver uma próxima.'")
            time.sleep(3)
            break
        else:
            print("\nOpção inválida.")
            time.sleep(2)
