from enum import Enum
from math import pi
from numpy import ndarray
from numpy.linalg import inv
from OpenGL import GL
from render import Input, matrices
from render.geometry import Geometry
from render.materials import Material

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

    def translate(self, x: float, y: float, z: float, local = True):
        self.apply_transformation(matrices.translation(x, y, z), local)

    def x_rotation(self, theta: float, local = True):
        self.apply_transformation(matrices.x_rotation(theta), local)

    def y_rotation(self, theta: float, local = True):
        self.apply_transformation(matrices.y_rotation(theta), local)

    def z_rotation(self, theta: float, local = True):
        self.apply_transformation(matrices.z_rotation(theta), local)

    def scale(self, x: float, y: float | None = None, z: float | None = None, local = True):
        self.apply_transformation(matrices.scale(x, y, z), local)

    def get_position(self):
        return tuple(self.local_transform.item((i, 3)) for i in range(3))

    def set_position(self, x: float, y: float, z: float):
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
    def __init__(self, a: float = pi/3, r: float = 1, n: float = 0.1, f: float = 100):
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
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
        for v, a in geometry.attributes.items():
            a.assoc_var(material.program, v)
        GL.glBindVertexArray(0)

class Controller(Object3d):
    class Moves(Enum):
        FORWARD         =  1
        BACK            =  2
        LEFT            =  3
        RIGHT           =  4
        UP              =  5
        DOWN            =  6
        TURN_UP         =  7
        TURN_DOWN       =  8
        LOOK_UP         =  9
        LOOK_DOWN       = 10
        TURN_LEFT       = 11
        TURN_RIGHT      = 12
        LOOK_LEFT       = 13
        LOOK_RIGHT      = 14
        TURN_TILT_LEFT  = 15
        TURN_TILT_RIGHT = 16
        LOOK_TILT_LEFT  = 17
        LOOK_TILT_RIGHT = 18

    def __init__(self, keys: dict[Moves, str|None] = None, move_speed: float = 1, turn_speed = pi / 3, local = True):
        super().__init__()
        self.looker = Object3d()
        self.children.append(self.looker)
        self.looker.parent = self
        if keys is None:
            self.keys = {}
        else:
            self.keys = keys
        for m in Controller.Moves:
            if m not in self.keys:
                self.keys[m] = None
        self.move_speed = move_speed
        self.turn_speed = turn_speed
        self.local = local

    def add(self, child):
        self.looker.add(child)

    def remove(self, child):
        self.looker.remove(child)

    def update(self, inputs: Input, delta: float):
        ma = self.move_speed * delta
        ta = self.turn_speed * delta
        if inputs.is_key_pressed(self.keys[Controller.Moves.FORWARD]):
            self.translate(0, 0, -ma, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.BACK]):
            self.translate(0, 0, ma, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.LEFT]):
            self.translate(-ma, 0, 0, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.RIGHT]):
            self.translate(ma, 0, 0, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.UP]):
            self.translate(0, ma, 0, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.DOWN]):
            self.translate(0, -ma, 0, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.TURN_UP]):
            self.x_rotation(ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.TURN_DOWN]):
            self.x_rotation(-ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.LOOK_UP]):
            self.looker.x_rotation(ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.LOOK_DOWN]):
            self.looker.x_rotation(-ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.TURN_LEFT]):
            self.y_rotation(ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.TURN_RIGHT]):
            self.y_rotation(-ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.LOOK_LEFT]):
            self.looker.y_rotation(ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.LOOK_RIGHT]):
            self.looker.y_rotation(-ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.TURN_TILT_LEFT]):
            self.z_rotation(ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.TURN_TILT_RIGHT]):
            self.z_rotation(-ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.LOOK_TILT_LEFT]):
            self.looker.z_rotation(ta, self.local)
        if inputs.is_key_pressed(self.keys[Controller.Moves.LOOK_TILT_RIGHT]):
            self.looker.z_rotation(-ta, self.local)