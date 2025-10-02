import math
import numpy as np
import os
from gcode_parser import parse_gcode_movements
from ikpyErosion import generate_config
from model import calculate_time_for_depth, get_crater_radius

def get_layer_movements(movements, layer_index):
    """Возвращает движения для указанного слоя."""
    return list(filter(lambda a: a['layer'] == layer_index, movements))

def filter_extrusion_movements(target_positions):
    """Отфильтровывает движения без экструзии."""
    positions = []
    last_e = 0
    for move in target_positions:
        if move["E"] > last_e:
            last_e = move["E"]
            positions.append(move)
    return positions

def get_layer_height(movements, layer_index):
    """Рассчитывает высоту (толщину) слоя в метрах."""
    if layer_index == 0:
        # Для первого слоя высота - это первая Z координата
        first_move_z = next((m['Z'] for m in movements if m['layer'] == 0 and 'Z' in m), 0)
        return first_move_z / 1000 # в метры
    
    current_layer_moves = get_layer_movements(movements, layer_index)
    prev_layer_moves = get_layer_movements(movements, layer_index - 1)
    
    if not current_layer_moves or not prev_layer_moves:
        return 0.0 # Невозможно рассчитать

    # Средняя Z для текущего и предыдущего слоев
    avg_z_current = np.mean([m['Z'] for m in current_layer_moves if 'Z' in m])
    avg_z_prev = np.mean([m['Z'] for m in prev_layer_moves if 'Z' in m])
    
    height = abs(avg_z_current - avg_z_prev) / 1000 # в метры
    return height if height > 0 else 0.2 / 1000 # Запасной вариант, если высота слоя 0

if __name__ == "__main__":
    os_id = os.name
    # --- Параметры материала и обработки ---
    C45_props = {
        "rho": 7875, "r_v": 6339000, "L_m": 278000, "C": 452,
        "T_m": 1535, "T_b": 3050, "T_0": 20,
    }
    U_pulse = 160.0
    I_pulse = 8.0
    t_pulse = 100e-6
    C_a = 0.01
    alpha_factor = 0.1
    electrode_diameter = 0.002 # м (2 мм)

    # --- Настройки симуляции ---
    dt = 1  # с (временной шаг симуляции)
    urdf_file = "unnamed.urdf"
    target_orientation = [0, 0, -1]
    # Смещение системы координат G-кода относительно мировой системы координат робота
    gcode_offset = np.array([200.0, -150.0, 300.0])
    start_position = gcode_offset  # Начинаем в точке отсчета G-кода

    # --- Загрузка и обработка G-кода ---
    gcode_file = "AA8_test1.gcode"
    all_movements = parse_gcode_movements(gcode_file)
    
    # Определяем последний слой для обработки
    last_layer_index = max(m['layer'] for m in all_movements)
    target_movements = filter_extrusion_movements(get_layer_movements(all_movements, last_layer_index))
    
    if not target_movements:
        print("Нет движений для обработки.")
        exit()

    # --- Инициализация симуляции ---
    layer_depth_m = get_layer_height(all_movements, last_layer_index)
    print(f"Глубина слоя: {layer_depth_m * 1000:.4f} мм")

    drilling_time_per_hole = calculate_time_for_depth(
        C45_props, U_pulse, I_pulse, t_pulse, C_a, alpha_factor, 
        electrode_diameter, layer_depth_m
    )
    print(f"Расчетное время обработки одной лунки: {drilling_time_per_hole:.4f} с")

    crater_radius_mm = get_crater_radius(electrode_diameter)
    crater_diameter_mm = crater_radius_mm * 2

    # --- Генерация плотной очереди точек для сверления ---
    point_queue_local = [] # Теперь будет список словарей

    if target_movements:
        # Добавляем первую точку G-кода
        first_move = target_movements[0]
        point_queue_local.append({
            'pos': np.array([first_move['X'], first_move['Y'], first_move['Z']]),
            'feed_rate': first_move.get('F', 3000) / 60
        })

        # Проходим по сегментам пути
        for i in range(len(target_movements) - 1):
            m1 = target_movements[i]
            m2 = target_movements[i+1]
            
            p1 = np.array([m1['X'], m1['Y'], m1['Z']])
            p2 = np.array([m2['X'], m2['Y'], m2['Z']])
            
            segment_vector = p2 - p1
            segment_length = np.linalg.norm(segment_vector)
            
            # Скорость для этого сегмента
            segment_feed_rate = m2.get('F', 3000) / 60

            # Если сегмент длиннее диаметра лунки, заполняем его
            if segment_length > crater_diameter_mm:
                direction_vector = segment_vector / segment_length
                
                num_holes = math.floor(segment_length / crater_diameter_mm)
                
                for j in range(1, num_holes):
                    new_point_pos = p1 + direction_vector * j * crater_diameter_mm
                    point_queue_local.append({'pos': new_point_pos, 'feed_rate': segment_feed_rate})
            
            # Всегда добавляем конечную точку сегмента из G-кода
            point_queue_local.append({'pos': p2, 'feed_rate': segment_feed_rate})

    # Применяем глобальное смещение ко всем точкам
    point_queue = [{'pos': p['pos'] + gcode_offset, 'feed_rate': p['feed_rate']} for p in point_queue_local]
    print(f"Сгенерировано {len(point_queue)} точек для обработки.")

    if not point_queue:
        print("Очередь точек пуста, симуляция не будет запущена.")
        exit()

    completed_holes = []
    current_pos = start_position
    current_point_index = 0
    state = "MOVING" # Состояния: MOVING, DRILLING, IDLE
    drilling_timer = 0

    # --- Основной цикл симуляции ---
    while state != "IDLE":
        # Целевая точка для текущего движения или сверления
        target_item = point_queue[current_point_index]
        target_pos = target_item['pos']
        
        if state == "MOVING":
            move_vector = target_pos - current_pos
            distance = np.linalg.norm(move_vector)
            
            # Скорость из g-кода (мм/мин) -> мм/с
            feed_rate = target_item['feed_rate']
            
            if distance > 0:
                move_step = move_vector / distance * feed_rate * dt
                if np.linalg.norm(move_step) >= distance:
                    current_pos = target_pos
                    state = "DRILLING"
                    drilling_timer = drilling_time_per_hole
                else:
                    current_pos += move_step
            else: # Если уже в точке
                state = "DRILLING"
                drilling_timer = drilling_time_per_hole

        elif state == "DRILLING":
            drilling_timer -= dt
            if drilling_timer <= 0:
                # Добавляем завершенную лунку в список для отрисовки
                completed_holes.append(target_pos.tolist())
                
                current_point_index += 1
                if current_point_index >= len(point_queue):
                    state = "IDLE"
                else:
                    state = "MOVING"
        
        # --- Отрисовка кадра ---
        # Для IK используется текущее положение, для `cuts` - все завершенные лунки
        render_positions = completed_holes + [current_pos.tolist()]
        generate_config(render_positions, target_orientation, crater_radius_mm, layer_depth_m * 1000, urdf_file,  os_id,True)
        

    print("Симуляция завершена.")
