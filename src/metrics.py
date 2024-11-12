"""
3D structures comparison metrics

"""
import numpy as np

def rmsd(coordinates_1: np.ndarray, coordinates_2: np.ndarray) -> float:
    """
    Compute the Root Mean Square deviation between two set of points, one set aligned to the other.

    Args
    ----
        coordinates_1:
            coordinates of the first set of points
        coordinates_2:
            coordinates of the second set of points

    Returns
    -------
        the Root Mean Square deviation between the two set of coordinates
    """
    return np.sqrt((((coordinates_1 - coordinates_2)**2).mean()))
