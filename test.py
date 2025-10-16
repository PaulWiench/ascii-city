import numpy as np

# # === CONFIGURATION ===
# res_x, res_y = 80, 40          # ASCII resolution
# subdiv = 6                     # samples per face edge
# f = 80                         # focal length
# ascii_chars = np.array(list(" .:-=+*#%@"))  # brightness ramp

# # === CAMERA & LIGHT SETUP ===
# L = np.array([0.3, 0.4, 0.9], dtype=float)
# L /= np.linalg.norm(L)

# C = np.array([25., -25., 20.])  # camera position
# look_at = np.array([5., 5., 5.])
# up = np.array([0., 0., 1.])

# # --- Build camera basis (right, up, forward) ---
# zaxis = look_at - C
# zaxis /= np.linalg.norm(zaxis)
# xaxis = np.cross(up, zaxis); xaxis /= np.linalg.norm(xaxis)
# yaxis = np.cross(zaxis, xaxis)
# R = np.vstack([xaxis, yaxis, zaxis])  # rotation matrix (3x3)

# # === HELPER: face normal ===
# def face_normal(v):
#     n = np.cross(v[1] - v[0], v[2] - v[0])
#     return n / np.linalg.norm(n)

# # === SUBDIVIDE FACES FOR DENSER SAMPLING ===
# samples = []
# normals = []
# for f_idx in faces:
#     v = verts[f_idx]
#     n = face_normal(v)
#     for i in np.linspace(0, 1, subdiv):
#         for j in np.linspace(0, 1, subdiv):
#             p = (
#                 v[0] * (1 - i) * (1 - j) +
#                 v[1] * i * (1 - j) +
#                 v[3] * (1 - i) * j +
#                 v[2] * i * j
#             )
#             samples.append(p)
#             normals.append(n)
# samples = np.array(samples)
# normals = np.array(normals)

# # === LIGHTING (Lambertian) ===
# I = np.clip(np.dot(normals, L), 0, 1)

# # === PROJECT TO CAMERA PLANE ===
# pts_cam = (R @ (samples - C).T).T
# x_proj = f * (pts_cam[:, 0] / -pts_cam[:, 2])
# y_proj = f * (pts_cam[:, 1] / -pts_cam[:, 2])

# # === NORMALIZE TO ASCII GRID ===
# x_min, x_max = x_proj.min(), x_proj.max()
# y_min, y_max = y_proj.min(), y_proj.max()
# x_scale = res_x / (x_max - x_min)
# y_scale = res_y / (y_max - y_min)
# scale = min(x_scale, y_scale)
# px = ((x_proj - x_min) * scale).astype(int)
# py = ((y_proj - y_min) * scale).astype(int)

# # === INITIALIZE CANVAS ===
# canvas = np.full((res_y, res_x), " ", dtype="<U1")

# # === DRAW POINTS (with backface culling) ===
# for i, (ix, iy) in enumerate(zip(px, py)):
#     if pts_cam[i, 2] >= 0:  # behind camera
#         continue
#     # Backface culling (skip faces pointing away)
#     if np.dot(normals[i], -zaxis) <= 0:
#         continue
#     if 0 <= ix < res_x and 0 <= iy < res_y:
#         c = ascii_chars[int(I[i] * (len(ascii_chars) - 1))]
#         canvas[res_y - 1 - iy, ix] = c

# === DISPLAY ===
# x = np.zeros((8,))
# x2 = np.array([0, 1, 1, 1, 1, 1, 1, 0])

# # canvas is 16x13
# canvas = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

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
point_world = np.array([0.5, 0.5, 0.5])

point_world_homogeneous = np.ones((4,))
point_world_homogeneous[0:3] = point_world

# World to camera projection
point_camera_homogeneous = int_matrix @ ext_matrix @ point_world_homogeneous

point_camera = np.ones((2,))
point_camera[0] = point_camera_homogeneous[0] / point_camera_homogeneous[2]
point_camera[1] = point_camera_homogeneous[1] / point_camera_homogeneous[2]

point_camera[1] = canvas_plane_y - point_camera[1]
point_camera = np.floor(point_camera)

canvas_points = []
canvas_points.append(point_camera)

# Draw canvas
for y in range(canvas_plane_y + 2):
    for x in range(canvas_plane_x + 2):
        if x == 0 or x == (canvas_plane_x + 1) or y == 0 or y == (canvas_plane_y + 1):
            print("%", end="" if x != canvas_plane_x + 1 else "\n")
        elif np.any(np.all(np.array([x - 1, y - 1]) == canvas_points, axis=1)):
            print("#", end="" if x != canvas_plane_x + 1 else "\n")
        else:
            print(" ", end="" if x != canvas_plane_x + 1 else "\n")


# focal_length = 2

# def compute_normal(verts):
#     normal = np.cross(verts[1] - verts[0], verts[2] - verts[0])
#     return normal / np.linalg.norm(normal)

# # for face in cube_faces:
# face = cube_faces[2]
# face_verts = cube_verts[face]
# face_normal = compute_normal(face_verts)

# cos_phi = np.dot(light_vec, face_normal)

# print(face_verts)
# face_verts_camera = (rotation_matrix @ (face_verts - translation_vec).T).T
# cam_x = focal_length * (face_verts_camera[:, 0] / -face_verts_camera[:, 2])
# cam_y = focal_length * (face_verts_camera[:, 1] / -face_verts_camera[:, 2])
# print(cam_x[0], cam_y[0])
    # break

# print("")

# projection_matrix = np.zeros((4, 4))
# projection_matrix[0:3, 0:3] = rotation_matrix
# projection_matrix[0:3, -1] = translation_vec
# projection_matrix[-1, -1] = 1.0

# print(projection_matrix)

# print("")

# world = np.ones((4,4))
# world[:, 0:3] = face_verts
# world = world[0]
# print(world)

# print("")

# test = projection_matrix @ world
# print(test)

# intrinsic_matrix = np.zeros((3,4))
# intrinsic_matrix[0, 0] = focal_length
# intrinsic_matrix[1, 1] = focal_length
# intrinsic_matrix[2, 2] = 1.0

# print("")
# print(intrinsic_matrix)
# print("")

# test2 = intrinsic_matrix @ test
# xx = test2[0] / test2[2]
# yy = test2[1] / test2[2]
# print(xx, yy)

# ascii_canvas_resolution = (100, 100)


# # === NORMALIZE TO ASCII GRID ===
# x_min, x_max = x_proj.min(), x_proj.max()
# y_min, y_max = y_proj.min(), y_proj.max()
# x_scale = res_x / (x_max - x_min)
# y_scale = res_y / (y_max - y_min)
# scale = min(x_scale, y_scale)
# px = ((x_proj - x_min) * scale).astype(int)
# py = ((y_proj - y_min) * scale).astype(int)

# for row in canvas:
#     for idx, char in enumerate(row):
#         if char == 0:
#             print(" ", end="" if idx != len(row) - 1 else "\n")
#         elif char == 1:
#             print("%", end="" if idx != len(row) - 1 else "\n")
#         elif char == 2:
#             print("=", end="" if idx != len(row) - 1 else "\n")
#         else:
#             print(".", end="" if idx != len(row) - 1 else "\n")