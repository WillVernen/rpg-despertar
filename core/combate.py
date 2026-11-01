import time
import random  # <-- NOVA IMPORTAÇÃO
from core.utils import escrever_texto
from core.menu import limpar_tela


def iniciar_combate(heroi, inimigo, batalha_tutorial=False, emboscada=False):
    limpar_tela()

    nome_inimigo_display = inimigo.nome if inimigo.analisado else "Figura Sombria"

    # NOVO: Lógica de Ataque Surpresa
    if emboscada:
        escrever_texto(
            f"Você salta das sombras e embosca o(a) {nome_inimigo_display}!", 0.03
        )
        dano_emboscada = heroi.calcular_ataque()
        dano_causado = inimigo.receber_dano(dano_emboscada)
        arma_nome = (
            heroi.arma_equipada["nome"] if heroi.arma_equipada else "mãos livres"
        )
        escrever_texto(
            f"Seu ataque surpresa com a {arma_nome} causa {dano_causado} de dano imediato!",
            0.03,
        )
        time.sleep(1)
    else:
        escrever_texto(
            f"Um(a) {nome_inimigo_display} surge das sombras e bloqueia o seu caminho!",
            0.03,
        )

    turno = 1  # Inicializador do contador de turnos

    while heroi.esta_vivo() and inimigo.esta_vivo():
        # Atualizamos o nome no caso de ter sido analisado no turno anterior
        nome_inimigo_display = inimigo.nome if inimigo.analisado else "Figura Sombria"

        print("\n" + "=" * 45)
        print(f"                  TURNO {turno}                  ")
        print("=" * 45)
        # O HP do herói agora é sempre visível
        print(f" {heroi.nome}: {heroi.vida}/{heroi.vida_maxima} HP")

        if inimigo.analisado:
            print(f" {inimigo.nome}: {inimigo.vida}/{inimigo.vida_maxima} HP")
        else:
            print(f" {nome_inimigo_display}: ???/??? HP")

        print("=" * 45)
        print("1. Atacar")
        print("2. Fugir")
        print("3. Usar Item")
        print("4. Verificar Status (Ação Livre)")
        print("5. Analisar Inimigo (Ação Livre)")
        print("=" * 45)

        escolha = input("\nEscolha sua ação (1-5): ")
        limpar_tela()

        turno_gasto = False  # Variável de controle para saber se o inimigo vai atacar

        if escolha == "1":
            dano_heroi = heroi.calcular_ataque()
            dano_causado = inimigo.receber_dano(dano_heroi)
            arma_nome = (
                heroi.arma_equipada["nome"] if heroi.arma_equipada else "mãos livres"
            )
            escrever_texto(
                f"Você ataca o(a) {nome_inimigo_display} com sua {arma_nome} e causa {dano_causado} de dano!"
            )
            turno_gasto = True

        elif escolha == "2":
            if batalha_tutorial:
                escrever_texto(
                    "Você tenta correr, mas as paredes estreitas e a escuridão bloqueiam sua fuga!"
                )
                escrever_texto(
                    "Esta é uma luta pela sobrevivência. Fugir não é uma opção!"
                )
                turno_gasto = True
            else:
                escrever_texto(
                    "Você dá as costas para o perigo e tenta correr desesperadamente..."
                )
                time.sleep(1)

                # Sorteia um número de 1 a 100. (50% de chance de sucesso por enquanto)
                chance_fuga = random.randint(1, 100)

                if chance_fuga <= 50:
                    escrever_texto(
                        "Você consegue despistar a criatura e escapar com vida... desta vez!"
                    )
                    time.sleep(2)
                    return "fuga"  # Retorna a string de sucesso na fuga
                else:
                    escrever_texto(
                        f"O(A) {nome_inimigo_display} é mais rápido e bloqueia sua rota de fuga!"
                    )
                    turno_gasto = (
                        True  # A fuga falhou, o turno foi gasto e o inimigo vai atacar!
                    )

        elif escolha == "3":
            if not heroi.mostrar_inventario():
                input("\n(Pressione ENTER para voltar à batalha)")
                continue  # Não gasta o turno se estiver vazio

            escolha_item = input("\nEscolha o número do item (ou '0' para cancelar): ")

            if escolha_item.isdigit() and int(escolha_item) > 0:
                indice_item = int(escolha_item) - 1
                if 0 <= indice_item < len(heroi.inventario):
                    mensagem = heroi.usar_item(indice_item)
                    escrever_texto(mensagem)
                    turno_gasto = True
                else:
                    print("Opção de item inválida.")
                    continue
            else:
                print("Ação cancelada.")
                continue

        elif escolha == "4":
            print("\n--- SEU STATUS ---")
            print(
                f"Nome: {heroi.nome} | Level: {heroi.level} ({heroi.xp}/{heroi.xp_necessario} XP)"
            )  # <-- ATUALIZADO
            print(f"Pontos de Habilidade: {heroi.pontos_habilidade}")  # <-- NOVO
            print(f"HP: {heroi.vida}/{heroi.vida_maxima}")
            print(
                f"Ataque Total: {heroi.calcular_ataque()} | Defesa: {heroi.calcular_defesa()}"
            )

            arma_nome = (
                heroi.arma_equipada["nome"] if heroi.arma_equipada else "Nenhuma"
            )
            armadura_nome = (
                heroi.armadura_equipada["nome"]
                if heroi.armadura_equipada
                else "Nenhuma"
            )
            print(f"Arma Equipada: {arma_nome}")
            print(f"Armadura Equipada: {armadura_nome}")

            print(
                f"Dinheiro: {heroi.dinheiro['cobre']} PC | {heroi.dinheiro['prata']} PP | {heroi.dinheiro['ouro']} PO | {heroi.dinheiro['platina']} PL"
            )
            print(f"Total estimado: {heroi.total_em_ouro():.2f} PO")
            input("\n(Pressione ENTER para voltar à batalha)")
            continue

        elif escolha == "5":
            # Revela os status do inimigo
            inimigo.analisado = True
            print("\n--- ANALISANDO O INIMIGO ---")
            print("Sua visão se ajusta à escuridão e você reconhece a ameaça.")
            print(f"É um(a) {inimigo.nome} (Level {inimigo.level})!")
            print(f"HP Atual: {inimigo.vida}/{inimigo.vida_maxima}")
            print(
                f"Força de Ataque: {inimigo.ataque_base} | Defesa: {inimigo.defesa_base}"
            )
            input("\n(Pressione ENTER para voltar à batalha)")
            continue  # Ação Livre

        else:
            print("Ação inválida. A tensão atrapalha sua mente.")
            continue

        # Turno do inimigo
        if inimigo.esta_vivo() and turno_gasto:
            time.sleep(1)
            dano_inimigo = inimigo.ataque_base
            dano_sofrido = heroi.receber_dano(dano_inimigo)
            escrever_texto(
                f"\nO(A) {nome_inimigo_display} avança e te atinge, causando {dano_sofrido} de dano!"
            )
            time.sleep(1)

        # Avança o contador de turnos apenas se o tempo passou de verdade
        if turno_gasto:
            turno += 1

    # Resolução final do combate
    if heroi.esta_vivo():
        escrever_texto(
            f"\nCom um último golpe, o(a) {nome_inimigo_display} se desfaz em uma pilha de ossos."
        )
        time.sleep(3)
        return "vitoria"
    else:
        escrever_texto(
            "\nSua visão escurece... O frio do chão é a última coisa que você sente antes do fim."
        )
        time.sleep(3)
        return "derrota"
