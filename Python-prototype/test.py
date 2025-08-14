import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from gcode_parser import parse_gcode_movements 


def visualize_gcode_movements(movements):
    """
    Визуализирует траекторию движения из G-кода в 3D.
    Цветом обозначаются разные слои.
    """
    if not movements:
        print("Нет данных для визуализации.")
        return

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Разделение движений по слоям
    layers = {}
    for move in movements:
        layer = move.get('layer', 0)
        if layer not in layers:
            layers[layer] = {'X': [], 'Y': [], 'Z': []}
        layers[layer]['X'].append(move.get('X', 0))
        layers[layer]['Y'].append(move.get('Y', 0))
        layers[layer]['Z'].append(move.get('Z', 0))

    # Создание цветовой карты для слоев
    num_layers = len(layers)
    # Используем 'viridis' или другую карту, например 'jet' или 'rainbow'
    colors = plt.cm.viridis(np.linspace(0, 1, num_layers))

    for i, layer_num in enumerate(sorted(layers.keys())):
        layer_data = layers[layer_num]
        ax.plot(layer_data['X'], layer_data['Y'], layer_data['Z'], color=colors[i], label=f'Слой {layer_num}')

    ax.set_xlabel('X (мм)')
    ax.set_ylabel('Y (мм)')
    ax.set_zlabel('Z (мм)')
    ax.set_title('3D Визуализация траектории G-кода')

    # Добавляем легенду, если слоев не слишком много, чтобы не загромождать график
    if 0 < num_layers <= 20:
        ax.legend()

    # Установка равных масштабов для осей для корректного отображения
    all_x = [x for layer in layers.values() for x in layer['X']]
    all_y = [y for layer in layers.values() for y in layer['Y']]
    all_z = [z for layer in layers.values() for z in layer['Z']]

    if not all_x:
        plt.show()
        return

    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    z_min, z_max = min(all_z), max(all_z)

    # Вычисляем центр и диапазон для установки одинакового масштаба
    max_range = np.array([x_max - x_min, y_max - y_min, z_max - z_min]).max() / 2.0
    if max_range == 0: max_range = 1 # Избегаем деления на ноль для плоских моделей

    mid_x = (x_max + x_min) * 0.5
    mid_y = (y_max + y_min) * 0.5
    mid_z = (z_max + z_min) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.show()



if __name__ == "__main__":
    filename = "AA8_test.gcode"  # путь к вашему файлу
    moves = parse_gcode_movements(filename)
    # print(moves) # Можно раскомментировать для отладки
    visualize_gcode_movements(moves)

