# O Despertar

`O Despertar` e um RPG de texto em desenvolvimento, criado em Python. O jogador desperta sem memoria em um local desconhecido, encontra um bilhete misterioso e precisa sobreviver ao primeiro encontro nas sombras.

## Estado atual

O jogo ja conta com:

- menu principal com opcoes de novo jogo, carregar jogo e sair;
- introducao narrativa com nome personalizado para o jogador;
- sistema de entidades para jogador, inimigos e atributos basicos;
- combate por turnos contra o Esqueleto;
- ataques com calculo de dano e defesa;
- analise do inimigo para revelar seus atributos;
- consulta de status durante o combate sem gastar o turno;
- equipamento de arma, com a Viga de Madeira como arma inicial;
- inventario inicial e recompensa de uma Pocao de Cura apos a vitoria;
- sistema de moedas com cobre, prata, ouro e platina;
- recompensa de 15 pecas de cobre apos o primeiro combate;
- efeitos de texto gradual para reforcar a narrativa.

## Como executar

Requisito: Python 3 instalado.

Na pasta do projeto, execute:

```bash
python main.py
```

No Windows, tambem e possivel usar:

```bash
py main.py
```

## Controles do combate

Durante uma batalha, escolha uma das opcoes exibidas no terminal:

1. `Atacar` - causa dano usando a arma equipada.
2. `Fugir` - ainda bloqueada na batalha tutorial.
3. `Usar Item` - o uso de itens sera implementado nas proximas versoes.
4. `Verificar Status` - mostra os atributos do jogador sem gastar o turno.
5. `Analisar Inimigo` - revela os atributos do inimigo sem gastar o turno.

## Estrutura do projeto

```text
.
|-- main.py              # Inicializacao do jogo e fluxo principal
|-- core/
|   |-- combate.py       # Combate por turnos
|   |-- entidades.py     # Jogador, inimigos e atributos
|   |-- historia.py      # Introducao narrativa
|   |-- menu.py          # Menu principal e limpeza do terminal
|   `-- utils.py         # Efeitos de exibicao de texto
|-- LICENSE              # Licenca MIT
`-- README.md            # Documentacao do projeto
```

## Proximos passos

- implementar o uso de itens e a recuperacao de vida;
- implementar o sistema de salvamento e carregamento;
- continuar a historia depois do primeiro combate;
- adicionar novas areas, inimigos, equipamentos e escolhas.

## Licenca

Este projeto e distribuido sob a licenca MIT. Consulte o arquivo `LICENSE` para os termos completos.