class Personagem:
    def __init__(self, nome, level, vida_maxima, ataque_base, defesa_base):
        self.nome = nome
        self.level = level
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima
        self.ataque_base = ataque_base
        self.defesa_base = defesa_base

    def esta_vivo(self):
        return self.vida > 0

    def calcular_defesa(self):
        return self.defesa_base

    def receber_dano(self, dano):
        dano_real = max(0, dano - self.calcular_defesa())
        self.vida -= dano_real
        if self.vida < 0:
            self.vida = 0
        return dano_real


class Jogador(Personagem):
    def __init__(self, nome):
        super().__init__(nome, level=1, vida_maxima=100, ataque_base=5, defesa_base=0)

        # NOVO: Sistema de Mana (MP) para usar habilidades
        self.mana_maxima = 50
        self.mana = 50

        self.inventario = []
        self.arma_equipada = None
        self.armadura_equipada = None
        self.dinheiro = {"cobre": 0, "prata": 0, "ouro": 0, "platina": 0}
        self.progresso = {}

        self.xp = 0
        self.xp_necessario = 100
        self.pontos_habilidade = 0
        self.habilidades = []  # Lista de habilidades que o herói já aprendeu

    def equipar_arma(self, nome_arma, bonus_ataque):
        self.arma_equipada = {"nome": nome_arma, "bonus": bonus_ataque}

    def calcular_ataque(self):
        if self.arma_equipada:
            return self.ataque_base + self.arma_equipada["bonus"]
        return self.ataque_base

    def equipar_armadura(self, nome_armadura, bonus_defesa):
        self.armadura_equipada = {"nome": nome_armadura, "bonus": bonus_defesa}

    def calcular_defesa(self):
        if self.armadura_equipada:
            return self.defesa_base + self.armadura_equipada["bonus"]
        return self.defesa_base

    def adicionar_dinheiro(self, tipo_moeda, quantidade):
        if tipo_moeda in self.dinheiro:
            self.dinheiro[tipo_moeda] += quantidade

    def gastar_dinheiro(self, tipo_moeda, quantidade):
        if self.dinheiro[tipo_moeda] >= quantidade:
            self.dinheiro[tipo_moeda] -= quantidade
            return True

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

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        mensagens = [f"Você recebeu {quantidade} de XP!"]

        while self.xp >= self.xp_necessario:
            self.xp -= self.xp_necessario
            self.level += 1
            self.xp_necessario = int(self.xp_necessario * 1.5)

            # Evolução dos atributos
            self.vida_maxima += 20
            self.mana_maxima += 10  # NOVO: Ganha 10 de MP máximo por nível
            self.vida = self.vida_maxima
            self.mana = self.mana_maxima  # NOVO: Recupera o MP ao upar
            self.ataque_base += 2
            self.pontos_habilidade += 1

            mensagens.append(f"\n🌟 PARABÉNS! Você alcançou o Level {self.level}! 🌟")
            mensagens.append(
                f"HP Máximo: {self.vida_maxima} | MP Máximo: {self.mana_maxima} | Ataque: {self.ataque_base}"
            )
            mensagens.append("Sua saúde e energia foram totalmente restauradas!")
            mensagens.append("Você ganhou 1 Ponto de Habilidade (PH)!")

        return mensagens

    # Atualizado: Salvando o MP no JSON
    def to_dict(self):
        return {
            "nome": self.nome,
            "level": self.level,
            "vida_maxima": self.vida_maxima,
            "vida": self.vida,
            "mana_maxima": self.mana_maxima,  # <-- SALVANDO MP
            "mana": self.mana,  # <-- SALVANDO MP
            "ataque_base": self.ataque_base,
            "defesa_base": self.defesa_base,
            "inventario": self.inventario,
            "arma_equipada": self.arma_equipada,
            "armadura_equipada": self.armadura_equipada,
            "dinheiro": self.dinheiro,
            "progresso": self.progresso,
            "xp": self.xp,
            "xp_necessario": self.xp_necessario,
            "pontos_habilidade": self.pontos_habilidade,
            "habilidades": self.habilidades,
        }

    # Atualizado: Carregando o MP do JSON
    @classmethod
    def from_dict(cls, data):
        jogador = cls(data["nome"])
        jogador.level = data["level"]
        jogador.vida_maxima = data["vida_maxima"]
        jogador.vida = data["vida"]
        # NOVO: Se o save antigo não tiver MP, inicia com 50
        jogador.mana_maxima = data.get("mana_maxima", 50)
        jogador.mana = data.get("mana", 50)
        jogador.ataque_base = data["ataque_base"]
        jogador.defesa_base = data["defesa_base"]
        jogador.inventario = data.get("inventario", [])
        jogador.arma_equipada = data.get("arma_equipada", None)
        jogador.armadura_equipada = data.get("armadura_equipada", None)
        jogador.dinheiro = data.get(
            "dinheiro", {"cobre": 0, "prata": 0, "ouro": 0, "platina": 0}
        )
        jogador.progresso = data.get("progresso", {})
        jogador.xp = data.get("xp", 0)
        jogador.xp_necessario = data.get("xp_necessario", 100)
        jogador.pontos_habilidade = data.get("pontos_habilidade", 0)
        jogador.habilidades = data.get("habilidades", [])
        return jogador


class Inimigo(Personagem):
    # NOVO: Adicionamos o xp_recompensa no construtor
    def __init__(
        self, nome, level, vida_maxima, ataque_base, defesa_base, xp_recompensa=0
    ):
        super().__init__(nome, level, vida_maxima, ataque_base, defesa_base)
        self.analisado = False
        self.xp_recompensa = xp_recompensa
