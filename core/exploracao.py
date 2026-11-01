import time
import random
from core.utils import escrever_texto
from core.menu import limpar_tela
from core.save import salvar_jogo
from core.loja import mercador_floresta
from core.habilidades import menu_arvore_habilidades

# --- NOVAS IMPORTAÇÕES PARA COMBATE NA EXPLORAÇÃO ---
from core.entidades import Inimigo
from core.combate import iniciar_combate


def menu_personagem_livre(heroi, sala_atual):
    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("                 ACAMPAMENTO / MENU           ")
        print("=" * 45)
        print("1. Abrir Inventário (Usar Item)")
        print("2. Verificar Status")
        print("3. Árvore de Habilidades")
        print("4. Salvar Jogo")
        print("5. Voltar à exploração")
        print("=" * 45)

        escolha = input("\nEscolha uma opção (1-5): ")

        if escolha == "1":
            limpar_tela()
            if heroi.mostrar_inventario():
                escolha_item = input(
                    "\nEscolha o número do item (ou '0' para voltar): "
                )
                if escolha_item.isdigit() and int(escolha_item) > 0:
                    indice = int(escolha_item) - 1
                    mensagem = heroi.usar_item(indice)
                    escrever_texto("\n" + mensagem)
                else:
                    print("\nFechando inventário...")
            input("\n(Pressione ENTER para continuar)")

        elif escolha == "2":
            limpar_tela()
            print("\n--- SEU STATUS ---")
            print(
                f"Nome: {heroi.nome} | Level: {heroi.level} ({heroi.xp}/{heroi.xp_necessario} XP)"
            )  # <-- ATUALIZADO
            print(f"Pontos de Habilidade: {heroi.pontos_habilidade}")  # <-- NOVO
            print(f"HP: {heroi.vida}/{heroi.vida_maxima}")
            # Correção: Agora usa calcular_defesa()
            print(
                f"Ataque Total: {heroi.calcular_ataque()} | Defesa: {heroi.calcular_defesa()}"
            )

            # Melhoria: Mostra arma e armadura
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
            input("\n(Pressione ENTER para voltar)")

        elif escolha == "3":
            limpar_tela()
            menu_arvore_habilidades(heroi)

        elif escolha == "4":
            limpar_tela()
            escrever_texto("Salvando o jogo...")
            salvar_jogo(heroi, sala_atual)
            print("\nJogo salvo com sucesso!")
            input("\n(Pressione ENTER para voltar)")

        elif escolha == "5":
            break


def cena_bifurcacao(heroi):
    # Inicializa a variável de progresso desta sala se ela ainda não existir
    if "estatua_vasculhada" not in heroi.progresso:
        heroi.progresso["estatua_vasculhada"] = False

    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("             A BIFURCAÇÃO DE PEDRA             ")
        print("=" * 45)
        print(f" {heroi.nome}: {heroi.vida}/{heroi.vida_maxima} HP")
        print("=" * 45)
        print("Você está em um corredor úmido. O caminho se divide em dois.")
        print(
            "1. Aproximar-se da porta de madeira (Luz fraca e calor emanando debaixo dela)"
        )
        print("2. Descer a escadaria espiral (Vento gelado e escuridão profunda)")

        # A opção 3 só aparece se a estátua ainda não foi vasculhada
        if not heroi.progresso["estatua_vasculhada"]:
            print("3. Investigar a estátua peculiar no centro da bifurcação")

        print("4. Menu do Personagem (Status e Inventário)")
        print("=" * 45)

        escolha = input("\nO que você faz?: ")

        if escolha == "1":
            limpar_tela()
            escrever_texto(
                "Você empurra a pesada porta de madeira. Suas dobradiças rangem ecoando pelo corredor..."
            )
            time.sleep(1)
            return "porta_madeira"  # Retorna o nome da próxima sala

        elif escolha == "2":
            limpar_tela()
            escrever_texto(
                "Você engole em seco e começa a descer os degraus escorregadios. O frio penetra seus ossos..."
            )
            time.sleep(1)
            return "escadaria"  # Retorna o nome da próxima sala

        elif escolha == "3" and not heroi.progresso["estatua_vasculhada"]:
            limpar_tela()
            escrever_texto(
                "Você se aproxima da estátua. É a figura de um corvo de pedra segurando um farol em miniatura."
            )
            time.sleep(1)
            escrever_texto(
                "O Farol... A mesma palavra do bilhete de Elara. Quem construiu isso?"
            )
            escrever_texto(
                "Ao tocar na miniatura do farol, você ouve um leve 'click'. Um compartimento oculto se abre na base."
            )
            escrever_texto(
                "Lá dentro, você encontra um Anel Estranho com um emblema apagado e 5 Peças de Prata (PP)!"
            )

            # Adiciona os itens e atualiza o progresso para a opção sumir do menu
            heroi.inventario.append(
                {"nome": "Anel com Emblema Apagado", "tipo": "misterio", "valor": 0}
            )
            heroi.adicionar_dinheiro("prata", 5)
            heroi.progresso["estatua_vasculhada"] = True

            input("\n(Pressione ENTER para voltar)")

        elif escolha == "4":
            menu_personagem_livre(heroi, "bifurcacao")

        else:
            print("\nOpção inválida. Tente novamente.")
            time.sleep(1)


# --- NOVAS SALAS AQUI ---


def cena_porta_madeira(heroi):
    # Setup inicial do progresso desta sala
    if "espada_encontrada" not in heroi.progresso:
        heroi.progresso["espada_encontrada"] = False
    if "diario_lido" not in heroi.progresso:
        heroi.progresso["diario_lido"] = False

    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("              ALOJAMENTO DOS GUARDAS           ")
        print("=" * 45)
        print("Uma pequena sala iluminada por uma tocha moribunda.")
        print("Há uma mesa bagunçada e um suporte de armas enferrujado.")
        print("É um beco sem saída. A única saída é por onde você entrou.")
        print("=" * 45)

        if not heroi.progresso["espada_encontrada"]:
            print("1. Vasculhar o suporte de armas")
        else:
            print("1. (Suporte de armas vazio)")

        print("2. Ler o livro aberto sobre a mesa")
        print("3. Voltar para a Bifurcação")
        print("4. Menu do Personagem")
        print("=" * 45)

        escolha = input("\nO que você faz?: ")

        if escolha == "1" and not heroi.progresso["espada_encontrada"]:
            limpar_tela()
            escrever_texto("A maioria das armas está quebrada ou inútil.")
            escrever_texto(
                "Porém, você encontra uma Espada Curta de Ferro em condições aceitáveis."
            )
            escrever_texto("É muito melhor que sua viga de madeira.")

            heroi.equipar_arma(
                "Espada Curta de Ferro", 15
            )  # Dá +15 de ataque em vez dos +10 da viga
            heroi.progresso["espada_encontrada"] = True

            print(
                f"\nVocê equipou a Espada Curta de Ferro. Seu ataque subiu para {heroi.calcular_ataque()}!"
            )
            input("\n(Pressione ENTER para voltar)")

        elif escolha == "2":
            limpar_tela()
            escrever_texto(
                "As páginas estão manchadas de sangue seco. Uma entrada recente chama atenção:"
            )
            print("\n" + "-" * 40)
            escrever_texto("'A cobaia #402 acordou mais cedo que o previsto.'", 0.04)
            escrever_texto(
                "'O soro do esquecimento funcionou, mas as memórias residuais o tornam perigoso.'",
                0.04,
            )
            escrever_texto("'Se ele tentar chegar ao Farol, ativem as Sombras.'", 0.04)
            print("-" * 40)

            if not heroi.progresso["diario_lido"]:
                escrever_texto(
                    "\nSua mente dispara. Cobaia #402? Soro do esquecimento? Isso explica sua perda de memória."
                )
                heroi.progresso["diario_lido"] = True

            input("\n(Pressione ENTER para voltar)")

        elif escolha == "3":
            limpar_tela()
            escrever_texto("Você deixa o alojamento e volta para o corredor frio.")
            time.sleep(1)
            return "bifurcacao"  # Retorna para a sala anterior!

        elif escolha == "4":
            menu_personagem_livre(heroi, "porta_madeira")

        else:
            print("\nOpção inválida ou já realizada.")
            time.sleep(1)


def cena_escadaria(heroi):
    limpar_tela()
    escrever_texto("Você desce os degraus em espiral com cuidado.")
    escrever_texto(
        "A luz da tocha vai ficando para trás até você ser engolido pela escuridão."
    )
    time.sleep(1)

    escrever_texto("\nDe repente, um degrau quebrado cede sob o seu peso!")

    print("\n1. Tentar pular para o próximo degrau (Requer sorte/agilidade)")
    print("2. Segurar-se nas pedras da parede")

    escolha = input("\nReação rápida! (1-2): ")

    limpar_tela()
    if escolha == "1":
        escrever_texto(
            "Você salta no escuro! Seu pé escorrega ao aterrissar e você torce o tornozelo."
        )
        dano = 5
        heroi.vida -= dano
        print(
            f"\nVocê sofreu {dano} de dano pela queda. HP atual: {heroi.vida}/{heroi.vida_maxima}"
        )
    else:
        escrever_texto(
            "Você rasga as mãos nas pedras afiadas, mas consegue se estabilizar sem cair."
        )
        escrever_texto("Apesar do susto, você está ileso.")

    input("\n(Pressione ENTER para continuar descendo...)")

    limpar_tela()
    escrever_texto("Após alguns minutos de descida tensa, a escadaria termina.")
    escrever_texto("O som de água corrente ecoa pelas paredes.")
    time.sleep(3)

    return "salao_alagado"  # Encaminha para o próximo grande nível do jogo


def cena_salao_alagado(heroi):
    # Setup de progresso para garantir que o monstro só apareça uma vez
    if "guardiao_morto" not in heroi.progresso:
        heroi.progresso["guardiao_morto"] = False

    limpar_tela()
    print("\n" + "=" * 45)
    print("                 O SALÃO ALAGADO               ")
    print("=" * 45)
    escrever_texto("Você pisa em uma poça d'água gélida até a altura dos tornozelos.")
    escrever_texto("O cheiro de lodo e decomposição é insuportável.")

    # Se o monstro ainda não foi morto, a batalha inicia!
    if not heroi.progresso["guardiao_morto"]:
        time.sleep(1)
        escrever_texto(
            "\nDe repente, a água começa a borbulhar violentamente à sua frente."
        )
        escrever_texto(
            "Uma abominação feita de ossos e lodo se ergue para bloquear a passagem!"
        )
        input("\n(Pressione ENTER para se defender!)")

        # Instancia um inimigo mais forte e chama a função de combate
        guardiao = Inimigo(
            "Aberração do Lodo",
            level=2,
            vida_maxima=75,
            ataque_base=12,
            defesa_base=2,
            xp_recompensa=70,
        )
        resultado = iniciar_combate(
            heroi, guardiao, batalha_tutorial=True
        )  # True para impedir fuga

        if resultado == "vitoria":
            limpar_tela()
            escrever_texto(
                "A abominação solta um guincho estridente e se dissolve em uma poça de lama escura."
            )
            time.sleep(1)
            escrever_texto(
                "\nNo meio dos restos da criatura, algo brilha com uma luz azul intensa."
            )
            escrever_texto(
                "Você se abaixa e recolhe um [Olho de Safira] e [20 Peças de Cobre]."
            )

            # Adiciona o item especial ao inventário (tipo 'chave') e o dinheiro
            heroi.inventario.append(
                {"nome": "Olho de Safira", "tipo": "chave", "valor": 0}
            )
            heroi.adicionar_dinheiro("cobre", 20)
            heroi.progresso["guardiao_morto"] = True

            mensagens_xp = heroi.ganhar_xp(guardiao.xp_recompensa)
            for msg in mensagens_xp:
                print(f"{msg}")

            input("\n(Pressione ENTER para prosseguir para o fundo do salão...)")
        else:
            # Se o herói morrer, retorna 'derrota' para encerrar o motor
            return "derrota"

    # Se já matou o monstro (ou acabou de matar), avança para a porta
    return "enigma_porta"


def cena_enigma_porta(heroi):
    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("             O PORTÃO DOS OBSERVADORES         ")
        print("=" * 45)
        escrever_texto(
            "No final do salão, um gigantesco portão de bronze barra a saída."
        )
        escrever_texto(
            "No centro da porta, há o rosto esculpido de um gigante com a boca aberta."
        )
        escrever_texto(
            "A órbita esquerda do gigante abriga um rubi cravado, mas a órbita direita está VAZIA."
        )
        print("=" * 45)

        print("1. Ler a inscrição na base do portão")
        print("2. Tentar empurrar o portão com força bruta")
        print("3. Abrir Inventário e usar um item na órbita vazia")
        print("4. Menu do Personagem")

        escolha = input("\nO que você faz?: ")

        if escolha == "1":
            limpar_tela()
            print("\n" + "-" * 45)
            escrever_texto("'O Guardião das águas afogadas retém a visão.'", 0.04)
            escrever_texto("'Devolva ao sentinela o que o lodo escondeu,'", 0.04)
            escrever_texto("'e o caminho para as estrelas se abrirá.'", 0.04)
            print("-" * 45)
            input("\n(Pressione ENTER para voltar)")

        elif escolha == "2":
            limpar_tela()
            escrever_texto(
                "Você empurra com todas as suas forças, mas o bronze denso não cede um milímetro sequer."
            )
            input("\n(Pressione ENTER para voltar)")

        elif escolha == "3":
            limpar_tela()
            if heroi.mostrar_inventario():
                escolha_item = input(
                    "\nEscolha o número do item para inserir na órbita (ou '0' para voltar): "
                )
                if escolha_item.isdigit() and int(escolha_item) > 0:
                    indice = int(escolha_item) - 1
                    item = heroi.inventario[indice]

                    # Verifica se o jogador usou o item correto
                    if item["nome"] == "Olho de Safira":
                        limpar_tela()
                        escrever_texto(
                            "Você pega o Olho de Safira úmido e o encaixa perfeitamente na órbita vazia."
                        )
                        time.sleep(1)
                        escrever_texto(
                            "\nUm som profundo de engrenagens ancestrais ecoa pelo salão!"
                        )
                        escrever_texto(
                            "O rosto do gigante parece se iluminar, e as pesadas portas se abrem lentamente..."
                        )

                        # Remove a chave do inventário após o uso
                        heroi.inventario.pop(indice)

                        input("\n(Pressione ENTER para atravessar o portão!)")
                        return "superficie"

                    else:
                        escrever_texto(
                            f"\nVocê tenta encaixar o(a) {item['nome']} na órbita, mas a peça não entra. Nada acontece."
                        )
                else:
                    print("\nCancelando ação...")
            input("\n(Pressione ENTER para voltar)")

        elif escolha == "4":
            menu_personagem_livre(heroi, "enigma_porta")

        else:
            print("\nOpção inválida.")
            time.sleep(1)


def cena_superficie(heroi):
    limpar_tela()
    print("\n" + "=" * 45)
    print("                 A SUPERFÍCIE                  ")
    print("=" * 45)
    escrever_texto("O ar frio da noite atinge o seu rosto. Você respira fundo.")
    escrever_texto(
        "O cheiro de lodo e masmorra fica para trás. Você vê uma densa floresta de pinheiros sob o luar."
    )
    time.sleep(1)

    escrever_texto(
        "\nVocê olha para cima e, cortando o céu escuro ao longe, uma luz circular gira lentamente."
    )
    escrever_texto("O Farol.")
    time.sleep(3)

    escrever_texto(f"\nParabéns, {heroi.nome}! Você sobreviveu à masmorra inicial.")
    escrever_texto("Mas a verdadeira jornada por respostas acabou de começar...")
    print("\n" + "=" * 45)
    input("\n[ FIM DO PRÓLOGO - Pressione ENTER para voltar ao menu ]")

    # Retorna o status de fim de jogo para encerrar o loop pacificamente
    return "fim_de_jogo"


def cena_acampamento(heroi):
    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("              FOGO DE ACAMPAMENTO              ")
        print("=" * 45)
        print(f" {heroi.nome}: {heroi.vida}/{heroi.vida_maxima} HP")
        print("=" * 45)
        print("As chamas estalam suavemente, oferecendo um breve alívio contra o frio.")
        print("A luz afasta as sombras da floresta. Este é um local seguro.")
        print("=" * 45)

        print("1. Descansar junto ao fogo (Recupera todo o HP/MP)")
        print("2. Menu do Personagem (Salvar Jogo)")
        print("3. Retornar à trilha principal")
        print("=" * 45)

        escolha = input("\nO que você faz?: ")

        if escolha == "1":
            limpar_tela()
            if heroi.vida == heroi.vida_maxima and heroi.mana == heroi.mana_maxima:
                escrever_texto(
                    "Você já está totalmente descansado. Suas feridas estão curadas."
                )
            else:
                escrever_texto(
                    "Você se deita perto das chamas, fecha os olhos e dorme um sono sem sonhos..."
                )
                time.sleep(3)
                heroi.vida = heroi.vida_maxima
                heroi.mana = heroi.mana_maxima
                escrever_texto(
                    "\nVocê acordou revigorado! Seu HP e MP foram totalmente restaurados."
                )
            input("\n(Pressione ENTER para continuar)")

        elif escolha == "2":
            # Passamos a string 'acampamento' para o Save funcionar corretamente aqui!
            menu_personagem_livre(heroi, "acampamento")

        elif escolha == "3":
            limpar_tela()
            escrever_texto(
                "Você apaga as brasas com um pouco de terra e volta para a escuridão da floresta."
            )
            time.sleep(3)
            return "floresta_inicio"

        else:
            print("\nOpção inválida.")
            time.sleep(2)


def cena_floresta_inicio(heroi):
    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("               A FLORESTA OBSCURA              ")
        print("=" * 45)
        print(
            "O vento assobia entre os pinheiros altos. O Farol ilumina o céu distante."
        )
        print("A trilha se divide. De um lado, você vê a fumaça de um acampamento.")
        print("Do outro, a figura encurvada de um mercador te observa.")
        print("=" * 45)

        print("1. Aproximar-se do Mercador Errante")
        print("2. Ir para o Fogo de Acampamento (Descansar e Salvar)")
        print("3. Seguir a trilha em direção ao Farol (Avançar na história)")
        print("4. Menu do Personagem")
        print("=" * 45)

        escolha = input("\nO que você faz?: ")

        if escolha == "1":
            mercador_floresta(heroi)

        elif escolha == "2":
            limpar_tela()
            escrever_texto(
                "Você caminha em direção à fumaça e encontra uma pequena clareira..."
            )
            time.sleep(1)
            return "acampamento"  # Envia o jogador para a nova cena

        elif escolha == "3":
            limpar_tela()
            escrever_texto(
                "Você se afasta do acampamento e entra na escuridão da trilha principal..."
            )
            time.sleep(1)
            return "trilha_lobos"  # AGORA APONTA PARA A NOVA CENA!

        elif escolha == "4":
            menu_personagem_livre(heroi, "floresta_inicio")

        else:
            print("\nOpção inválida.")
            time.sleep(1)


def cena_trilha_lobos(heroi):
    # Inicializa o progresso para saber se o obstáculo já foi superado
    if "lobo_derrotado" not in heroi.progresso:
        heroi.progresso["lobo_derrotado"] = False

    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("          TRILHA PARA O FAROL - A PATRULHA         ")
        print("=" * 45)

        # Se o lobo já foi derrotado (ou despistado)
        if heroi.progresso["lobo_derrotado"]:
            escrever_texto("O caminho de terra escura está silencioso.")
            escrever_texto("A silhueta do Farol parece um pouco mais próxima agora.")
            print("=" * 45)
            print("1. Continuar a jornada em direção ao Farol")
            print("2. Voltar para o Acampamento")
            print("3. Menu do Personagem")
            print("=" * 45)

            escolha = input("\nO que você faz?: ")

            if escolha == "1":
                limpar_tela()
                escrever_texto(
                    "Você segue pela trilha, adentrando ainda mais os mistérios da floresta..."
                )
                input("\n[Fim da Atualização 1.1 - Pressione ENTER para voltar]")
                return "fim_de_jogo"
            elif escolha == "2":
                return "floresta_inicio"
            elif escolha == "3":
                menu_personagem_livre(heroi, "trilha_lobos")
            else:
                print("\nOpção inválida.")
                time.sleep(1)

        # Se for a primeira vez encontrando o lobo
        else:
            escrever_texto(
                "Você avança sorrateiramente pela trilha. Um rosnado gutural corta o silêncio."
            )
            escrever_texto("À frente, dois olhos vermelhos brilham na escuridão.")
            escrever_texto(
                "É um [Lobo Corrompido] patrulhando a área. Ele ainda não notou sua presença."
            )
            print("=" * 45)
            print(
                "1. Tentar passar furtivamente pelas sombras (50% de chance de sucesso)"
            )
            print("2. Armar uma emboscada e atacar primeiro (Garante um ataque extra)")
            print("3. Recuar furtivamente para o Acampamento")
            print("4. Menu do Personagem")
            print("=" * 45)

            escolha = input("\nO que você faz?: ")

            if escolha == "1":
                limpar_tela()
                escrever_texto(
                    "Você prende a respiração e pisa suavemente entre as folhas secas..."
                )
                time.sleep(2)

                # RNG: Sorteia um número de 1 a 100. Se for <= 50, é sucesso.
                chance = random.randint(1, 100)

                if chance <= 50:
                    escrever_texto(
                        "\nSUCESSO! Você desliza pelas sombras como um fantasma."
                    )
                    escrever_texto(
                        "A fera não percebe nada, e você deixa o perigo para trás."
                    )
                    heroi.progresso["lobo_derrotado"] = True
                    input("\n(Pressione ENTER para continuar)")
                else:
                    escrever_texto("\n*CRACK*... Você pisa em um galho seco!")
                    escrever_texto(
                        "O Lobo Corrompido se vira e avança violentamente na sua direção!"
                    )
                    input("\n(Pressione ENTER para se defender!)")

                    lobo = Inimigo(
                        "Lobo Corrompido",
                        level=2,
                        vida_maxima=55,
                        ataque_base=14,
                        defesa_base=1,
                        xp_recompensa=40,
                    )
                    resultado = iniciar_combate(
                        heroi, lobo
                    )  # Combate normal, você perdeu a surpresa

                    if resultado == "vitoria":
                        resolver_vitoria_lobo(heroi, lobo)
                    elif resultado == "fuga":  # <-- NOVO TRATAMENTO DE FUGA
                        limpar_tela()
                        escrever_texto(
                            "Você corre de volta para a segurança do Acampamento com o coração acelerado."
                        )
                        time.sleep(2)
                        return "floresta_inicio"  # Retorna o jogador para a área segura
                    else:
                        return "derrota"

            elif escolha == "2":
                limpar_tela()
                escrever_texto(
                    "Você saca sua arma e aguarda o momento perfeito no matagal..."
                )
                input("\n(Pressione ENTER para saltar sobre a fera!)")

                lobo = Inimigo(
                    "Lobo Corrompido",
                    level=2,
                    vida_maxima=55,
                    ataque_base=14,
                    defesa_base=1,
                    xp_recompensa=40,
                )
                # Chama o combate passando emboscada=True
                resultado = iniciar_combate(heroi, lobo, emboscada=True)

                if resultado == "vitoria":
                    resolver_vitoria_lobo(heroi, lobo)
                elif resultado == "fuga":  # <-- NOVO TRATAMENTO DE FUGA
                    limpar_tela()
                    escrever_texto(
                        "Você abandona a luta e recua correndo para a beirada da floresta."
                    )
                    time.sleep(2)
                    return "floresta_inicio"  # Retorna o jogador para a área segura
                else:
                    return "derrota"

            elif escolha == "3":
                return "floresta_inicio"

            elif escolha == "4":
                menu_personagem_livre(heroi, "trilha_lobos")
            else:
                print("\nOpção inválida.")
                time.sleep(1)


def resolver_vitoria_lobo(heroi, inimigo_derrotado):
    """Função auxiliar para entregar o loot se o jogador vencer o lobo."""
    limpar_tela()
    escrever_texto("A fera demoníaca cai inerte no chão, dissipando uma fumaça negra.")
    time.sleep(1)
    escrever_texto(
        "\nVasculhando os restos mortais, você encontra [1 Dente de Lobo] e [10 Peças de Cobre]."
    )

    heroi.inventario.append({"nome": "Dente de Lobo", "tipo": "material", "valor": 0})
    heroi.adicionar_dinheiro("cobre", 10)
    heroi.progresso["lobo_derrotado"] = True

    # Entrega o XP do lobo
    mensagens_xp = heroi.ganhar_xp(inimigo_derrotado.xp_recompensa)
    for msg in mensagens_xp:
        print(f"{msg}")

    input("\n(Pressione ENTER para continuar a exploração...)")


def iniciar_exploracao(heroi, sala_inicial="bifurcacao"):
    sala_atual = sala_inicial

    while heroi.esta_vivo():
        if sala_atual == "bifurcacao":
            sala_atual = cena_bifurcacao(heroi)

        elif sala_atual == "porta_madeira":
            sala_atual = cena_porta_madeira(heroi)

        elif sala_atual == "escadaria":
            sala_atual = cena_escadaria(heroi)

        elif sala_atual == "salao_alagado":
            sala_atual = cena_salao_alagado(heroi)

        elif sala_atual == "enigma_porta":
            sala_atual = cena_enigma_porta(heroi)
            # Ao sair do enigma (superficie), o jogo nos manda para cena_floresta_inicio

        elif sala_atual == "superficie":
            sala_atual = cena_superficie(heroi)
            sala_atual = "floresta_inicio"

        elif sala_atual == "floresta_inicio":
            sala_atual = cena_floresta_inicio(heroi)

        elif sala_atual == "acampamento":
            sala_atual = cena_acampamento(heroi)

        # NOVO: Conexão para a trilha
        elif sala_atual == "trilha_lobos":
            sala_atual = cena_trilha_lobos(heroi)

        elif sala_atual == "derrota" or sala_atual == "fim_de_jogo":
            break
