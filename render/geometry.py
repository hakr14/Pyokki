from render import Attribute

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

class Rectangle(Geometry):
    def __init__(self, width = 1, height = 1):
        super().__init__()
        p0 = [-width / 2, -height / 2, 0]
        p1 = [ width / 2, -height / 2, 0]
        p2 = [-width / 2,  height / 2, 0]
        p3 = [ width / 2,  height / 2, 0]
        c0 = [1, 1, 1]
        c1 = [0, 1, 1]
        c2 = [1, 0, 1]
        c3 = [1, 1, 0]
        pos = [p0, p1, p3, p0, p3, p2]
        col = [c0, c1, c3, c0, c3, c2]
        self.attributes["vertexPosition"] = Attribute("vec3", pos)
        self.attributes["vertexColor"] = Attribute("vec3", col)
        self.count_vertices()

class Box(Geometry):
    def __init__(self, width = 1, height = 1, depth = 1):
        super().__init__()
        p0 = [-width / 2, -height / 2, -depth / 2]
        p1 = [ width / 2, -height / 2, -depth / 2]
        p2 = [-width / 2,  height / 2, -depth / 2]
        p3 = [ width / 2,  height / 2, -depth / 2]
        p4 = [-width / 2, -height / 2,  depth / 2]
        p5 = [ width / 2, -height / 2,  depth / 2]
        p6 = [-width / 2,  height / 2,  depth / 2]
        p7 = [ width / 2,  height / 2,  depth / 2]
        c0 = [0, 0, 0]
        c1 = [1, 0, 0]
        c2 = [0, 1, 0]
        c3 = [1, 1, 0]
        c4 = [0, 0, 1]
        c5 = [1, 0, 1]
        c6 = [0, 1, 1]
        c7 = [1, 1, 1]
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
        self.attributes["vertexPosition"] = Attribute("vec3", pos)
        self.attributes["vertexColor"] = Attribute("vec3", col)
        self.count_vertices()