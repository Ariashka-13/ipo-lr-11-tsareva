class Vehicle():
    def __init__(self, vehicle_id, capacity = 0, current_load = 0):
        self.vehicle_id = vehicle_id
        self.capacity = capacity
        self.current_load = current_load
        self.clients_list = []

    def load_cargo(self, client):
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Превышение грузоподъемности")
        if not isinstance(client.cargo_weight, (int, float)):
            raise ValueError("Вес груза должен иметь числовое значение")
        
        self.current_load += client.cargo_weight
        self.clients_list.append(client)
        
        print(f"Загружен груз весом {client.cargo_weight} т на транспортное средство ID {self.vehicle_id}. Текущая загрузка: {self.current_load} т")

    def __str__(self):
        return f"ID транспорта: {self.vehicle_id}. Грузоподъёмность: {self.capacity} т. Текущая загрузка: {self.current_load} т"
