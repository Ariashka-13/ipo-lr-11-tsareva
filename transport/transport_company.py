from .vehicle import Vehicle
from .clients import Client

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise ValueError("Транспортное средство должно быть экземпляром класса Vehicle или его подкласса")
        self.vehicles.append(vehicle)
        print(f"Транспортное средство {vehicle.vehicle_id} добавлено в компанию {self.name}")

    def all_vehicle(self):
        return self.vehicles

    def add_client(self, client):
        if not isinstance(client, Client):
            raise ValueError("Клиент должен быть экземпляром класса Client")
        self.clients.append(client)
        print(f"Клиент {client.name} добавлен в компанию {self.name}")

    def all_clients(self):
        return self.clients

    def optimize_cargo_distribution(self):
        vip_clients = [client for client in self.clients if client.is_vip]
        simple_clients = [client for client in self.clients if not client.is_vip]
        sorted_clients = vip_clients + simple_clients

        for client in sorted_clients:
            for vehicle in self.vehicles:
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    vehicle.load_cargo(client)
                    break
