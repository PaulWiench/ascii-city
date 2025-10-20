import numpy as np


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

        self.camera_x_axis = np.cross(self.camera_z_axis, world_z_axis)
        self.camera_x_axis /= np.linalg.norm(self.camera_x_axis)

        self.camera_y_axis = np.cross(self.camera_x_axis, self.camera_z_axis)

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
