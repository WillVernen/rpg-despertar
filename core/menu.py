import os


def limpar_tela():
    # Limpa o terminal do VSCode/Windows (cls) ou Linux/Mac (clear)
    os.system("cls" if os.name == "nt" else "clear")


def exibir_titulo():
    print("========================================")
    print("             O DESPERTAR                ")  # Podemos mudar o título depois
    print("========================================")
    print("1. Novo Jogo")
    print("2. Carregar Jogo")
    print("3. Sair")
    print("========================================")


def menu_principal():
    while True:
        limpar_tela()
        exibir_titulo()

        escolha = input("\nO que você deseja fazer? (1-3): ")

        if escolha == "1":
            return "novo_jogo"
        elif escolha == "2":
            return "carregar_jogo"
        elif escolha == "3":
            return "sair"
        else:
            input("\nOpção inválida. Pressione ENTER para tentar novamente.")
