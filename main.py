from core.menu import menu_principal, limpar_tela
from core.historia import introducao


def iniciar_jogo():
    rodando = True

    while rodando:
        estado_atual = menu_principal()

        if estado_atual == "novo_jogo":
            limpar_tela()
            print("Iniciando uma nova jornada...")
            nome_personagem = introducao()

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
