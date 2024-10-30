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
        
        # Конвертируем матрицу вращения в углы Эйлера
        orientation_euler = rotation_matrix_to_euler_angles(orientation_matrix)
        
        joint_positions.append(position)
        joint_orientations.append(orientation_euler)
        
        print(f"Joint {i}: Position = {position}, Orientation (Euler angles) = {orientation_euler}")
    
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

urdf_file = "3DModel/urdf/unnamed.urdf"
target_position = [2, -1, 2]
compute_joint_positions_and_orientations(urdf_file, target_position)