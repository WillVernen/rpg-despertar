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
        self.dinheiro = {"cobre": 0, "prata": 0, "ouro": 0, "platina": 0}
        # NOVO: Dicionário para rastrear eventos do mundo (baús abertos, chefes mortos, portas destrancadas)
        self.progresso = {}

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
        return (
            (self.dinheiro["cobre"] / 100)
            + (self.dinheiro["prata"] / 10)
            + self.dinheiro["ouro"]
            + (self.dinheiro["platina"] * 10)
        )

    # --- NOVAS FUNÇÕES DE INVENTÁRIO ---
    def mostrar_inventario(self):
        if not self.inventario:
            print("Seu inventário está vazio.")
            return False

        print("\n--- INVENTÁRIO ---")
        for i, item in enumerate(self.inventario):
            efeito = f"Cura {item['valor']} HP" if item["tipo"] == "cura" else "Outro"
            print(f"{i + 1}. {item['nome']} ({efeito})")
        return True

    def usar_item(self, indice):
        if 0 <= indice < len(self.inventario):
            item = self.inventario[indice]

            if item["tipo"] == "cura":
                vida_anterior = self.vida
                # A função min() garante que a vida curada não ultrapasse a vida_maxima
                self.vida = min(self.vida + item["valor"], self.vida_maxima)
                vida_recuperada = self.vida - vida_anterior

                # Remove o item do inventário usando pop()
                self.inventario.pop(indice)
                return f"Você bebe a {item['nome']} e recupera {vida_recuperada} de HP!"

            # Aqui poderemos adicionar outros tipos de itens no futuro (venenos, buffs, etc.)
            return f"Você não pode usar {item['nome']} agora."
        return "Item inválido."


class Inimigo(Personagem):
    def __init__(self, nome, level, vida_maxima, ataque_base, defesa_base):
        # O Inimigo é mais simples, pois não precisa de inventário ou equipamento neste momento
        super().__init__(nome, level, vida_maxima, ataque_base, defesa_base)
        # Flag para controlar se as informações estão ocultas
        self.analisado = False
