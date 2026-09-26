import time
from core.menu import menu_principal, limpar_tela
from core.historia import introducao
from core.entidades import Jogador, Inimigo
from core.combate import iniciar_combate
from core.utils import escrever_texto


def iniciar_jogo():
    rodando = True

    while rodando:
        estado_atual = menu_principal()

        if estado_atual == "novo_jogo":
            limpar_tela()
            print("Iniciando uma nova jornada...")
            nome_personagem = introducao()
            heroi = Jogador(nome=nome_personagem)
            heroi.equipar_arma("Viga de Madeira", 10)

            # 4. Instancia o Inimigo
            esqueleto = Inimigo(
                nome="Esqueleto", level=1, vida_maxima=50, ataque_base=10, defesa_base=0
            )

            # (O próximo passo será chamar a função de Combate aqui)
            limpar_tela()
            print(
                f"\n{heroi.nome} está pronto para a batalha com HP {heroi.vida}/{heroi.vida_maxima} e Ataque {heroi.calcular_ataque()}!"
            )
            print("Uma figura sombria apareceu!")
            input("\n(Pressione ENTER para continuar...)")

            # Inicia o combate com a flag de tutorial ativada (não pode fugir)
            resultado = iniciar_combate(heroi, esqueleto, batalha_tutorial=True)

            if resultado == "vitoria":
                limpar_tela()
                escrever_texto(
                    "Você respira ofegante. O perigo imediato passou, mas a dor dos ferimentos é real."
                )
                time.sleep(1)
                escrever_texto(
                    "\nVasculhando os restos da criatura, você nota algo brilhando no meio dos ossos."
                )
                escrever_texto(
                    "É uma pequena garrafinha de vidro contendo um líquido avermelhado. O rótulo desgastado diz: 'Poção de Cura'."
                )
                escrever_texto(
                    "Você também encontra uma pequena bolsa de couro surrada presa à cintura do que sobrou da criatura."
                )
                escrever_texto("Dentro dela, algumas peças de cobre tilintam.")

                # Adicionando os itens ao inventário do jogador (Dicionários são ótimos para organizar os dados do item)
                heroi.inventario.append(
                    {"nome": "Poção de Cura", "tipo": "cura", "valor": 50}
                )
                heroi.adicionar_dinheiro("cobre", 15)  # Adiciona 15 PC à carteira

                print("\nVocê adquiriu [1 Poção de Cura] e [15 Peças de Cobre]!")
                input("\n(Pressione ENTER para continuar a exploração...)")

                # O jogo continuará a partir daqui...

            elif resultado == "derrota":
                print("\n====================")
                print("     GAME OVER      ")
                print("====================")
                input("\nPressione ENTER para voltar ao Menu Principal.")

        elif estado_atual == "carregar_jogo":
            limpar_tela()
            print("Sistema de Save/Load será implementado em breve.")
            input("\n(Pressione ENTER para voltar ao menu por enquanto)")

        elif estado_atual == "sair":
            limpar_tela()
            print("Obrigado por jogar. Até a próxima!")
            rodando = False


if __name__ == "__main__":
    iniciar_jogo()
