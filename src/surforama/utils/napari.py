from typing import List, Tuple, Union

import numpy as np
from napari.layers import Points

from surforama.constants import (
    NAPARI_NORMAL_0,
    NAPARI_NORMAL_1,
    NAPARI_NORMAL_2,
    NAPARI_UP_0,
    NAPARI_UP_1,
    NAPARI_UP_2,
    ROTATION,
)
from surforama.utils.geometry import rotate_around_vector


def vectors_data_from_points_features(
    points_layer: Points,
) -> Tuple[np.ndarray, np.ndarray]:
    """Get the vectors data for normal and up vectors from an oriented points layer.

    Parameters
    ----------
    points_layer : Points
        The oriented points layer from which to get the vectors data.

    Returns
    -------
    normals_data : np.ndarray
        The Vectors layer data for the normal vectors
    up_data : np.ndarray
        The Vectors layer data for the up vectors
    """

    # get the point data
    point_coordinates = points_layer.data

    feature_table = points_layer.features

    # get the vectors
    normal_vectors = feature_table[
        [NAPARI_NORMAL_0, NAPARI_NORMAL_1, NAPARI_NORMAL_2]
    ].to_numpy()
    up_vectors = feature_table[
        [NAPARI_UP_0, NAPARI_UP_1, NAPARI_UP_2]
    ].to_numpy()
    rotations = feature_table[ROTATION].to_numpy()
    rotated_up_vectors = rotate_around_vector(
        rotate_around=normal_vectors, to_rotate=up_vectors, angle=rotations
    )

    # make the vector data
    n_points = point_coordinates.shape[0]
    normal_vector_data = np.zeros((n_points, 2, 3))
    normal_vector_data[:, 0, :] = point_coordinates
    normal_vector_data[:, 1, :] = normal_vectors

    up_vector_data = np.zeros((n_points, 2, 3))
    up_vector_data[:, 0, :] = point_coordinates
    up_vector_data[:, 1, :] = rotated_up_vectors

    return normal_vector_data, up_vector_data


def get_vectors_data_from_points_layer(
    points_layer: Points, point_index: Union[int, List[int]]
) -> Tuple[np.ndarray, np.ndarray, Union[float, np.ndarray]]:
    feature_table = points_layer.features

    # get the normal vector
    normal_vectors = feature_table[
        [NAPARI_NORMAL_0, NAPARI_NORMAL_1, NAPARI_NORMAL_2]
    ].to_numpy()
    selected_normal_vector = normal_vectors[point_index]

    # get the up vector
    up_vectors = feature_table[
        [NAPARI_UP_0, NAPARI_UP_1, NAPARI_UP_2]
    ].to_numpy()
    selected_up_vector = up_vectors[point_index]

    # get the rotation
    rotations = feature_table[ROTATION].to_numpy()
    selected_rotation = rotations[point_index]

    return selected_normal_vector, selected_up_vector, selected_rotation


def update_vectors_data_on_points_layer(
    points_layer: Points,
    point_index: Union[int, List[int]],
    normal_vectors: np.ndarray,
    up_vectors: np.ndarray,
    rotations: np.ndarray,
):
    if isinstance(point_index, int):
        point_index = [point_index]

    feature_table = points_layer.features

    # get the normal vector
    current_normal_vectors = feature_table[
        [NAPARI_NORMAL_0, NAPARI_NORMAL_1, NAPARI_NORMAL_2]
    ].to_numpy()
    current_normal_vectors[point_index, :] = normal_vectors

    # get the up vector
    current_up_vectors = feature_table[
        [NAPARI_UP_0, NAPARI_UP_1, NAPARI_UP_2]
    ].to_numpy()
    current_up_vectors[point_index, :] = up_vectors

    # get the rotation
    current_rotations = feature_table[ROTATION].to_numpy()
    current_rotations[point_index] = rotations

    # set the values
    feature_table[NAPARI_NORMAL_0] = current_normal_vectors[:, 0]
    feature_table[NAPARI_NORMAL_1] = current_normal_vectors[:, 1]
    feature_table[NAPARI_NORMAL_2] = current_normal_vectors[:, 2]
    feature_table[NAPARI_UP_0] = current_up_vectors[:, 0]
    feature_table[NAPARI_UP_1] = current_up_vectors[:, 1]
    feature_table[NAPARI_UP_2] = current_up_vectors[:, 2]
    feature_table[ROTATION] = current_rotations


def update_rotations_on_points_layer(
    points_layer: Points,
    point_index: Union[int, List[int]],
    rotations: np.ndarray,
):
    if isinstance(point_index, int):
        point_index = [point_index]

    feature_table = points_layer.features

    # get the rotation
    current_rotations = feature_table[ROTATION].to_numpy()
    current_rotations[point_index] = rotations

    # set the values
    feature_table[ROTATION] = current_rotations
