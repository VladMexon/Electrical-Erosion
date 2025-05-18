import math

# --- 0. Глобальный коэффициент масштабирования для визуализации ---
global_visual_scale_factor = 1000.0 # Увеличиваем все в 10 раз для OpenSCAD

# --- 1. Свойства материала и параметры симуляции ---
C45_props = {
    "rho": 7875,    # кг/м^3 (Плотность)
    "r_v": 6339000, # Дж/кг (Теплота испарения)
    "L_m": 278000,  # Дж/кг (Теплота плавления)
    "C": 452,       # Дж/(кг·°C) (Удельная теплоемкость)
    "T_m": 1535,    # °C (Температура плавления)
    "T_b": 3050,    # °C (Температура кипения)
    "T_0": 20,      # °C (Начальная температура)
}
material_props = C45_props

# Параметры электроэрозионной обработки (EDM)
U_pulse = 160.0  # В (Напряжение импульса)
I_pulse = 8.0    # А (Ток импульса)
t_pulse = 100e-6 # с (Длительность импульса, 100 мкс) 
C_a = 0.01       # Коэффициент использования энергии
alpha_factor = 0.1 # Доля материала, удаляемого испарением

# --- 2. Фактические размеры заготовки и электрода (в метрах) ---
actual_wp_dim_x_m = 0.100  # Фактическая ширина заготовки (10 см)
actual_wp_dim_y_m = 0.050  # Фактическая длина заготовки (5 см)
actual_wp_dim_z_m = 0.005  # Фактическая высота/толщина заготовки (5 мм)

actual_electrode_diameter_m = 0.005 # Фактический диаметр электрода (5 мм)
actual_electrode_radius_m = actual_electrode_diameter_m / 2
actual_electrode_height_display_m = actual_wp_dim_z_m * 1.5 # Высота отображаемого электрода

# --- 3. Управление симуляцией ---
# Количество разрядов для каждого из ТРЕХ кратеров
discharges_for_craters = [10000, 50000, 100000] 

# --- 4. Вспомогательная функция для расчета объема удаленного материала ЗА ОДИН РАЗРЯД ---
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

# --- 5. Расчет ФАКТИЧЕСКИХ глубин для каждого кратера ---
delta_V_m3_per_pulse = calculate_removed_volume_per_pulse(
    material_props, U_pulse, I_pulse, t_pulse, C_a, alpha_factor
)
actual_cut_area_m2 = math.pi * (actual_electrode_radius_m**2) 

actual_crater_depths_m = []
for num_discharges in discharges_for_craters:
    total_delta_V_m3_for_crater = delta_V_m3_per_pulse * num_discharges
    depth = total_delta_V_m3_for_crater / actual_cut_area_m2 if actual_cut_area_m2 > 0 else 0
    actual_crater_depths_m.append(depth)

# --- 6. Подготовка масштабированных размеров для OpenSCAD ---
scad_wp_dx = actual_wp_dim_x_m * global_visual_scale_factor
scad_wp_dy = actual_wp_dim_y_m * global_visual_scale_factor
scad_wp_dz = actual_wp_dim_z_m * global_visual_scale_factor

scad_electrode_diameter = actual_electrode_diameter_m * global_visual_scale_factor
scad_electrode_height_display = actual_electrode_height_display_m * global_visual_scale_factor

scad_cut_diameter = scad_electrode_diameter 

scad_physical_crater_depths = [depth * global_visual_scale_factor for depth in actual_crater_depths_m]

scad_crater_x_positions = [
    scad_wp_dx * 0.25,
    scad_wp_dx * 0.50,
    scad_wp_dx * 0.75,
]
scad_crater_y_position = scad_wp_dy / 2 

# --- 7. Функция для генерации кода OpenSCAD ---
def generate_openscad_code(
    wp_dx_scad, wp_dy_scad, wp_dz_scad,
    electrode_dia_scad, 
    electrode_h_display_scad,
    craters_data_scad, 
    common_y_pos_scad,
    electrode_final_pos_x_scad, electrode_final_pos_y_scad, electrode_final_pos_z_tip_scad
):
    
    # Небольшая величина для "выступа" вычитаемых цилиндров, чтобы избежать Z-fighting
    # Зависит от масштабированной толщины заготовки
    scad_epsilon = wp_dz_scad * 0.05 

    craters_difference_str = ""
    for idx, (x_pos, physical_depth_scad) in enumerate(craters_data_scad):
        
        # Определяем, является ли кратер сквозным на основе его физической (масштабированной) глубины
        is_through_cut = (physical_depth_scad >= wp_dz_scad - (1e-9 * global_visual_scale_factor)) # Небольшой допуск для сравнения float

        current_cylinder_base_z_scad = 0
        current_cylinder_height_scad = 0

        if is_through_cut:
            # Для сквозных кратеров: цилиндр начинается ниже заготовки и заканчивается выше нее
            current_cylinder_base_z_scad = -scad_epsilon 
            current_cylinder_height_scad = wp_dz_scad + 2 * scad_epsilon # Проходит через всю заготовку + два эпсилон
        else:
            # Для несквозных кратеров: база на физической глубине, верх чуть выше поверхности заготовки
            current_cylinder_base_z_scad = wp_dz_scad - physical_depth_scad
            current_cylinder_height_scad = physical_depth_scad + scad_epsilon
        
        craters_difference_str += f"""
        // Кратер {idx + 1} (физ. глубина SCAD: {physical_depth_scad:.4f})
        translate([{x_pos}, {common_y_pos_scad}, {current_cylinder_base_z_scad}]) 
            cylinder(
                h = {current_cylinder_height_scad}, 
                d = {electrode_dia_scad},
                center = false 
            );"""
        electrode_final_pos_x_scad = x_pos # Чтобы электрод был над последним кратером
    openscad_script = f"""// OpenSCAD код, сгенерированный Python-скриптом
// Моделируется {len(craters_data_scad)} КРАТЕРА с разным количеством разрядов.
// Глубина каждого кратера ОСНОВАНА НА ФИЗИЧЕСКОМ РАСЧЕТЕ.
// Вычитаемые цилиндры немного удлинены для избежания Z-fighting.
// Все размеры УЖЕ МАСШТАБИРОВАНЫ для OpenSCAD с коэффициентом {global_visual_scale_factor}.
$fn = 32; // Количество граней для цилиндров

// --- Определения модулей ---
module workpiece(dim_x, dim_y, dim_z) {{
    color("lightgray")
    cube([dim_x, dim_y, dim_z], center = false);
}}

module electrode_tool_shape(diameter, height) {{
    color("darkred", 0.7)
    cylinder(h = height, d = diameter, center = false); 
}}

// --- Основная сборка ---
difference() {{
    workpiece({wp_dx_scad}, {wp_dy_scad}, {wp_dz_scad});
    {craters_difference_str}
}}

translate([{electrode_final_pos_x_scad}, {electrode_final_pos_y_scad}, {electrode_final_pos_z_tip_scad}])
    electrode_tool_shape(diameter = {electrode_dia_scad}, height = {electrode_h_display_scad});

// --- Информация для отладки (в единицах SCAD, т.е. масштабированных) ---
// Фактический коэффициент масштабирования: {global_visual_scale_factor}
// Заготовка (SCAD): X={wp_dx_scad}, Y={wp_dy_scad}, Z={wp_dz_scad}
// Электрод/Вырез (SCAD): диаметр={electrode_dia_scad}
// --- Фактические (немасштабированные) расчетные значения (в метрах) ---
// delta_V за 1 разряд: {delta_V_m3_per_pulse} м^3
"""
    for i in range(len(discharges_for_craters)):
        openscad_script += f"""
// Кратер {i+1}: {discharges_for_craters[i]} разрядов, Физическая глубина (немасштаб.): {actual_crater_depths_m[i]} м, Глубина в SCAD: {scad_physical_crater_depths[i]}
"""
    return openscad_script

if __name__ == "__main__":
    scad_electrode_final_pos_x = scad_wp_dx / 2
    scad_electrode_final_pos_y = scad_wp_dy / 2
    scad_electrode_final_pos_z_tip = scad_wp_dz + (scad_electrode_diameter * 0.2) 

    scad_craters_data = []
    for i in range(len(scad_crater_x_positions)):
        scad_craters_data.append((scad_crater_x_positions[i], scad_physical_crater_depths[i]))

    scad_code_output = generate_openscad_code(
        wp_dx_scad = scad_wp_dx,
        wp_dy_scad = scad_wp_dy,
        wp_dz_scad = scad_wp_dz,
        electrode_dia_scad = scad_electrode_diameter,
        electrode_h_display_scad = scad_electrode_height_display,
        craters_data_scad = scad_craters_data,
        common_y_pos_scad = scad_crater_y_position,
        electrode_final_pos_x_scad = scad_electrode_final_pos_x,
        electrode_final_pos_y_scad = scad_electrode_final_pos_y,
        electrode_final_pos_z_tip_scad = scad_electrode_final_pos_z_tip
    )

    output_filename = "edm_simulation.scad" # Имя файла остается прежним, будет перезаписан
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(scad_code_output)
        print(f"OpenSCAD скрипт успешно сгенерирован: {output_filename}")
        print(f"  Моделируется {len(discharges_for_craters)} КРАТЕРА.")
        print(f"  Глобальный коэффициент визуального масштабирования: {global_visual_scale_factor}")
        print(f"  Фактический диаметр электрода: {actual_electrode_diameter_m*1000:.1f} мм")
        print(f"  Объем удаляемый за 1 разряд: {delta_V_m3_per_pulse:.4e} м^3")
        for i in range(len(discharges_for_craters)):
            print(f"  Кратер {i+1}:")
            print(f"    Количество разрядов: {discharges_for_craters[i]}")
            print(f"    Общий объем для кратера: {delta_V_m3_per_pulse * discharges_for_craters[i]:.4e} м^3")
            print(f"    ФИЗИЧЕСКАЯ расчетная глубина: {actual_crater_depths_m[i]*1000:.3f} мм")
            print(f"    Глубина в SCAD (масштабированная физическая): {scad_physical_crater_depths[i]:.4f}")
        
    except IOError:
        print(f"Ошибка: Не удалось записать файл {output_filename}")

