from render import matrices
from render.geometry import Geometry
from render.materials import Material
from math import pi
from numpy import ndarray
from numpy.linalg import inv
from OpenGL.GL import *

class Object3d:
    def __init__(self):
        self.local_transform = matrices.identity()
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
        d = [self]
        for c in self.children:
            d.extend(c.descendants())
        return d

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
        self.apply_transformation(matrices.scale(x, y, z), local)

    def get_position(self):
        return tuple(self.local_transform.item((i, 3)) for i in range(3))

    def set_position(self, x: int | float, y: int | float, z: int | float):
        self.local_transform.itemset((0, 3), x)
        self.local_transform.itemset((1, 3), y)
        self.local_transform.itemset((2, 3), z)

class Scene(Object3d):
    def __init__(self):
        super().__init__()

class Group(Object3d):
    def __init__(self):
        super().__init__()

class Camera(Object3d):
    def __init__(self, a: float = pi/3, r: int | float = 1, n: int | float = 0.1, f: int | float = 100):
        super().__init__()
        self.projection = matrices.perspective(a, r, n, f)
        self.view = matrices.identity()

    def update_view(self):
        self.view = inv(self.global_transform())

class Mesh(Object3d):
    def __init__(self, geometry: Geometry, material: Material):
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        for v, a in geometry.attributes.items():
            a.assoc_var(material.program, v)
        glBindVertexArray(0)