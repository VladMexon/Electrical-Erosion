from gcode_parser import parse_gcode_movements
from ikpyErosion import interface
from model import calculate_crater_dimensions

def layer_number(movements):
    layers = 0
    for i in movements:
        if i["layer"] > layers:
            layers = i["layer"]
    return layers

def get_layer(movements, layer):
    return list(filter(lambda a : a['layer'] == layer, movements))

if __name__ == "__main__":
    C45_props = {
        "rho": 7875,    # кг/м^3 (Плотность)
        "r_v": 6339000, # Дж/кг (Теплота испарения)
        "L_m": 278000,  # Дж/кг (Теплота плавления)
        "C": 452,       # Дж/(кг·°C) (Удельная теплоемкость)
        "T_m": 1535,    # °C (Температура плавления)
        "T_b": 3050,    # °C (Температура кипения)
        "T_0": 20,      # °C (Начальная температура)
    }

    # Параметры электроэрозионной обработки (EDM)
    U_pulse = 160.0  # В (Напряжение импульса)
    I_pulse = 8.0    # А (Ток импульса)
    t_pulse = 100e-6 # с (Длительность импульса, 100 мкс) 
    C_a = 0.01       # Коэффициент использования энергии
    alpha_factor = 0.1 # Доля материала, удаляемого испарением
    
    # Диаметр электрода
    electrode_diameter = 0.003 # м (5 мм)
    
    # Количество разрядов
    discharges = 50000

    # 2. Вызов функции
    radius, depth = calculate_crater_dimensions(
        material_props=C45_props,
        U_pulse=U_pulse,
        I_pulse=I_pulse,
        t_pulse=t_pulse,
        C_a=C_a,
        alpha_factor=alpha_factor,
        electrode_diameter_m=electrode_diameter,
        num_discharges=discharges
    )

    urdf_file = "unnamed.urdf"
    target_orientation = [0, 0, -1]
    start_position = [200, -150, 300]

    movements = parse_gcode_movements("AA8_test1.gcode")
    target_positions = get_layer(movements, layer_number(movements))

    for i in range(len(target_positions) - 1):
        #print(target_positions[0:i + 1])
        interface(start_position, target_positions[0:i + 1], target_orientation, radius, depth, "./unnamed.urdf", False)