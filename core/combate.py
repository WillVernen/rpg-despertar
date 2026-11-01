import time
import random
from core.utils import escrever_texto
from core.menu import limpar_tela
from core.habilidades import CATALOGO_HABILIDADES  # <-- NOVA IMPORTAÇÃO


def iniciar_combate(heroi, inimigo, batalha_tutorial=False, emboscada=False):
    limpar_tela()

    nome_inimigo_display = inimigo.nome if inimigo.analisado else "Figura Sombria"

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

    turno = 1

    while heroi.esta_vivo() and inimigo.esta_vivo():
        nome_inimigo_display = inimigo.nome if inimigo.analisado else "Figura Sombria"

        print("\n" + "=" * 45)
        print(f"                  TURNO {turno}                  ")
        print("=" * 45)

        # O HP e MP do herói agora são visíveis
        print(
            f" {heroi.nome}: {heroi.vida}/{heroi.vida_maxima} HP | {heroi.mana}/{heroi.mana_maxima} MP"
        )

        if inimigo.analisado:
            print(f" {inimigo.nome}: {inimigo.vida}/{inimigo.vida_maxima} HP")
        else:
            print(f" {nome_inimigo_display}: ???/??? HP")

        print("=" * 45)
        print("1. Atacar")
        print("2. Habilidade / Magia")  # <-- NOVA OPÇÃO
        print("3. Fugir")
        print("4. Usar Item")
        print("5. Verificar Status (Ação Livre)")
        print("6. Analisar Inimigo (Ação Livre)")
        print("=" * 45)

        escolha = input("\nEscolha sua ação (1-6): ")
        limpar_tela()

        turno_gasto = False

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

        elif escolha == "2":  # --- NOVO SISTEMA DE HABILIDADES ---
            if not heroi.habilidades:
                print("Você ainda não aprendeu nenhuma habilidade.")
                input("\n(Pressione ENTER para voltar à batalha)")
                continue

            print("\n--- SUAS HABILIDADES ---")
            for i, hab_nome in enumerate(heroi.habilidades):
                custo = CATALOGO_HABILIDADES[hab_nome]["custo_mp"]
                print(f"{i + 1}. {hab_nome} ({custo} MP)")
            print("0. Voltar")

            hab_escolha = input("\nEscolha a habilidade: ")
            limpar_tela()

            if hab_escolha.isdigit() and int(hab_escolha) > 0:
                indice = int(hab_escolha) - 1
                if 0 <= indice < len(heroi.habilidades):
                    nome_hab = heroi.habilidades[indice]
                    detalhes = CATALOGO_HABILIDADES[nome_hab]

                    # Verifica se tem Mana suficiente
                    if heroi.mana >= detalhes["custo_mp"]:
                        heroi.mana -= detalhes["custo_mp"]  # Consome o MP
                        turno_gasto = True

                        # Processa o efeito com base no TIPO da habilidade
                        if detalhes["tipo"] == "fisico":
                            # Dano base multiplicado
                            dano_base = heroi.calcular_ataque()
                            dano_skill = int(dano_base * detalhes["multiplicador_dano"])
                            dano_causado = inimigo.receber_dano(dano_skill)
                            escrever_texto(
                                f"Você usa {nome_hab}! O impacto brutal causa {dano_causado} de dano!"
                            )

                        elif detalhes["tipo"] == "magico":
                            # Magia causa dano direto (ignorando a defesa do inimigo)
                            dano_skill = detalhes["dano_fixo"]
                            inimigo.vida -= dano_skill
                            if inimigo.vida < 0:
                                inimigo.vida = 0
                            escrever_texto(
                                f"Você conjura {nome_hab}! O ataque mágico atinge em cheio causando {dano_skill} de dano direto!"
                            )

                        elif detalhes["tipo"] == "cura":
                            # Cura o jogador sem ultrapassar a vida máxima
                            cura = detalhes["cura"]
                            vida_anterior = heroi.vida
                            heroi.vida = min(heroi.vida + cura, heroi.vida_maxima)
                            vida_recuperada = heroi.vida - vida_anterior
                            escrever_texto(
                                f"Você foca sua energia e usa {nome_hab}! Recuperou {vida_recuperada} HP!"
                            )
                    else:
                        print(
                            f"MP insuficiente! {nome_hab} requer {detalhes['custo_mp']} MP."
                        )
                        continue  # Não gasta o turno
                else:
                    print("Opção inválida.")
                    continue
            else:
                print("Ação cancelada.")
                continue

        elif escolha == "3":
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

                chance_fuga = random.randint(1, 100)

                if chance_fuga <= 50:
                    escrever_texto(
                        "Você consegue despistar a criatura e escapar com vida... desta vez!"
                    )
                    time.sleep(2)
                    return "fuga"
                else:
                    escrever_texto(
                        f"O(A) {nome_inimigo_display} é mais rápido e bloqueia sua rota de fuga!"
                    )
                    turno_gasto = True

        elif escolha == "4":
            if not heroi.mostrar_inventario():
                input("\n(Pressione ENTER para voltar à batalha)")
                continue

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

        elif escolha == "5":
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

        elif escolha == "6":
            inimigo.analisado = True
            print("\n--- ANALISANDO O INIMIGO ---")
            print("Sua visão se ajusta à escuridão e você reconhece a ameaça.")
            print(f"É um(a) {inimigo.nome} (Level {inimigo.level})!")
            print(f"HP Atual: {inimigo.vida}/{inimigo.vida_maxima}")
            print(
                f"Força de Ataque: {inimigo.ataque_base} | Defesa: {inimigo.defesa_base}"
            )
            input("\n(Pressione ENTER para voltar à batalha)")
            continue

        else:
            print("Ação inválida. A tensão atrapalha sua mente.")
            continue

        if inimigo.esta_vivo() and turno_gasto:
            time.sleep(1)
            dano_inimigo = inimigo.ataque_base
            dano_sofrido = heroi.receber_dano(dano_inimigo)
            escrever_texto(
                f"\nO(A) {nome_inimigo_display} avança e te atinge, causando {dano_sofrido} de dano!"
            )
            time.sleep(1)

        if turno_gasto:
            turno += 1

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
