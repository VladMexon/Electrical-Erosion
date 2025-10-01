import math

def calculate_removed_volume_per_pulse(props, U, I, t_i, Ca, alpha):
    """Рассчитывает объем удаленного материала за один импульс."""
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

def calculate_time_for_depth(material_props, U_pulse, I_pulse, t_pulse, C_a, alpha_factor, electrode_diameter_m, target_depth_m):
    """
    Рассчитывает время, необходимое для достижения заданной глубины кратера.

    Args:
        material_props (dict): Свойства материала.
        U_pulse (float): Напряжение импульса (В).
        I_pulse (float): Ток импульса (А).
        t_pulse (float): Длительность импульса (с).
        C_a (float): Коэффициент использования энергии.
        alpha_factor (float): Доля материала, удаляемого испарением.
        electrode_diameter_m (float): Диаметр электрода (м).
        target_depth_m (float): Целевая глубина кратера (м).

    Returns:
        float: Общее время, необходимое для достижения глубины (с).
    """
    delta_V_m3_per_pulse = calculate_removed_volume_per_pulse(
        material_props, U_pulse, I_pulse, t_pulse, C_a, alpha_factor
    )
    
    if delta_V_m3_per_pulse <= 0:
        return float('inf') # Если за импульс ничего не удаляется, время будет бесконечным

    electrode_radius_m = electrode_diameter_m / 2
    actual_cut_area_m2 = math.pi * (electrode_radius_m**2)
    
    target_volume_m3 = target_depth_m * actual_cut_area_m2
    
    num_discharges_needed = target_volume_m3 / delta_V_m3_per_pulse
    
    total_time_s = num_discharges_needed * t_pulse
    
    return total_time_s

def get_crater_radius(electrode_diameter_m):
    """Возвращает радиус кратера (в мм)."""
    return (electrode_diameter_m / 2) * 1000

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
    electrode_diameter = 0.003 # м (3 мм)
    
    # Целевая глубина
    target_depth = 0.1 / 1000 # м (0.1 мм)

    # 2. Вызов функции
    required_time = calculate_time_for_depth(
        material_props=C45_props,
        U_pulse=U_pulse,
        I_pulse=I_pulse,
        t_pulse=t_pulse,
        C_a=C_a,
        alpha_factor=alpha_factor,
        electrode_diameter_m=electrode_diameter,
        target_depth_m=target_depth
    )
    
    radius_mm = get_crater_radius(electrode_diameter)

    # 3. Вывод результатов
    print(f"Для достижения глубины {target_depth * 1000} мм:")
    print(f"  Требуемое время обработки: {required_time:.4f} с")
    print(f"  Радиус кратера: {radius_mm} мм")
