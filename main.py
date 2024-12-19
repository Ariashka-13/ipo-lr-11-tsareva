from transport import Client, Vehicle, Van, Ship, TransportCompany

def main():
    
    name = input("Введите имя компании: ")
    company = TransportCompany(name)
    
    def menu():
        print("""
              МЕНЮ 
            1 - Вывести всех клиентов
            2 - Вывести все транспортные средства
            3 - Добавить клиентов
            4 - Добавить транспорт
            5 - Распределение грузов клиентов
            6 - Выход из программы
              """)

    def all_clients():
        for client in company.clients:
            print(client) 

    def all_vehicle():
        for vehicle in company.vehicles:
            print(vehicle)

    def add_clients():
        name = input("Введите имя клиента: ")
        
        while True:
            cargo_weight = input("Введите вес груза: ")
            if cargo_weight.replace('.', '', 1).isdigit() and float(cargo_weight) > 0:
                cargo_weight = float(cargo_weight)
                break
            else:
                print("Некорректный ввод")
        
        while True:
            is_vip = input("Есть ли VIP-статус?: ").lower()
            if is_vip in ['true', 'да']:
                is_vip = 'True'
                break
            elif is_vip in ['false', 'нет']:
                is_vip = 'False'
                break
            else:
                print("Некорректный ввод")

        company.add_client(Client(name, cargo_weight, is_vip))

    def add_vehicles():
        while True:
            vehicle_id = input("Введите id для транспорта: ")
            if vehicle_id.isdigit():
                break
            else:
                print("Некорректный ввод")

        vehicle_type = input("Введите вид транспорта: ")

        while True:
            capacity = input("Введите грузоподъёмность(в тоннах): ")
            if capacity.replace('.', '', 1).isdigit() and float(capacity) > 0:
                capacity = float(capacity)
                break
            else:
                print("Некорректный ввод")
        
        if vehicle_type in ["van", "фургон"]:
            while True:
                is_refrigerated = input("Есть ли холодильник? ").lower()
                if is_refrigerated in ['true', 'да']:
                    is_refrigerated = 'True'
                    break
                elif is_refrigerated in ['false', 'нет']:
                    is_refrigerated = 'False'
                    break
                else:
                    print("Некорректный ввод")
            
            company.add_vehicle(Van(vehicle_id, capacity, is_refrigerated))

        elif vehicle_type in ["ship", "судно"]:
            name = input("Введите цвет судна: ")
            company.add_vehicle(Ship(vehicle_id, capacity, name))
        else:
            print("Ошибка")

    def optimize():
        company.optimize_cargo_distribution()
        print("Оптимизировано грузы клиентов")

    def end():
        print("Выход из программы")
        exit()

    while True:
        menu()

        n = input("Введите номер пункта: ")

        if n.isdigit():
            n = int(n)
            if n == 1:
                all_clients()
            elif n == 2:
                all_vehicle()
            elif n == 3:
                add_clients()
            elif n == 4:
                add_vehicles()
            elif n == 5:
                optimize()
            elif n == 6:
                end()
            else:
                print("Ошибка")
        else:
            print("Ошибка: введено не числовое значение")

if __name__ == "__main__":
    main()
