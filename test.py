import math

import numpy as np


class AsciiRenderer:
    def __init__(
            self,
            canvas_res: tuple
    ) -> None:
        self.canvas_plane_x = canvas_res[0]
        self.canvas_plane_y = canvas_res[1] 

        self.asciis = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

    def _luminance_to_ascii(
            self,
            luminance: float
    ) -> str:
        idx = int(luminance * (len(self.asciis) - 1))
        return self.asciis[idx]

    def render(
            self,
            points: dict
    ) -> None:
        for y in range(self.canvas_plane_y):
            row = []
            for x in range(self.canvas_plane_x):
                luminance, _, _ = points.get((x, y), (0.0, 0.0, 0.0))
                row.append(self._luminance_to_ascii(luminance))
            print("".join(row))


class Camera:
    def __init__(
            self,
            camera_pos: np.ndarray,
            focal_length: float,
            canvas_middle: np.ndarray,
            pixel_size_x: float,
            pixel_size_y: float
    ) -> None:
        # Define world coordinate system
        self.world_center = np.array([0.0, 0.0, 0.0])
        world_z_axis = np.array([0.0, 0.0, 1.0])

        self.world_middle = np.array([0.5, 0.5, 0.5])

        # Define camera coordinate system
        self.camera_center = camera_pos

        self.camera_z_axis = self.world_middle - self.camera_center
        self.camera_z_axis /= np.linalg.norm(self.camera_z_axis)

        self.camera_y_axis = np.cross(self.camera_z_axis, world_z_axis)
        self.camera_y_axis /= np.linalg.norm(self.camera_y_axis)

        self.camera_x_axis = np.cross(self.camera_y_axis, self.camera_z_axis)

        self.focal_length = focal_length

        # Define canvas parameter
        self.canvas_middle = canvas_middle
        self.pixel_size_x = pixel_size_x
        self.pixel_size_y = pixel_size_y

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

    def world_to_camera(
            self,
            points_world: list
    ) -> tuple:
        points_world_homogeneous = self.cartesian_to_homogeneous(points_world)
        
        points_camera_homogeneous = []
        points_z_values = []
        for point_world_homogeneous in points_world_homogeneous:
            point_camera_homogeneous = self.int_matrix @ self.ext_matrix @ point_world_homogeneous
            points_camera_homogeneous.append(point_camera_homogeneous)
            points_z_values.append(point_camera_homogeneous[-1])

        points_camera = self.homogeneous_to_cartesian(points_camera_homogeneous)

        return points_camera, points_z_values


class CanvasHandler:
    def __init__(
            self,
            canvas_res: tuple,
            light_pos: np.ndarray,
            camera_pos: np.ndarray,
            focal_length: float
    ) -> None:
        # Define canvas
        self.canvas_plane_x = canvas_res[0]
        self.canvas_plane_y = canvas_res[1]
        self.canvas_middle = np.array([math.floor(self.canvas_plane_x / 2), math.floor(self.canvas_plane_y / 2)], dtype=int)

        self.pixel_size_x = 1.0 / (self.canvas_plane_x - 1)
        self.pixel_size_y = 1.0 / (self.canvas_plane_y - 1)

        self.canvas_z_buffer = np.array(canvas_res)
        self.canvas = {}

        # Camera
        self.camera_center = camera_pos
        self.cam = Camera(camera_pos, focal_length, self.canvas_middle, self.pixel_size_x, self.pixel_size_y)

        # Define light source
        light_center = light_pos
        self.light_path = light_center - self.cam.world_middle
        self.light_path /= np.linalg.norm(self.light_path)

    def process_objects(
            self,
            objects: list
    ) -> None:
        for object in objects:
            self.process_polygons(object)

    def process_polygons(
            self,
            polygons: list
    ) -> None:
        object_center = np.mean(np.vstack(polygons), axis=0)

        for polygon in polygons:
            normal = self.compute_normal(polygon, object_center)
            
            luminance = np.dot(normal, self.light_path)
            luminance = np.clip(luminance, 0.0, 1.0)

            polygon_center = np.mean(polygon, axis=0)
            closeness = np.linalg.norm(self.camera_center - polygon_center)

            vertices, z_values = self.cam.world_to_camera(polygon)
            points_camera = self.points_in_polygon(vertices)
            points_pixel = self.cartesian_to_pixel(points_camera)

            for point_pixel in points_pixel:
                coords = tuple(int(p) for p in point_pixel)
                min_z_value = np.min(z_values)

                if coords in self.canvas.keys():
                    old_luminance = self.canvas[coords][0]
                    old_min_z_value = self.canvas[coords][1]
                    old_closeness = self.canvas[coords][2]

                    if old_min_z_value > min_z_value:
                        self.canvas[coords] = [luminance, min_z_value, closeness]
                    elif old_min_z_value == min_z_value:
                        if old_closeness > closeness:
                            self.canvas[coords] = [luminance, min_z_value, closeness]
                else:
                    self.canvas[coords] = [luminance, min_z_value, closeness]

    def compute_normal(
            self,
            polygon: list,
            object_center: np.ndarray
    ) -> np.ndarray:
        polygon_center = np.mean(polygon, axis=0)
        center_line = polygon_center - object_center
        center_line /= np.linalg.norm(center_line)

        normal = np.cross(polygon[1] - polygon[0], polygon[2] - polygon[0])
        normal /= np.linalg.norm(normal)

        if np.dot(center_line, normal) < 0:
            normal = -normal

        return normal

    def points_in_polygon(self, polygon, grid_spacing=1.0):
        polygon = np.asarray(polygon)
        if not np.allclose(polygon[0], polygon[-1]):
            polygon = np.vstack([polygon, polygon[0]])  # ensure closed

        # bounding box
        min_x, min_y = polygon.min(axis=0)
        max_x, max_y = polygon.max(axis=0)

        # create grid
        xs = np.arange(min_x, max_x + grid_spacing, grid_spacing)
        ys = np.arange(min_y, max_y + grid_spacing, grid_spacing)
        xx, yy = np.meshgrid(xs, ys)
        grid_points = np.column_stack((xx.ravel(), yy.ravel()))

        # Ray casting algorithm (NumPy vectorized)
        x = grid_points[:, 0][:, None]
        y = grid_points[:, 1][:, None]
        x0, y0 = polygon[:-1, 0], polygon[:-1, 1]
        x1, y1 = polygon[1:, 0], polygon[1:, 1]

        cond1 = ((y0 <= y) & (y < y1)) | ((y1 <= y) & (y < y0))
        cond2 = x < (x1 - x0) * (y - y0) / (y1 - y0 + 1e-12) + x0
        crossings = np.sum(cond1 & cond2, axis=1)
        inside = crossings % 2 == 1

        return grid_points[inside]

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


canvas_resolution = (80, 40)
light_position = np.array([1.0, 0.4, 0.8])
camera_position = np.array([1.5, -2.0, 1.0])
focal_length = 2.0

handler = CanvasHandler(canvas_resolution, light_position, camera_position, focal_length)
renderer = AsciiRenderer(canvas_resolution)

# Define vertices of a cube floating in the middle of a unit room
cube_verts = np.array([
    # x     y     z
    [0.25, 0.25, 0.25], # 0: bottom front left corner
    [0.75, 0.25, 0.25], # 1: bottom front right corner
    [0.75, 0.75, 0.25], # 2: bottom back right corner
    [0.25, 0.75, 0.25], # 3: bottom back left corner
    [0.25, 0.25, 0.75], # 4: top front left corner
    [0.75, 0.25, 0.75], # 5: top front right corner
    [0.75, 0.75, 0.75], # 6: top back right corner
    [0.25, 0.75, 0.75]  # 7: top back left corner
])

# # Define faces of the cube
cube_faces = np.array([
    [0, 1, 2, 3], # 0: bottom
    [4, 5, 6, 7], # 1: top
    [0, 1, 5, 4], # 2: front
    [1, 2, 6, 5], # 3: right
    [2, 3, 7, 6], # 4: back
    [3, 0, 4, 7]  # 5: left
])

cube_front_verts = cube_verts[cube_faces[2]]

sideways_rectangle_verts = np.array([
    [0.5, 0.5, 0.25],
    [0.75, 0.5, 0.5],
    [0.5, 0.5, 0.75],
    [0.25, 0.5, 0.5]
])

weird_shape_verts = np.array([
    [0.1, 0.5, 0.1],
    [0.5, 0.5, 0.4],
    [0.9, 0.5, 0.1],
    [0.9, 0.5, 0.9],
    [0.3, 0.5, 0.8],
    [0.5, 0.5, 0.9],
    [0.1, 0.5, 0.9],
    [0.1, 0.5, 0.7],
    [0.4, 0.5, 0.4]
])

cube = []
for face in cube_faces:
    face_verts = cube_verts[face]
    cube.append(face_verts)

cubes = [cube]

handler.process_objects(cubes)
points = handler.canvas
renderer.render(points)
