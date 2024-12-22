import dearpygui.dearpygui as dpg
from transport import Client, Vehicle, Van, Ship, TransportCompany
import json
import time

company = TransportCompany("Company")
transport_list = ["Фургон", "Судно"]

client_row_count = 1
transport_row_count = 1

window_width, window_height = 1000, 800
popup_window_width, popup_window_height = 800, 400
state_button_width = 100
height_of_small_spacer = 10
height_of_medium_spacer = 30
height_of_big_spacer = 45
width_of_small_spacer = 15

def clear_client_fields():
    dpg.set_value("name_input", "")
    dpg.set_value("cargo_weight_input", "")
    dpg.set_value("vip_checkbox", False)

def clear_transport_fields():
    dpg.set_value("transport_type", "")
    dpg.set_value("capacity_input", "")

def to_dict_client(client_ex):
    return {
        "Имя клиента": client_ex.name,
        "Вес груза": client_ex.cargo_weight,
        "VIP статус": client_ex.is_vip
    }

def to_dict_transport(transport_ex):
    if isinstance(transport_ex, Ship):
        return {
            "Тип": "Судно",
            "Грузоподъемность": transport_ex.capacity,
            "Текущая загрузка": transport_ex.current_load,
            "Цвет": transport_ex.name
        }
    else:
        return {
            "Тип": "Фургон",
            "Грузоподъемность": transport_ex.capacity,
            "Текущая загрузка": transport_ex.current_load,
            "Наличие холодильника": transport_ex.is_refrigerated
        }

def save_data():
    data = {
        "Название компании": company.name,
        "Клиенты компании": [to_dict_client(client) for client in company.clients],
        "Транспорт компании": [to_dict_transport(vehicle) for vehicle in company.vehicles]
    }

    try:
        with open('company_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        dpg.set_value(
            "status_bar", "Данные успешно сохранены в файл: company_data.json")
    except Exception as e:
        dpg.set_value("status_bar", f"Ошибка при сохранении данных: {e}")

def show_warning_modal(message):
    time.sleep(0.1) 
    if not dpg.does_item_exist("warning_modal"):
        with dpg.window(tag="warning_modal", label="Предупреждение", modal=True, width=popup_window_width, height=popup_window_height, show=False, no_resize=True):
            dpg.add_text(tag="warning_message")
            dpg.add_spacer(height=height_of_small_spacer)
            dpg.add_button(label="Закрыть", callback=lambda: dpg.configure_item(
                "warning_modal", show=True))

    dpg.set_value("warning_message", message)
    dpg.configure_item("warning_modal", show=False)

def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)
    dpg.add_table_column(label="Выбор", parent="clients_table")
    dpg.add_table_column(label="Имя клиента", parent="clients_table")
    dpg.add_table_column(label="Вес груза", parent="clients_table")
    dpg.add_table_column(label="VIP статус", parent="clients_table")

    for idx, client in enumerate(company.clients):
        with dpg.table_row(parent="clients_table"):
            dpg.add_checkbox(tag=f"client_checkbox_{idx}")
            dpg.add_text(client.name)
            dpg.add_text(str(client.cargo_weight))
            dpg.add_text("Да" if client.is_vip else "Нет")

def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True)
    dpg.add_table_column(label="Выбор", parent="vehicles_table")
    dpg.add_table_column(label="ID", parent="vehicles_table")
    dpg.add_table_column(label="Тип", parent="vehicles_table")
    dpg.add_table_column(label="Грузоподъемность",
                         parent="vehicles_table")
    dpg.add_table_column(label="Текущая загрузка",
                         parent="vehicles_table")

    for vehicle in company.vehicles:
        with dpg.table_row(parent="vehicles_table"):
            checkbox_tag = f"vehicle_checkbox_{vehicle.vehicle_id}"
            dpg.add_checkbox(tag=checkbox_tag)
            dpg.add_text(str(vehicle.vehicle_id))
            dpg.add_text("Фургон" if isinstance(vehicle, Van) else "Судно")
            dpg.add_text(str(vehicle.capacity))
            dpg.add_text(str(vehicle.current_load))

def update_transport_fields():
    transport_mode = dpg.get_value("transport_type")
    
    if transport_mode == "Фургон":
        dpg.configure_item("refrigerated_checkbox", show=True)
        dpg.configure_item("ship_name_input", show=False)
    elif transport_mode == "Судно":
        dpg.configure_item("refrigerated_checkbox", show=False)
        dpg.configure_item("ship_name_input", show=True)
    else:
        dpg.configure_item("refrigerated_checkbox", show=False)
        dpg.configure_item("ship_name_input", show=False)

def update_distribution_table():
    existing_clients = set()

    dpg.delete_item("distribution_table", children_only=True)

    dpg.add_table_column(label="Имя клиента", parent="distribution_table")
    dpg.add_table_column(label="Вес груза", parent="distribution_table")
    dpg.add_table_column(label="VIP статус", parent="distribution_table")
    dpg.add_table_column(label="Транспорт ID", parent="distribution_table")
    dpg.add_table_column(label="Тип транспорта", parent="distribution_table")

    for vehicle in company.vehicles:
        for client in vehicle.clients_list:
            client_key = (client.name, client.cargo_weight)

            if client_key in existing_clients:
                continue

            existing_clients.add(client_key)

            with dpg.table_row(parent="distribution_table"):
                dpg.add_text(client.name)
                dpg.add_text(str(client.cargo_weight))
                dpg.add_text("Да" if client.is_vip else "Нет")
                dpg.add_text(vehicle.vehicle_id)
                dpg.add_text("Фургон" if isinstance(vehicle, Van) else "Судно")

    update_vehicles_table()
    dpg.set_value("status_bar", "Таблица распределения обновлена")

def delete_selected_client_object(table_tag, data_list, checkbox_prefix):
    items_to_delete = []

    for idx in range(len(data_list)):
        checkbox_tag = f"{checkbox_prefix}_{idx}"
        if dpg.does_item_exist(checkbox_tag) and dpg.get_value(checkbox_tag):
            items_to_delete.append(idx)

    if not items_to_delete:
        dpg.set_value("status_bar", "Выберите объект для удаления.")
        return

    for idx in sorted(items_to_delete, reverse=True):
        del data_list[idx]

    if table_tag == "clients_table":
        update_clients_table()

    dpg.set_value("status_bar", "Объект(ы) удалены")

def delete_selected_transport_object(table_tag, data_list, checkbox_prefix):
    items_to_delete = []

    for idx in range(len(data_list)):
        checkbox_tag = f"{checkbox_prefix}_{data_list[idx].vehicle_id}"
        if dpg.does_item_exist(checkbox_tag) and dpg.get_value(checkbox_tag):
            items_to_delete.append(idx)

    if not items_to_delete:
        dpg.set_value("status_bar", "Выберите объект для удаления.")
        return

    for idx in sorted(items_to_delete, reverse=True):
        if table_tag == "vehicles_table":
            vehicle = data_list[idx]
            print(f"Удаление транспорта: {vehicle}")
            del data_list[idx]
            update_vehicles_table()

    dpg.set_value("status_bar", "Объект(ы) удалены")

def create_new_client(sender, app_data):
    client_name = dpg.get_value("name_input")
    cargo_weight = dpg.get_value("cargo_weight_input")
    is_vip = dpg.get_value("vip_checkbox")

    if not client_name.strip() or not cargo_weight.strip():
        show_warning_modal("Ошибка: Все поля должны быть заполнены.")
        return False, "Ошибка добавления клиента: все поля должны быть заполнены."

    try:
        cargo_weight = float(cargo_weight)
    except ValueError:
        show_warning_modal("Ошибка: Вес груза должен быть числом.")
        dpg.set_value("cargo_weight_input", "") 
        return False, "Ошибка добавления клиента: вес груза должен быть числом."

    if not (client_name.isalpha() and len(client_name) >= 2):
        show_warning_modal(
            "Ошибка: Имя клиента должно содержать только буквы и быть длиной от 2 символов.")
        dpg.set_value("name_input", "")
        return False, "Ошибка добавления клиента: Имя клиента должно содержать только буквы и быть длиной от 2 символов."

    if not (0 < cargo_weight <= 10000):
        show_warning_modal(
            "Ошибка: Вес груза должен быть больше 0 и не более 10000 кг.")
        dpg.set_value("cargo_weight_input", "") 
        return False, "Ошибка добавления клиента: Вес груза должен быть положительным числом и не более 10000 кг."

    company.add_client(Client(client_name, cargo_weight, is_vip))
    update_clients_table()
    dpg.set_value("status_bar", "Клиент успешно добавлен!")
    dpg.configure_item("add_client_window", show=False)
    clear_client_fields()

def add_new_transport(sender, app_data):
    transport_mode = dpg.get_value("transport_type")
    capacity = dpg.get_value("capacity_input")
    refrigerated = dpg.get_value("refrigerated_checkbox")
    ship_name = dpg.get_value("ship_name_input")

    if not transport_mode.strip() or not capacity.strip():
        show_warning_modal("Ошибка: Все поля должны быть заполнены.")
        return

    try:
        capacity = float(capacity)
    except ValueError:
        show_warning_modal("Ошибка: Грузоподъемность должна быть числом.")
        dpg.set_value("capacity_input", "")
        return

    if capacity <= 0:
        show_warning_modal("Ошибка: Грузоподъемность должна быть больше 0.")
        dpg.set_value("capacity_input", "")
        return

    if transport_mode == "Фургон":
        company.add_vehicle(Van(0, capacity, refrigerated))
    else:
        company.add_vehicle(Ship(ship_name, capacity, ship_name))

    update_vehicles_table()
    dpg.set_value("status_bar", "Транспортное средство успешно добавлено!")
    dpg.configure_item("add_transport_window", show=False)
    clear_transport_fields()

def distribute_cargo():
    if not company.clients:
        dpg.set_value("status_bar", "Ошибка: В компании отсутствуют клиенты. Распределение невозможно.")
        return

    if not company.vehicles:
        dpg.set_value("status_bar", "Ошибка: В компании отсутствуют транспортные средства.")
        return
    company.optimize_cargo_distribution()
    update_distribution_table()
    dpg.set_value("status_bar", "Распределение грузов завершено успешно!")

dpg.create_context()

big_let_start = 0x00C0  
big_let_end = 0x00DF  
small_let_end = 0x00FF 
remap_big_let = 0x0410
alph_len = big_let_end - big_let_start + 1
alph_shift = remap_big_let - big_let_start
with dpg.font_registry():
    with dpg.font("fonts/Intro.otf", 20) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        biglet = remap_big_let 

        for i1 in range(big_let_start, big_let_end + 1):
            dpg.add_char_remap(i1, biglet) 
            dpg.add_char_remap(i1 + alph_len, biglet + alph_len)
            biglet += 1
        dpg.bind_font(default_font)

with dpg.window(tag="Main Window", label="Company",  width=window_width, height=window_height):
    with dpg.menu_bar():
        with dpg.menu(label="Файл"):
            dpg.add_menu_item(label="Экспорт результата", callback=save_data)

        dpg.add_spacer(width=width_of_small_spacer)

        with dpg.menu(label="Помощь"):
            dpg.add_menu_item(label="О программе", callback=lambda: dpg.configure_item(
                "about_window", show=True))

    dpg.add_spacer(height=height_of_big_spacer)

    with dpg.group(horizontal=True):
        dpg.add_button(label="Добавить клиента", callback=lambda: dpg.configure_item(
            "add_client_window", show=True))
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Добавить транспорт", callback=lambda: dpg.configure_item(
            "add_transport_window", show=True))
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Распределить грузы", callback=distribute_cargo)

    dpg.add_spacer(height=height_of_big_spacer)

    with dpg.table(header_row=True, tag="clients_table"):
        dpg.add_table_column(label="Имя клиента")
        dpg.add_table_column(label="Вес груза")
        dpg.add_table_column(label="VIP статус")

    dpg.add_spacer(height=height_of_medium_spacer)

    with dpg.table(header_row=True, tag="vehicles_table"):
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Тип")
        dpg.add_table_column(label="Грузоподъемность")
        dpg.add_table_column(label="Текущая загрузка")

    dpg.add_spacer(height=height_of_medium_spacer)

    with dpg.table(header_row=True, tag="distribution_table"):
        dpg.add_table_column(label="Имя клиента")
        dpg.add_table_column(label="Вес груза")
        dpg.add_table_column(label="VIP статус")
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Тип транспорта")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Удалить клиента", callback=lambda: delete_selected_client_object(
            "clients_table", company.clients, "client_checkbox"))
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Удалить транспорт", callback=lambda: delete_selected_transport_object(
            "vehicles_table", company.vehicles, "vehicle_checkbox"))

    dpg.add_spacer(height=height_of_medium_spacer)
    dpg.add_text("Статусная строка:")
    dpg.add_spacer(height=height_of_medium_spacer)
    dpg.add_text("", tag="status_bar")

with dpg.window(tag="about_window", label="О программе", modal=True, show=False, no_resize=True, width=popup_window_width, height=popup_window_height):
    dpg.add_text("Номер ЛР: 11 и 12")
    dpg.add_text("Вариант: 3")
    dpg.add_text("ФИО: Царёва А. А.")
    dpg.add_spacer(height=height_of_medium_spacer)
    dpg.add_button(label="Закрыть", callback=lambda: dpg.configure_item(
        "about_window", show=False))

with dpg.window(tag="add_client_window", label="Добавить клиента", modal=True, show=False, no_resize=True,  width=popup_window_width, height=popup_window_height):
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_input_text(label="Имя клиента", tag="name_input")
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_input_text(label="Вес груза", tag="cargo_weight_input")
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_checkbox(label="VIP статус", tag="vip_checkbox")
    dpg.add_spacer(height=height_of_medium_spacer)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Сохранить", callback=create_new_client)
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Отмена", callback=lambda: dpg.configure_item(
            "add_client_window", show=False))

with dpg.window(tag="add_transport_window", label="Добавить транспорт", modal=True, show=False, no_resize=True, width=popup_window_width, height=popup_window_height):
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_combo(label="Тип транспорта", items=transport_list, tag="transport_type", callback=lambda: update_transport_fields())
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_input_text(label="Грузоподъемность (тонны)", tag="capacity_input")
    dpg.add_spacer(height=height_of_small_spacer)
   
    dpg.add_checkbox(label="Наличие холодильника", tag="refrigerated_checkbox", show=False)
    dpg.add_spacer(height=height_of_small_spacer)
    
    dpg.add_input_text(label="Цвет судна", tag="ship_name_input", show=False)
    dpg.add_spacer(height=height_of_small_spacer)

    with dpg.group(horizontal=True):
        dpg.add_button(label="Сохранить", callback=add_new_transport)
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Отмена", callback=lambda: dpg.configure_item("add_transport_window", show=False))


dpg.create_viewport(title ="Company", width=window_width, height=window_height)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()


