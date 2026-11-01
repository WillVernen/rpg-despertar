# O Despertar

**O Despertar** é um RPG de texto em desenvolvimento, criado em Python. Esta documentação apresenta os aspectos técnicos e os recursos do jogo sem revelar detalhes da aventura.

## Recursos disponíveis

- Menu principal para iniciar uma partida, carregar um jogo salvo ou sair.
- Combate por turnos com ataque, fuga quando permitida, uso de itens, consulta de status e análise de oponentes.
- Personagem com pontos de vida, ataque, defesa, equipamento, inventário e moedas.
- Progressão por experiência: derrotar inimigos concede XP e pode aumentar o nível, os atributos e os pontos de habilidade.
- Itens de cura utilizáveis durante a exploração e os combates.
- Exploração com caminhos alternativos, eventos, masmorra, floresta, acampamento seguro e mercador.
- Encontros com furtividade, emboscadas, combate e chance de fuga.
- Sistema de loja para comprar itens e equipamentos e negociar itens do inventário.
- Salvamento e carregamento local do progresso, incluindo dados do personagem, progressão e posição atual.

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

O jogo é executado no terminal e apresenta as instruções de cada ação na tela. Os dados salvos são armazenados localmente em `savegame.json`, criado ao salvar a partida.

## Estrutura do projeto

```text
.
|-- main.py              # Inicialização e fluxo principal do jogo
|-- core/
|   |-- combate.py       # Combate por turnos
|   |-- entidades.py     # Personagens, atributos, inventário e dinheiro
|   |-- exploracao.py    # Exploração, escolhas e progressão
|   |-- historia.py      # Introdução narrativa
|   |-- loja.py          # Compras e negociações
|   |-- menu.py          # Menu principal e limpeza da tela
|   |-- save.py          # Salvamento e carregamento local
|   `-- utils.py         # Exibição gradual de texto
|-- .gitignore           # Arquivos locais e temporários ignorados pelo Git
|-- LICENSE              # Licença MIT
`-- README.md            # Documentação do projeto
```

## Próximas melhorias

Possíveis evoluções para versões futuras:

- Expandir os sistemas de combate, equipamentos e progressão de personagem.
- Adicionar mais opções e consequências às escolhas de exploração.
- Ampliar os recursos de inventário, lojas e gerenciamento de itens.
- Criar testes automatizados para os sistemas do jogo.
- Adicionar recursos de áudio e elementos visuais.
- Adaptar a interface para disponibilizar o jogo em outras plataformas.

## Autor

Will Vernen

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para os termos completos.
