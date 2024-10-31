import ikpy.chain
import numpy as np
import math

def compute_joint_positions_and_orientations(urdf_file, target_position):
    my_chain = ikpy.chain.Chain.from_urdf_file(urdf_file)
    inverse_kinematics = my_chain.inverse_kinematics(target_position)
    transformations = my_chain.forward_kinematics(inverse_kinematics, full_kinematics=True)
    
    joint_positions = []
    joint_orientations = []
    
    for i, transformation_matrix in enumerate(transformations):
        transformation_matrix = np.array(transformation_matrix).reshape((4, 4))
        position = transformation_matrix[:3, 3]
        orientation_matrix = transformation_matrix[:3, :3]
        
        orientation_euler = rotation_matrix_to_euler_angles(orientation_matrix)
        
        joint_positions.append(position)
        joint_orientations.append(orientation_euler)
        
        #print(f"Joint {i}: Position = {position}, Orientation (Euler angles) = {orientation_euler}")
    
    return joint_positions, joint_orientations

def rotation_matrix_to_euler_angles(R):
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    
    singular = sy < 1e-6
    
    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0
    
    x, y, z = np.array([x, y, z]) * 180.0 / math.pi
    return np.array([x, y, z])

def emulate_movement(direction, step, count, list):
    for i in range(count):
        position = list[len(list) - 1].copy()
        if(direction == 'x'):
            position[0] += step
        elif(direction == 'y'):
            position[1] += step
        elif(direction == 'z'):
            position[3] += step
        list.append(position)
    return list

def generate_config(target_positions):
    joint_positions, joint_orientations = compute_joint_positions_and_orientations(urdf_file, target_positions[len(target_positions) - 1])
    config = ""
    for i in range(len(joint_positions)):
        config += f"pos{i} = [{joint_positions[i][0]}, {joint_positions[i][1]}, {joint_positions[i][2]}];"
    for i in range(len(joint_orientations)):
        config += f"rot{i} = [{joint_orientations[i][0]}, {joint_orientations[i][1]}, {joint_orientations[i][2]}];"
    config += "cuts = ["
    for i in range(len(target_positions)):
        config += f"[{target_positions[i][0]}, {target_positions[i][1]}, {target_positions[i][2]}]"
        if i < len(target_positions) - 1:
            config += ","
    config += "];"
    f = open("config.scad", "w")
    f.write(config);
    f.close();

urdf_file = "3DModel/urdf/unnamed.urdf"
target_positions = [[3.1,-0.2,3.3]] #start point
emulate_movement('y', 0.04, 10, target_positions)
emulate_movement('x', 0.04, 5, target_positions)
emulate_movement('y', -0.04, 10, target_positions)
emulate_movement('x', -0.04, 4, target_positions)
generate_config(target_positions)