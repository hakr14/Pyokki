from math import sin, cos, tan, pi
import numpy as np

def identity():
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]).astype(float)

def translation(x: float, y: float, z: float):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]]).astype(float)

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


def scale(x: float, y: float | None = None, z: float | None = None):
    if z is None:
        if y is None:
            z = y = x
        else:
            raise TypeError("z must be defined if y is defined")
    elif y is None:
        raise TypeError("y must be defined if z is defined")
    return np.array([[x, 0, 0, 0],
                     [0, y, 0, 0],
                     [0, 0, z, 0],
                     [0, 0, 0, 1]]).astype(float)

def perspective(a: float = pi/3, r: float = 1, n: float = 0.1, f: float = 100):
    b = (f + n) / (n - f)
    c = 2 * f * n / (n - f)
    d = 1 / tan(a/2)
    return np.array([[d/r, 0,  0, 0],
                     [  0, d,  0, 0],
                     [  0, 0,  b, c],
                     [  0, 0, -1, 0]]).astype(float)