import ikpy.chain
import numpy as np

my_chain = ikpy.chain.Chain.from_urdf_file("3DModel/urdf/unnamed.urdf")

target_position = [ 4, 4, 5]
print("The angles of each joints are : ", my_chain.inverse_kinematics(target_position))