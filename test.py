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
x = np.zeros((8,))
x2 = np.array([0, 1, 1, 1, 1, 1, 1, 0])

# canvas is 16x13
canvas = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Define vertices of a cube floating in the middle of a unit room
cube_verts = np.array([
    # x     y     z
    [0.25, 0.25, 0.25], # 0: bottom front-left corner
    [0.75, 0.25, 0.25], # 1: bottom front-right corner
    [0.75, 0.75, 0.25], # 2: bottom back-right corner
    [0.25, 0.75, 0.25], # 3: bottom back-left corner
    [0.25, 0.25, 0.75], # 4: top front-left corner
    [0.75, 0.25, 0.75], # 5: top front-right corner
    [0.75, 0.75, 0.75], # 6: top back-right corner
    [0.25, 0.75, 0.75]  # 7: top back-left corner
])

# Define faces of the cube
cube_faces = np.array([
    [0, 1, 2, 3], # 0: bottom
    [4, 5, 6, 7], # 1: top
    [0, 1, 4, 5], # 2: front
    [1, 2, 5, 6], # 3: right
    [2, 3, 6, 7], # 4: back
    [3, 0, 7, 4]  # 5: left
])

cube_center = np.array([0.5, 0.5, 0.5])
camera_center = np.array([1.0, 1.0, 1.0])
light_center = np.array([1.0, 1.0, 1.0])

def compute_normal(verts):
    normal = np.cross(verts[1] - verts[0], verts[2] - verts[0])
    return normal / np.linalg.norm(normal)

for face in cube_faces:
    face_verts = cube_verts[face]
    face_normal = compute_normal(face_verts)
    print(face_normal)

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