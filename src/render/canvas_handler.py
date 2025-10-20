import math

import numpy as np

from src.render.camera import Camera


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
            points_cartesian: np.ndarray
    ) -> list:
        points_pixel = []
        for point_cartesian in points_cartesian:
            point_cartesian[1] = self.canvas_plane_y - point_cartesian[1]
            point_pixel = np.floor(point_cartesian)
            points_pixel.append(point_pixel)

        return points_pixel
