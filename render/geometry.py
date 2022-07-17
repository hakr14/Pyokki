from math import cos, sin, pi
from numpy import linspace
from render import Attribute
from typing import Callable

class Geometry:
    def __init__(self):
        self.attributes: dict[str, Attribute] = {}
        self.vertex_count = 0

    def count_vertices(self):
        for v in self.attributes.values():
            if isinstance(v.data, (list, tuple)):
                self.vertex_count = len(v.data)
                return
        raise RuntimeError("No sized attribute found")

    def add_attribute(self, data_type: Attribute.Type, var_name: str, data: list|tuple|int|float):
        self.attributes[var_name] = Attribute(data_type, data)

class Rectangle(Geometry):
    def __init__(self, width = 1, height = 1):
        super().__init__()
        p0 = (-width / 2, -height / 2, 0)
        p1 = ( width / 2, -height / 2, 0)
        p2 = (-width / 2,  height / 2, 0)
        p3 = ( width / 2,  height / 2, 0)
        c0 = (1, 1, 1)
        c1 = (0, 1, 1)
        c2 = (1, 0, 1)
        c3 = (1, 1, 0)
        t0 = (0, 0)
        t1 = (1, 0)
        t2 = (0, 1)
        t3 = (1, 1)
        pos = [p0, p1, p3, p0, p3, p2]
        col = [c0, c1, c3, c0, c3, c2]
        tex = [t0, t1, t3, t0, t3, t2]
        self.add_attribute(Attribute.Type.VEC3, "vertexPosition", pos)
        self.add_attribute(Attribute.Type.VEC3, "vertexColor", col)
        self.add_attribute(Attribute.Type.VEC2, "vertexUV", tex)
        self.count_vertices()

class Polygon(Geometry):
    def __init__(self, sides: int = 6, rad: float = 1):
        super().__init__()
        a = 2 * pi / sides
        pos = [p for s in range(sides) for p in [(0, 0, 0), (rad*cos(s*a), rad*sin(s*a), 0), (rad*cos((s+1)*a), rad*sin((s+1)*a), 0)]]
        col = [(1, 1, 1), (0.75, 0.75, 0.75), (0.75, 0.75, 0.75)] * sides
        tex = [p for s in range(sides) for p in [(0.5, 0.5), (cos(s * a) * 0.5 + 0.5, sin(s * a) * 0.5 + 0.5), (cos((s + 1) * a) * 0.5 + 0.5, sin((s + 1) * a) * 0.5 + 0.5)]]
        self.add_attribute(Attribute.Type.VEC3, "vertexPosition", pos)
        self.add_attribute(Attribute.Type.VEC3, "vertexColor", col)
        self.add_attribute(Attribute.Type.VEC2, "vertexUV", tex)
        self.count_vertices()

class Box(Geometry):
    def __init__(self, width = 1, height = 1, depth = 1):
        super().__init__()
        p0 = (-width / 2, -height / 2, -depth / 2)
        p1 = ( width / 2, -height / 2, -depth / 2)
        p2 = (-width / 2,  height / 2, -depth / 2)
        p3 = ( width / 2,  height / 2, -depth / 2)
        p4 = (-width / 2, -height / 2,  depth / 2)
        p5 = ( width / 2, -height / 2,  depth / 2)
        p6 = (-width / 2,  height / 2,  depth / 2)
        p7 = ( width / 2,  height / 2,  depth / 2)
        c0 = (0, 0, 0)
        c1 = (1, 0, 0)
        c2 = (0, 1, 0)
        c3 = (1, 1, 0)
        c4 = (0, 0, 1)
        c5 = (1, 0, 1)
        c6 = (0, 1, 1)
        c7 = (1, 1, 1)
        t0 = (0, 0)
        t1 = (1, 0)
        t2 = (0, 1)
        t3 = (1, 1)
        pos = [p5, p1, p3, p5, p3, p7,
               p0, p4, p6, p0, p6, p2,
               p6, p7, p3, p6, p3, p2,
               p0, p1, p5, p0, p5, p4,
               p4, p5, p7, p4, p7, p6,
               p1, p0, p2, p1, p2, p3]
        col = [c5, c1, c3, c5, c3, c7,
               c0, c4, c6, c0, c6, c2,
               c6, c7, c3, c6, c3, c2,
               c0, c1, c5, c0, c5, c4,
               c4, c5, c7, c4, c7, c6,
               c1, c0, c2, c1, c2, c3]
        tex = [t0, t1, t3, t0, t3, t2] * 6
        self.add_attribute(Attribute.Type.VEC3, "vertexPosition", pos)
        self.add_attribute(Attribute.Type.VEC3, "vertexColor", col)
        self.add_attribute(Attribute.Type.VEC2, "vertexUV", tex)
        self.count_vertices()

class Parametric(Geometry):
    def __init__(self, us: float, ue: float, ur: int, vs: float, ve: float, vr: int, func: Callable[[float, float], tuple[float, float, float]]):
        super().__init__()
        grid = [[(u, v) for v in linspace(0, 1, vr + 1)] for u in linspace(0, 1, ur + 1)]
        tex = []
        for x in range(ur):
            for y in range(vr):
                a = grid[x][y]
                b = grid[x+1][y]
                c = grid[x+1][y+1]
                d = grid[x][y+1]
                tex.extend([a, b, c, a, c, d])
        pos = list(map(lambda p: func(*p), map(lambda p: (p[0] * (ue - us) + us, p[1] * (ve - vs) + vs), tex)))
        col = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0)] * ur * vr
        self.add_attribute(Attribute.Type.VEC3, "vertexPosition", pos)
        self.add_attribute(Attribute.Type.VEC3, "vertexColor", col)
        self.add_attribute(Attribute.Type.VEC2, "vertexUV", tex)
        self.count_vertices()

class Plane(Parametric):
    def __init__(self, width: float = 1, height: float = 1, w_sub: int = 50, h_sub: int = 50):
        def func(u: float, v: float):
            return u, v, 0
        super().__init__(-width / 2, width / 2, w_sub, -height / 2, height / 2, h_sub, func)

class Ellipsoid(Parametric):
    def __init__(self, x_rad: float = 1, y_rad: float = 1, z_rad: float = 1, ur = 50, vr = 50):
        def func(u: float, v: float):
            return x_rad * sin(u) * cos(v), y_rad * sin(v), z_rad * cos(u) * cos(v)
        super().__init__(0, 2*pi, ur, 0, 2*pi, vr, func)

class Sphere(Ellipsoid):
    def __init__(self, radius = 1, ur = 50, vr = 50):
        super().__init__(radius, radius, radius, ur, vr)

class Cylindrical(Parametric):
    def __init__(self, x_rad_top: float = 1, x_rad_bottom: float = 1, z_rad_top: float = 1, z_rad_bottom: float = 1, height: float = 1, res = 50):
        def func(u: float, v: float):
            return (v * x_rad_top + (1-v) * x_rad_bottom) * sin(u), height * (v - 0.5), (v * z_rad_top + (1-v) * z_rad_bottom) * cos(u)
        super().__init__(0, 2*pi, res, 0, 1, 1, func)

class Cylinder(Cylindrical):
    def __init__(self, radius: float = 1, height: float = 1, res = 50):
        super().__init__(radius, radius, radius, radius, height, res)

class Prism(Cylindrical):
    def __init__(self, radius: float = 1, height: float = 1, sides = 4):
        super().__init__(radius, radius, radius, radius, height, sides)

class Cone(Cylindrical):
    def __init__(self, radius: float = 1, height: float = 1, res = 50):
        super().__init__(0, radius, 0, radius, height, res)

class Pyramid(Cylindrical):
    def __init__(self, radius: float = 1, height: float = 1, sides = 4):
        super().__init__(0, radius, 0, radius, height, sides)