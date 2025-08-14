def parse_gcode_movements(filename):
    movements = []
    # Сохраняем последние известные координаты, так как G-код модальный
    last_coords = {'X': 0, 'Y': 0, 'Z': 0, 'E': 0, 'F': 0, 'layer': 0}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Определяем слой. Gcode часто содержит комментарии вида ";LAYER:2", указывающие на начало нового слоя.
            if line.startswith(';LAYER:'):
                try:
                    # Обновляем номер слоя для последующих команд
                    last_coords['layer'] = int(line.split(':')[1])
                except (ValueError, IndexError):
                    # Игнорируем, если комментарий слоя имеет неверный формат
                    pass

            # Пропускаем комментарии и пустые строки
            if not line or line.startswith(';'):
                continue

            # Интересуют команды перемещения: G0 или G1
            if line.startswith(('G0', 'G1')):
                current_move = last_coords.copy()
                parts = line.split()
                has_move_command = False
                for p in parts:
                    if p.startswith(('X', 'Y', 'Z', 'E', 'F')):
                        try:
                            current_move[p[0]] = float(p[1:])
                            has_move_command = True
                        except ValueError:
                            print(f"Не удалось преобразовать координату: {p}")
                            pass
                
                # Добавляем движение, только если были команды перемещения
                if has_move_command:
                    movements.append(current_move)
                    # Обновляем последние известные координаты
                    last_coords = current_move

    return movements



if __name__ == "__main__":
    filename = "AA8_test1.gcode"  # путь к вашему файлу
    moves = parse_gcode_movements(filename)
    print(moves)
