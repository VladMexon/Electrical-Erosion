import ikpy.chain
import numpy as np
import math
import os

def compute_joint_positions_and_orientations(urdf_file, target_position, target_orientation_vector):
    my_chain = ikpy.chain.Chain.from_urdf_file(urdf_file, active_links_mask=[False, True, True, True, True, True, True, True, False])
    inverse_kinematics = my_chain.inverse_kinematics(target_position=target_position, target_orientation=target_orientation_vector, orientation_mode='Z')
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
            position[2] += step
        list.append(position)
    

def generate_config(target_positions, target_orientation_vector, imgs = False):
    joint_positions, joint_orientations = compute_joint_positions_and_orientations(urdf_file, target_positions[len(target_positions) - 1], target_orientation_vector)
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
    f.write(config)
    f.close()
    if(imgs):
        generate_images()

def generate_images():
    global lastImageNum
    os.system(f"\"c:\Program Files\OpenSCAD\openscad.exe\" -o imgs/output{lastImageNum}.png openSCADModel2.scad");
    lastImageNum += 1


if __name__ == "__main__":
    urdf_file = "unnamed.urdf"
    target_orientation_vector = [0, 0, -1]
    target_positions = [[100,-30,40]] 
    generate_config(target_positions, target_orientation_vector, False)
    # lastImageNum = 1
    # urdf_file = "../3DModel/urdf/unnamed.urdf"

    # step = 0.02
    # stepZ= 0.05
    # target_positions = [[3.05,-0.4,3.2]] #start point
    # for i in range(math.floor(0.1/step)):
    #     generate_config(target_positions, True)
    #     emulate_movement('z', -stepZ, 1, target_positions)
    #     generate_config(target_positions, True)
    #     emulate_movement('z', stepZ, 1, target_positions)
    #     generate_config(target_positions, True)
    #     emulate_movement('y', step, 1, target_positions)
    # target_positions = [[3.05,-0.4,3.15]] #start point
    # for i in range(3):
    #     emulate_movement('y', step, math.floor(0.8/step) - i * 2, target_positions)
    #     emulate_movement('x', step, math.floor(0.1/step) - i * 2, target_positions)
    #     emulate_movement('y', -step, math.floor(0.8/step) - i * 2, target_positions)
    #     emulate_movement('x', -step, math.floor(0.1/step) - i * 2, target_positions)
    #     emulate_movement('x', step, 1, target_positions)
    #     emulate_movement('y', step, 1, target_positions)
    #     generate_config(target_positions, True)
        



   
    
    
    