# O Despertar

**O Despertar** é um RPG de texto em desenvolvimento, criado em Python. O jogador acorda sem memória em uma masmorra, encontra um bilhete assinado por Elara e parte em busca do Farol.

## Estado atual

O jogo já conta com:

- Menu principal com opções de novo jogo, carregar jogo e sair.
- Introdução narrativa com nome personalizado para o personagem.
- Combate por turnos, com ataques, defesa, análise de inimigos e consulta de status.
- Opção de fugir em combates que permitem escapar; batalhas de história podem bloquear a fuga.
- Inventário com uso de itens de cura durante o combate ou na exploração.
- Personagem com pontos de vida, ataque, defesa, arma equipada e dinheiro.
- Sistema de moedas de cobre, prata, ouro e platina.
- Exploração de uma masmorra com salas conectadas e escolhas de caminho.
- Objetos e pistas opcionais, como a estátua do corvo, o anel misterioso e o diário dos guardas.
- Inimigos como o Esqueleto e a Aberração do Lodo.
- Enigmas e itens-chave, incluindo o Olho de Safira e o portão dos Observadores.
- Primeiro capítulo concluído com a saída da masmorra e a chegada à superfície.

> **Observação:** as opções de carregar jogo já aparecem no menu, mas o sistema de salvamento ainda não foi implementado.

## Como executar

Requisito: Python 3 instalado.

Na pasta do projeto, execute:

```bash
python main.py
```

No Windows, também é possível usar:

```bash
py main.py
```

O jogo é executado no terminal e apresenta as instruções de cada ação na tela.

## Estrutura do projeto

```text
.
|-- main.py              # Inicialização e fluxo principal do jogo
|-- core/
|   |-- combate.py       # Combate por turnos
|   |-- entidades.py     # Personagens, atributos, inventário e dinheiro
|   |-- exploracao.py    # Salas, escolhas e progressão do capítulo
|   |-- historia.py      # Introdução narrativa
|   |-- menu.py          # Menu principal e limpeza da tela
|   `-- utils.py         # Exibição gradual de texto
|-- LICENSE              # Licença MIT
`-- README.md            # Documentação do projeto
```

## Ideias para o futuro

Estas são possibilidades para versões futuras, não funcionalidades já disponíveis:

- Implementar salvamento e carregamento da campanha.
- Continuar a história após o primeiro capítulo, com novas áreas, personagens, inimigos e missões.
- Criar mais escolhas com consequências e diferentes caminhos ou finais.
- Expandir o inventário com equipamentos, consumíveis, melhorias e gerenciamento de itens.
- Adicionar progressão de nível, atributos, habilidades e novas opções de combate.
- Incluir lojas, recompensas e mais usos para o sistema de moedas.
- Adicionar efeitos sonoros, música e ilustrações para enriquecer a experiência.
- Disponibilizar o jogo para jogar diretamente no navegador, adaptando a interface e a execução para a web.
- Criar testes automatizados para os sistemas de combate, inventário, exploração e salvamento.

## Autor

Will Vernen

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para os termos completos.
