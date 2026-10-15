import time
from core.utils import escrever_texto
from core.menu import limpar_tela

# --- NOVAS IMPORTAÇÕES PARA COMBATE NA EXPLORAÇÃO ---
from core.entidades import Inimigo
from core.combate import iniciar_combate


def menu_personagem_livre(heroi):
    """Um submenu para o jogador gerenciar inventário e status fora de combate."""
    while True:
        limpar_tela()
        print("\n" + "=" * 45)
        print("                 ACAMPAMENTO / MENU           ")
        print("=" * 45)
        print("1. Abrir Inventário (Usar Item)")
        print("2. Verificar Status")
        print("3. Voltar à exploração")
        print("=" * 45)

        escolha = input("\nEscolha uma opção (1-3): ")

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
            print(f"Nome: {heroi.nome} | Level: {heroi.level}")
            print(f"HP: {heroi.vida}/{heroi.vida_maxima}")
            print(
                f"Ataque Total: {heroi.calcular_ataque()} | Defesa: {heroi.defesa_base}"
            )
            print(
                f"Arma Equipada: {heroi.arma_equipada['nome'] if heroi.arma_equipada else 'Desarmado'}"
            )
            print(
                f"Dinheiro: {heroi.dinheiro['cobre']} PC | {heroi.dinheiro['prata']} PP | {heroi.dinheiro['ouro']} PO | {heroi.dinheiro['platina']} PL"
            )
            print(f"Total estimado: {heroi.total_em_ouro():.2f} PO")
            input("\n(Pressione ENTER para voltar)")

        elif escolha == "3":
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
            menu_personagem_livre(heroi)

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
            menu_personagem_livre(heroi)

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
            "Aberração do Lodo", level=2, vida_maxima=75, ataque_base=12, defesa_base=2
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
            menu_personagem_livre(heroi)

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
    input("\n[ FIM DO CAPÍTULO 1 - Pressione ENTER para voltar ao menu ]")

    # Retorna o status de fim de jogo para encerrar o loop pacificamente
    return "fim_de_jogo"


def iniciar_exploracao(heroi):
    """
    O Motor Principal do Jogo. Ele gerencia as transições de tela.
    """
    sala_atual = "bifurcacao"  # O jogador começa aqui após o primeiro boss

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

        elif sala_atual == "superficie":
            sala_atual = cena_superficie(heroi)

        # Se a função retornar derrota (morreu no monstro) ou fim do jogo (venceu a demo)
        elif sala_atual == "derrota" or sala_atual == "fim_de_jogo":
            break
