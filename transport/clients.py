class Client():
    def __init__(self, name, cargo_weight, is_vip = False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

    def __str__(self): 
        return f"Клиент: {self.name}. Вес груза: {self.cargo_weight}. VIP-статус: {self.is_vip}"