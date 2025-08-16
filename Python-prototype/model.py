import math

def calculate_crater_dimensions(material_props, U_pulse, I_pulse, t_pulse, C_a, alpha_factor, electrode_diameter_m, num_discharges):
    """
    Рассчитывает и возвращает радиус и глубину кратера, образовавшегося в результате
    электроэрозионной обработки.

    Args:
        material_props (dict): Словарь со свойствами материала.
        U_pulse (float): Напряжение импульса (В).
        I_pulse (float): Ток импульса (А).
        t_pulse (float): Длительность импульса (с).
        C_a (float): Коэффициент использования энергии.
        alpha_factor (float): Доля материала, удаляемого испарением.
        electrode_diameter_m (float): Диаметр электрода (м).
        num_discharges (int): Количество разрядов.

    Returns:
        tuple: Кортеж, содержащий радиус кратера (м) и глубину кратера (м).
    """
    
    # --- 1. Вспомогательная функция для расчета объема удаленного материала ЗА ОДИН РАЗРЯД ---
    def calculate_removed_volume_per_pulse(props, U, I, t_i, Ca, alpha):
        E_c = U * I * t_i
        E_rem = Ca * E_c
        rho = props["rho"]
        r_v = props["r_v"]
        L_m = props["L_m"]
        C_spec = props["C"]
        T_m = props["T_m"]
        T_b = props["T_b"]
        T_0 = props["T_0"]
        denominator = rho * (
            alpha * r_v + L_m +
            alpha * C_spec * (T_b - T_0) +
            (1 - alpha) * C_spec * (T_m - T_0)
        )
        if denominator == 0: return 0.0
        return E_rem / denominator

    # --- 2. Расчет объема и глубины ---
    delta_V_m3_per_pulse = calculate_removed_volume_per_pulse(
        material_props, U_pulse, I_pulse, t_pulse, C_a, alpha_factor
    )
    
    total_delta_V_m3_for_crater = delta_V_m3_per_pulse * num_discharges
    
    electrode_radius_m = electrode_diameter_m / 2
    actual_cut_area_m2 = math.pi * (electrode_radius_m**2)
    
    depth = total_delta_V_m3_for_crater / actual_cut_area_m2 if actual_cut_area_m2 > 0 else 0
    
    return electrode_radius_m * 1000, depth * 1000

if __name__ == '__main__':
    # --- Пример использования ---

    # 1. Свойства материала и параметры симуляции
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
    electrode_diameter = 0.005 # м (5 мм)
    
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

    # 3. Вывод результатов
    print(f"Расчет для {discharges} разрядов:")
    print(f"  Радиус кратера: {radius} мм")
    print(f"  Глубина кратера: {depth} мм")