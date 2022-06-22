from core import matrices
from math import pi
from numpy import ndarray
from numpy.linalg import inv
from OpenGL.GL import *

class Object2d:
    def __init__(self):
        self.local_transform = matrices.identity2d()
        self.parent: "Object2d" | None = None
        self.children: list["Object2d"] = []

    def add(self, child: "Object2d"):
        self.children.append(child)
        child.parent = self

    def remove(self, child: "Object2d"):
        self.children.remove(child)
        child.parent = None

    def global_transform(self):
        if self.parent is None:
            return self.local_transform
        return self.parent.global_transform() @ self.local_transform

    def descendants(self) -> list["Object2d"]:
        return [b for a in self.children for b in a.descendants()]

    def apply_transformation(self, matrix: ndarray, local = True):
        if local:
            self.local_transform = self.local_transform @ matrix
        else:
            self.local_transform =  matrix @ self.local_transform

    def translate(self, x: int | float, y: int | float, local = True):
        self.apply_transformation(matrices.translation(x, y), local)

    def rotation(self, theta: float, local = True):
        self.apply_transformation(matrices.rotation(theta), local)

    def scale(self, x: int | float, y: int | float | None = None, local = True):
        self.apply_transformation(matrices.scale2d(x, y), local)

    def get_position(self):
        return tuple(self.local_transform.item((i, 2)) for i in range(2))

    def set_position(self, x: int | float, y: int | float):
        self.local_transform.itemset((0, 2), x)
        self.local_transform.itemset((1, 2), y)

class Object3d:
    def __init__(self):
        self.local_transform = matrices.identity3d()
        self.parent: "Object3d" | None = None
        self.children: list["Object3d"] = []

    def add(self, child: "Object3d"):
        self.children.append(child)
        child.parent = self

    def remove(self, child: "Object3d"):
        self.children.remove(child)
        child.parent = None

    def global_transform(self):
        if self.parent is None:
            return self.local_transform
        return self.parent.global_transform() @ self.local_transform

    def descendants(self) -> list["Object3d"]:
        return [b for a in self.children for b in a.descendants()]

    def apply_transformation(self, matrix: ndarray, local = True):
        if local:
            self.local_transform = self.local_transform @ matrix
        else:
            self.local_transform =  matrix @ self.local_transform

    def translate(self, x: int | float, y: int | float, z: int | float, local = True):
        self.apply_transformation(matrices.translation(x, y, z), local)

    def x_rotation(self, theta: float, local = True):
        self.apply_transformation(matrices.x_rotation(theta), local)

    def y_rotation(self, theta: float, local = True):
        self.apply_transformation(matrices.y_rotation(theta), local)

    def z_rotation(self, theta: float, local = True):
        self.apply_transformation(matrices.z_rotation(theta), local)

    def scale(self, x: int | float, y: int | float | None = None, z: int | float | None = None, local = True):
        self.apply_transformation(matrices.scale3d(x, y, z), local)

    def get_position(self):
        return tuple(self.local_transform.item((i, 3)) for i in range(3))

    def set_position(self, x: int | float, y: int | float, z: int | float):
        self.local_transform.itemset((0, 3), x)
        self.local_transform.itemset((1, 3), y)
        self.local_transform.itemset((2, 3), z)

class Scene2d(Object2d):
    def __init__(self):
        super().__init__()

class Scene3d(Object3d):
    def __init__(self):
        super().__init__()

class Group2d(Object2d):
    def __init__(self):
        super().__init__()

class Group3d(Object3d):
    def __init__(self):
        super().__init__()

class Camera2d(Object2d):
    def __init__(self):
        super().__init__()
        self.view = matrices.identity2d()

    def update_view(self):
        self.view = inv(self.global_transform())

class Camera3d(Object3d):
    def __init__(self, a: float = pi/3, r: int | float = 1, n: int | float = 0.1, f: int | float = 100):
        super().__init__()
        self.projection = matrices.perspective(a, r, n, f)
        self.view = matrices.identity3d()

    def update_view(self):
        self.view = inv(self.global_transform())

class Mesh2d(Object2d):
    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        for v, a in geometry.attributes.items():
            a.assoc_var(material.program, v)
        glBindVertexArray(0)

class Mesh3d(Object3d):
    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        for v, a in geometry.attributes.items():
            a.assoc_var(material.program, v)
        glBindVertexArray(0)