from core.objects import *
from csv import reader
import numpy as np
from typing import Iterable

def parse_pyk(filename: Iterable[str]):
    return reader(filename, delimiter='|', escapechar='\\')

def convert_2d_3d(matrix2d: np.ndarray) -> np.ndarray:
    matrix3d: np.ndarray = np.pad(matrix2d, ((0, 1), (0, 1)))
    matrix3d[[2, 3]] = matrix3d[[3, 2]]
    matrix3d[:, [2, 3]] = matrix3d[:, [3, 2]]
    matrix3d.itemset((2, 2), 1)
    return matrix3d

def convert_tree(obj: Object2d | Scene2d | Group2d | Camera2d | Mesh2d):
    o: Object3d | Scene3d | Group3d | Camera3d | Mesh3d
    if isinstance(obj, Scene2d):
        o = Scene3d()
    elif isinstance(obj, Group2d):
        o = Group3d()
    elif isinstance(obj, Camera2d):
        o = Camera3d()
    elif isinstance(obj, Mesh2d):
        o = Mesh3d(obj.geometry, obj.material)
    else:
        o = Object3d()
    o.apply_transformation(convert_2d_3d(obj.local_transform))
    for c in obj.children:
        n = convert_tree(c)
        o.add(n)
    return o