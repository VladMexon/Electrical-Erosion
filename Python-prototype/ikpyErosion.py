import ikpy.chain
import numpy as np
import math
import os

lastImageNum = 0

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

def generate_config(target_positions, target_orientation_vector, radius, depth, urdf_file, os_id,imgs = False):
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
    config += "radius = " + str(radius) + ";"
    config += "depth = " + str(depth) + ";"
    f = open("config.scad", "w")
    f.write(config)
    f.close()
    if(imgs):
        generate_images(os_id)

def generate_images(os_id):
    global lastImageNum
    if os_id == "nt":  # Windows
        os.system(f"\"c:\Program Files\OpenSCAD\openscad.exe\" -o imgs/output{lastImageNum}.png openSCADModel2.scad --imgsize=1920,1080")
    elif os_id == "posix":  # Unix-like (Linux, macOS)
        os.system(f"openscad -o imgs/output{lastImageNum}.png openSCADModel2.scad --imgsize=1920,1080")
    lastImageNum += 1

if __name__ == "__main__":
    urdf_file = "unnamed.urdf"
    target_orientation_vector = [0, 0, -1]
    target_positions = [[200,-150,200]] 
    generate_config(target_positions, target_orientation_vector, "unnamed.urdf", False)
        



   
    
    
    