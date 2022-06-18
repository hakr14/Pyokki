from math import sin, cos, tan, pi
import numpy as np

def identity2d():
    return np.array([[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]]).astype(float)
def identity3d():
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]).astype(float)

def translation(x: int | float, y: int| float, z: int | float | None = None):
    if z is None:
        return translation2d(x, y)
    else:
        return translation3d(x, y, z)
def translation2d(x: int | float, y: int | float):
    return np.array([[1, 0, x],
                     [0, 1, y],
                     [0, 0, 1]]).astype(float)
def translation3d(x: int | float, y: int | float, z: int | float):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]]).astype(float)

def rotation(theta: float):
    s = sin(theta)
    c = cos(theta)
    return np.array([[c, -s, 0],
                     [s,  c, 0],
                     [0,  0, 1]]).astype(float)
def x_rotation(theta: float):
    s = sin(theta)
    c = cos(theta)
    return np.array([[1, 0,  0, 0],
                     [0, c, -s, 0],
                     [0, s,  c, 0],
                     [0, 0,  0, 1]]).astype(float)
def y_rotation(theta: float):
    s = sin(theta)
    c = cos(theta)
    return np.array([[ c, 0, s, 0],
                     [ 0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [ 0, 0, 0, 1]]).astype(float)
def z_rotation(theta: float):
    s = sin(theta)
    c = cos(theta)
    return np.array([[c, -s, 0, 0],
                     [s,  c, 0, 0],
                     [0,  0, 1, 0],
                     [0,  0, 0, 1]]).astype(float)

def scale2d(x: int | float, y: int | float | None = None):
    if y is None:
        y = x
    return np.array([[x, 0, 0],
                     [0, y, 0],
                     [0, 0, 1]]).astype(float)
def scale3d(x: int | float, y: int | float | None = None, z: int | float | None = None):
    if z is None:
        if y is None:
            z = y = x
        else:
            return scale2d(x, y)
    return np.array([[x, 0, 0, 0],
                     [0, y, 0, 0],
                     [0, 0, z, 0],
                     [0, 0, 0, 1]]).astype(float)

def perspective(a: float = pi/3, r: int | float = 1, n: int | float = 0.1, f: int | float = 100):
    b = (f + n) / (n - f)
    c = 2 * f * n / (n - f)
    d = 1 / tan(a/2)
    return np.array([[d/r, 0,  0, 0],
                     [  0, d,  0, 0],
                     [  0, 0,  b, c],
                     [  0, 0, -1, 0]]).astype(float)