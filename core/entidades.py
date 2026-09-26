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

    def receber_dano(self, dano):
        dano_real = max(
            0, dano - self.defesa_base
        )  # O max(0, ...) impede que o dano fique negativo e cure o alvo
        self.vida -= dano_real
        if self.vida < 0:
            self.vida = 0
        return dano_real


class Jogador(Personagem):
    def __init__(self, nome):
        super().__init__(nome, level=1, vida_maxima=100, ataque_base=5, defesa_base=0)
        self.inventario = []
        self.arma_equipada = None
        # Sistema de economia usando dicionário
        self.dinheiro = {
            "cobre": 0,  # PC
            "prata": 0,  # PP
            "ouro": 0,  # PO
            "platina": 0,  # PL
        }

    def equipar_arma(self, nome_arma, bonus_ataque):
        self.arma_equipada = {"nome": nome_arma, "bonus": bonus_ataque}

    def calcular_ataque(self):
        if self.arma_equipada:
            return self.ataque_base + self.arma_equipada["bonus"]
        return self.ataque_base

    def adicionar_dinheiro(self, tipo_moeda, quantidade):
        if tipo_moeda in self.dinheiro:
            self.dinheiro[tipo_moeda] += quantidade

    def total_em_ouro(self):
        # Converte todo o dinheiro para a unidade padrão (Peças de Ouro)
        total = (
            (self.dinheiro["cobre"] / 100)
            + (self.dinheiro["prata"] / 10)
            + self.dinheiro["ouro"]
            + (self.dinheiro["platina"] * 10)
        )
        return total


class Inimigo(Personagem):
    def __init__(self, nome, level, vida_maxima, ataque_base, defesa_base):
        # O Inimigo é mais simples, pois não precisa de inventário ou equipamento neste momento
        super().__init__(nome, level, vida_maxima, ataque_base, defesa_base)
        # Flag para controlar se as informações estão ocultas
        self.analisado = False
