from core.utils import escrever_texto
import time


def introducao():
    escrever_texto(
        "Sua cabeça lateja. O frio do chão de pedra é a primeira coisa que você sente."
    )
    time.sleep(1)
    escrever_texto(
        "Você abre os olhos lentamente. A escuridão é quase total, quebrada apenas por frestas de luz."
    )
    escrever_texto(
        "Você não lembra como chegou aqui. Na verdade... você não lembra de absolutamente nada."
    )
    time.sleep(1)

    escrever_texto(
        "\nTateando os próprios bolsos da calça em busca de respostas, seus dedos encontram um pedaço de papel amassado."
    )
    escrever_texto(
        "Forçando a vista, você percebe para o seu alívio que ainda sabe ler. O bilhete diz:"
    )
    print("-" * 50)
    time.sleep(1)

    # O input para capturar o nome do jogador de forma imersiva
    nome_jogador = input("No topo do bilhete está escrito o seu nome. Qual é? \n> ")

    print("-" * 50)
    # Podemos diminuir a velocidade para dar mais impacto dramático à carta
    escrever_texto(
        f"'{nome_jogador}, se você está lendo isso, o pior já aconteceu.'", 0.05
    )
    escrever_texto(
        "'Eles sabem que você acordou. Não confie nas sombras e não pare de se mover.'",
        0.05,
    )
    escrever_texto("'Encontre o farol.'", 0.08)
    escrever_texto("Ass.: Elara.", 0.05)
    print("-" * 50)

    time.sleep(1)
    escrever_texto(
        f"\n'{nome_jogador}... Esse é o meu nome. Mas quem é Elara? O que aconteceu comigo?'"
    )
    time.sleep(1)
    escrever_texto(
        "\nDe repente, o som de passos pesados e rasgados ecoa pela escuridão, vindo na sua direção."
    )
    escrever_texto(
        "Você olha ao redor desesperado, encontra uma pequena viga de madeira no chão e a pega sem hesitar."
    )
    escrever_texto("Das sombras, uma figura decrépita avança para atacar!")

    input("\n(Pressione ENTER para entrar em combate...)")

    # Retornamos o nome para usá-lo na criação do objeto da classe Jogador no próximo passo
    return nome_jogador
