import math

import numpy as np


class AsciiRenderer:
    def __init__(
            self,
            canvas_res: tuple,
            camera_pos: np.ndarray
    ) -> None:
        # Define world coordinate system
        self.world_center = np.array([0.0, 0.0, 0.0])
        world_x_axis = np.array([1.0, 0.0, 0.0])
        world_y_axis = np.array([0.0, 1.0, 0.0])
        world_z_axis = np.array([0.0, 0.0, 1.0])

        world_middle = np.array([0.5, 0.5, 0.5])

        # Define camera coordinate system
        self.camera_center = camera_pos

        self.camera_z_axis = world_middle - self.camera_center
        self.camera_z_axis /= np.linalg.norm(self.camera_z_axis)

        self.camera_y_axis = np.cross(self.camera_z_axis, world_z_axis)
        self.camera_y_axis /= np.linalg.norm(self.camera_y_axis)

        self.camera_x_axis = np.cross(self.camera_y_axis, self.camera_z_axis)

        self.focal_length = 1.0

        camer_plane_middle = np.array([0.0, 0.0])
        camera_plane_x = 1.0
        camera_plane_y = 1.0

        # Define pixel canvas
        self.canvas_plane_x = canvas_resolution[0]
        self.canvas_plane_y = canvas_resolution[1]
        self.canvas_middle = np.array([math.floor(self.canvas_plane_x / 2), math.floor(self.canvas_plane_y / 2)], dtype=int)

        self.pixel_size_x = camera_plane_x / (self.canvas_plane_x - 1)
        self.pixel_size_y = camera_plane_y / (self.canvas_plane_y - 1)

        # Define light source
        light_center = np.array([1.0, 1.0, 1.0])
        light_path = light_center - world_middle
        light_path /= np.linalg.norm(light_path)

        # Define projection matrices
        self.int_matrix, self.ext_matrix = self.compute_projection_matrices()

    def compute_projection_matrices(
            self
    ) -> tuple:
        # Translation vector
        translation_vector = self.world_center - self.camera_center

        # Rotation matrix
        rotation_matrix = np.vstack([self.camera_x_axis, self.camera_y_axis, self.camera_z_axis])

        # Intrinsic matrix
        intrinsic_matrix = np.zeros((3, 3))
        intrinsic_matrix[0, 0] = self.focal_length / self.pixel_size_x
        intrinsic_matrix[1, 1] = self.focal_length / self.pixel_size_y
        intrinsic_matrix[2, 2] = 1.0

        intrinsic_matrix[0, 2] = self.canvas_middle[0]
        intrinsic_matrix[1, 2] = self.canvas_middle[1]

        # Extrinsic matrix
        extrinsic_matrix = np.zeros((3, 4))
        extrinsic_matrix[:, :3] = rotation_matrix
        extrinsic_matrix[0, 3] = rotation_matrix[0] @ translation_vector
        extrinsic_matrix[1, 3] = rotation_matrix[1] @ translation_vector
        extrinsic_matrix[2, 3] = rotation_matrix[2] @ translation_vector

        return intrinsic_matrix, extrinsic_matrix

    def cartesian_to_homogeneous(
            self,
            points_cartesian: list
    ) -> list:
        dim = len(points_cartesian[0])

        points_homogeneous = []
        for point_cartesian in points_cartesian:
            point_homogeneous = np.ones((dim + 1,))
            point_homogeneous[0:dim] = point_cartesian
            points_homogeneous.append(point_homogeneous)

        return points_homogeneous

    def homogeneous_to_cartesian(
            self,
            points_homogeneous: list
    ) -> list:
        dim = len(points_homogeneous[0])

        points_cartesian = []
        for point_homogeneous in points_homogeneous:
            point_cartesian = np.ones((dim - 1,))
            for idx in range(dim - 1):
                point_cartesian[idx] = point_homogeneous[idx] / point_homogeneous[-1]
            points_cartesian.append(point_cartesian)
        
        return points_cartesian

    def cartesian_to_pixel(
            self,
            points_cartesian: list
    ) -> list:
        points_pixel = []
        for point_cartesian in points_cartesian:
            point_cartesian[1] = self.canvas_plane_y - point_cartesian[1]
            point_pixel = np.floor(point_cartesian)
            points_pixel.append(point_pixel)

        return points_pixel

    def world_to_camera(
            self,
            points_world: list
    ) -> list:
        points_world_homogeneous = self.cartesian_to_homogeneous(points_world)
        
        points_camera_homogeneous = []
        for point_world_homogeneous in points_world_homogeneous:
            point_camera_homogeneous = self.int_matrix @ self.ext_matrix @ point_world_homogeneous
            points_camera_homogeneous.append(point_camera_homogeneous)

        points_camera = self.homogeneous_to_cartesian(points_camera_homogeneous)

        return points_camera
    
    def render(
            self,
            points_world: list
    ) -> None:
        points_camera = self.world_to_camera(points_world)
        points_canvas = self.cartesian_to_pixel(points_camera)

        # Draw canvas
        for y in range(self.canvas_plane_y + 2):
            for x in range(self.canvas_plane_x + 2):
                if x == 0 or x == (self.canvas_plane_x + 1) or y == 0 or y == (self.canvas_plane_y + 1):
                    print("%", end="" if x != self.canvas_plane_x + 1 else "\n")
                elif np.any(np.all(np.array([x - 1, y - 1]) == points_canvas, axis=1)):
                    print("#", end="" if x != self.canvas_plane_x + 1 else "\n")
                else:
                    print(" ", end="" if x != self.canvas_plane_x + 1 else "\n")


canvas_resolution = (40, 20)
camera_position = np.array([0.5, -1.0, 0.5])
renderer = AsciiRenderer(canvas_resolution, camera_position)

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

# Define point to transform
point_world_01 = np.array([0.25, 0.5, 0.25])
point_world_02 = np.array([0.75, 0.5, 0.25])
point_world_03 = np.array([0.75, 0.5, 0.75])
point_world_04 = np.array([0.25, 0.5, 0.75])

world_points = [point_world_01, point_world_02, point_world_03, point_world_04]

renderer.render(world_points)
