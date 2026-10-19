class Personagem:
    def __init__(self, nome, level, vida_maxima, ataque_base, defesa_base):
        self.nome = nome
        self.level = level
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima  # A vida atual começa igual à máxima
        self.ataque_base = ataque_base
        self.defesa_base = defesa_base

    def esta_vivo(self):
        return self.vida > 0

    # NOVO: Adicionamos a função base aqui para que o Inimigo não quebre o jogo
    def calcular_defesa(self):
        return self.defesa_base

    def receber_dano(self, dano):
        dano_real = max(
            0, dano - self.calcular_defesa()
        )  # Agora funciona tanto para o Jogador quanto para o Inimigo
        self.vida -= dano_real
        if self.vida < 0:
            self.vida = 0
        return dano_real


class Jogador(Personagem):
    def __init__(self, nome):
        super().__init__(nome, level=1, vida_maxima=100, ataque_base=5, defesa_base=0)
        self.inventario = []
        self.arma_equipada = None
        self.armadura_equipada = None  # NOVO: Slot de armadura/escudo
        self.dinheiro = {"cobre": 0, "prata": 0, "ouro": 0, "platina": 0}
        self.progresso = {}

    def equipar_arma(self, nome_arma, bonus_ataque):
        self.arma_equipada = {"nome": nome_arma, "bonus": bonus_ataque}

    def calcular_ataque(self):
        if self.arma_equipada:
            return self.ataque_base + self.arma_equipada["bonus"]
        return self.ataque_base

    # NOVO: Sistema de Defesa
    def equipar_armadura(self, nome_armadura, bonus_defesa):
        self.armadura_equipada = {"nome": nome_armadura, "bonus": bonus_defesa}

    # NOVO: Calcula a defesa total
    def calcular_defesa(self):
        if self.armadura_equipada:
            return self.defesa_base + self.armadura_equipada["bonus"]
        return self.defesa_base

    def adicionar_dinheiro(self, tipo_moeda, quantidade):
        if tipo_moeda in self.dinheiro:
            self.dinheiro[tipo_moeda] += quantidade

    # NOVO: Função para comprar itens (Prioriza o gasto exato)
    def gastar_dinheiro(self, tipo_moeda, quantidade):
        # 1. Tenta pagar com a moeda solicitada primeiro (para não bagunçar as outras moedas)
        if self.dinheiro[tipo_moeda] >= quantidade:
            self.dinheiro[tipo_moeda] -= quantidade
            return True

        # 2. Se não houver moedas daquele tipo suficientes, aciona o sistema de troco
        valores_em_pc = {"cobre": 1, "prata": 10, "ouro": 100, "platina": 1000}

        custo_total_pc = quantidade * valores_em_pc[tipo_moeda]

        riqueza_total_pc = (
            (self.dinheiro["cobre"] * 1)
            + (self.dinheiro["prata"] * 10)
            + (self.dinheiro["ouro"] * 100)
            + (self.dinheiro["platina"] * 1000)
        )

        if riqueza_total_pc >= custo_total_pc:
            troco_pc = riqueza_total_pc - custo_total_pc

            self.dinheiro["platina"] = troco_pc // 1000
            troco_pc %= 1000

            self.dinheiro["ouro"] = troco_pc // 100
            troco_pc %= 100

            self.dinheiro["prata"] = troco_pc // 10
            troco_pc %= 10

            self.dinheiro["cobre"] = troco_pc
            return True

        return False

    def total_em_ouro(self):
        return (
            (self.dinheiro["cobre"] / 100)
            + (self.dinheiro["prata"] / 10)
            + self.dinheiro["ouro"]
            + (self.dinheiro["platina"] * 10)
        )

    def mostrar_inventario(self):
        if not self.inventario:
            print("Seu inventário está vazio.")
            return False

        print("\n--- INVENTÁRIO ---")
        for i, item in enumerate(self.inventario):
            efeito = (
                f"Cura {item['valor']} HP" if item["tipo"] == "cura" else "Diversos"
            )
            print(f"{i + 1}. {item['nome']} ({efeito})")
        return True

    def usar_item(self, indice):
        if 0 <= indice < len(self.inventario):
            item = self.inventario[indice]

            if item["tipo"] == "cura":
                vida_anterior = self.vida
                self.vida = min(self.vida + item["valor"], self.vida_maxima)
                vida_recuperada = self.vida - vida_anterior
                self.inventario.pop(indice)
                return f"Você bebe a {item['nome']} e recupera {vida_recuperada} de HP!"

            return f"Você não pode usar {item['nome']} agora."
        return "Item inválido."

    def to_dict(self):
        return {
            "nome": self.nome,
            "level": self.level,
            "vida_maxima": self.vida_maxima,
            "vida": self.vida,
            "ataque_base": self.ataque_base,
            "defesa_base": self.defesa_base,
            "inventario": self.inventario,
            "arma_equipada": self.arma_equipada,
            "armadura_equipada": self.armadura_equipada,  # Atualizado para o Save
            "dinheiro": self.dinheiro,
            "progresso": self.progresso,
        }

    @classmethod
    def from_dict(cls, data):
        jogador = cls(data["nome"])
        jogador.level = data["level"]
        jogador.vida_maxima = data["vida_maxima"]
        jogador.vida = data["vida"]
        jogador.ataque_base = data["ataque_base"]
        jogador.defesa_base = data["defesa_base"]
        jogador.inventario = data.get("inventario", [])
        jogador.arma_equipada = data.get("arma_equipada", None)
        jogador.armadura_equipada = data.get(
            "armadura_equipada", None
        )  # Atualizado para o Load
        jogador.dinheiro = data.get(
            "dinheiro", {"cobre": 0, "prata": 0, "ouro": 0, "platina": 0}
        )
        jogador.progresso = data.get("progresso", {})
        return jogador


class Inimigo(Personagem):
    def __init__(self, nome, level, vida_maxima, ataque_base, defesa_base):
        # O Inimigo é mais simples, pois não precisa de inventário ou equipamento neste momento
        super().__init__(nome, level, vida_maxima, ataque_base, defesa_base)
        # Flag para controlar se as informações estão ocultas
        self.analisado = False
