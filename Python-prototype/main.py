from gcode_parser import parse_gcode_movements
from ikpyErosion import interface

def layer_number(movements):
    layers = 0
    for i in movements:
        if i["layer"] > layers:
            layers = i["layer"]
    return layers

def get_layer(movements, layer):
    return list(filter(lambda a : a['layer'] == layer, movements))

if __name__ == "__main__":
    urdf_file = "unnamed.urdf"
    target_orientation = [0, 0, -1]
    start_position = [200, -150, 300]

    movements = parse_gcode_movements("AA8_test1.gcode")
    target_positions = get_layer(movements, layer_number(movements))

    for i in range(len(target_positions) - 1):
        #print(target_positions[0:i + 1])
        interface(start_position, target_positions[0:i + 1], target_orientation, "./unnamed.urdf", False)