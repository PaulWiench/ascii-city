import numpy as np


# Define vertices of a cube floating in the middle of a unit room
# cube_verts = np.array([
#     # x     y     z
#     [0.25, 0.25, 0.25], # 0: bottom front-left corner
#     [0.75, 0.25, 0.25], # 1: bottom front-right corner
#     [0.75, 0.75, 0.25], # 2: bottom back-right corner
#     [0.25, 0.75, 0.25], # 3: bottom back-left corner
#     [0.25, 0.25, 0.75], # 4: top front-left corner
#     [0.75, 0.25, 0.75], # 5: top front-right corner
#     [0.75, 0.75, 0.75], # 6: top back-right corner
#     [0.25, 0.75, 0.75]  # 7: top back-left corner
# ])

# # Define faces of the cube
# cube_faces = np.array([
#     [0, 1, 2, 3], # 0: bottom
#     [4, 5, 6, 7], # 1: top
#     [0, 1, 4, 5], # 2: front
#     [1, 2, 5, 6], # 3: right
#     [2, 3, 6, 7], # 4: back
#     [3, 0, 7, 4]  # 5: left
# ])

# z  y
# | /
# |/__ x
# Define world coordinate system
world_center = np.array([0.0, 0.0, 0.0])
world_x_axis = np.array([1.0, 0.0, 0.0])
world_y_axis = np.array([0.0, 1.0, 0.0])
world_z_axis = np.array([0.0, 0.0, 1.0])

world_middle = np.array([0.5, 0.5, 0.5])

# x  z
# | /
# |/__ y
# Define camera coordinate system
camera_center = np.array([0.5, -1.0, 0.5])

camera_z_axis = world_middle - camera_center
camera_z_axis /= np.linalg.norm(camera_z_axis)

camera_y_axis = np.cross(camera_z_axis, world_z_axis)
camera_y_axis /= np.linalg.norm(camera_y_axis)

camera_x_axis = np.cross(camera_y_axis, camera_z_axis)

focal_length = 1.0

camer_plane_middle = np.array([0.0, 0.0])
camera_plane_x = 1.0
camera_plane_y = 1.0

# Define pixel canvas
canvas_plane_x = 40
canvas_plane_y = 20
canvas_middle = np.array([20, 10], dtype=int)

pixel_size_x = camera_plane_x / (canvas_plane_x - 1)
pixel_size_y = camera_plane_y / (canvas_plane_y - 1)

# Define light source
light_center = np.array([1.0, 1.0, 1.0])
light_path = light_center - world_middle
light_path /= np.linalg.norm(light_path)

# Translation vector
translation_vector = world_center - camera_center

# Rotation matrix
rotation_matrix = np.vstack([camera_x_axis, camera_y_axis, camera_z_axis])

# Intrinsic matrix
int_matrix = np.zeros((3, 3))
int_matrix[0, 0] = focal_length / pixel_size_x
int_matrix[1, 1] = focal_length / pixel_size_y
int_matrix[2, 2] = 1.0

int_matrix[0, 2] = canvas_middle[0]
int_matrix[1, 2] = canvas_middle[1]

# Extrinsic matrix
ext_matrix = np.zeros((3, 4))
ext_matrix[:, :3] = rotation_matrix
ext_matrix[0, 3] = rotation_matrix[0] @ translation_vector
ext_matrix[1, 3] = rotation_matrix[1] @ translation_vector
ext_matrix[2, 3] = rotation_matrix[2] @ translation_vector

# Define point to transform
point_world_01 = np.array([0.25, 0.5, 0.25])
point_world_02 = np.array([0.75, 0.5, 0.25])
point_world_03 = np.array([0.75, 0.5, 0.75])
point_world_04 = np.array([0.25, 0.5, 0.75])

world_points = [point_world_01, point_world_02, point_world_03, point_world_04]

def to_homogeneous(points):
    dim = len(points[0])

    points_homogeneous = []
    for point in points:
        point_homogeneous = np.ones((dim + 1,))
        point_homogeneous[0:dim] = point
        points_homogeneous.append(point_homogeneous)

    return points_homogeneous

def to_pixel(points, canvas_plane_y):
    dim = len(points[0])

    points_pixel = []
    for point in points:
        point_pixel = np.ones((2,))
        point_pixel[0] = point[0] / point[2]
        point_pixel[1] = point[1] / point[2]

        point_pixel[1] = canvas_plane_y - point_pixel[1]
        point_pixel = np.floor(point_pixel)
        points_pixel.append(point_pixel)

    return points_pixel


def world_to_camera(points_world, canvas_plane_y):
    points_world_homogeneous = to_homogeneous(points_world)
    
    points_camera_homogeneous = []
    for point in points_world_homogeneous:
        point_camera_homogeneous = int_matrix @ ext_matrix @ point
        points_camera_homogeneous.append(point_camera_homogeneous)

    points_pixel = to_pixel(points_camera_homogeneous, canvas_plane_y)

    return points_pixel


canvas_points = world_to_camera(world_points, canvas_plane_y)

# Draw canvas
for y in range(canvas_plane_y + 2):
    for x in range(canvas_plane_x + 2):
        if x == 0 or x == (canvas_plane_x + 1) or y == 0 or y == (canvas_plane_y + 1):
            print("%", end="" if x != canvas_plane_x + 1 else "\n")
        elif np.any(np.all(np.array([x - 1, y - 1]) == canvas_points, axis=1)):
            print("#", end="" if x != canvas_plane_x + 1 else "\n")
        else:
            print(" ", end="" if x != canvas_plane_x + 1 else "\n")
