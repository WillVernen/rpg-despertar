import sys
import time


def escrever_texto(texto, velocidade=0.03):
    """
    Imprime o texto letra por letra no terminal para criar imersão narrativa.
    """
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()  # Força o terminal a exibir a letra imediatamente
        time.sleep(velocidade)
    print()  # Garante a quebra de linha no final da frase
