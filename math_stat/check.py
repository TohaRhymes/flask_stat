import numpy as np


def min_max_check(array: np.array, min: float, max: float) -> bool:
    return all((array >= min) & (array <= max))
