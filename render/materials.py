from render import Uniform
from render.openGL_util import initialize_program
from OpenGL import GL
from typing import Any

class Material:
    def __init__(self, vs_code: str, fs_code: str):
        self.program = initialize_program(vs_code, fs_code)
        self.uniforms = {"modelMatrix": Uniform("mat4", None),
                         "viewMatrix": Uniform("mat4", None),
                         "projectionMatrix": Uniform("mat4", None)}
        self.settings = {"drawStyle": None}

    def locate_uniforms(self):
        for v, u in self.uniforms.items():
            u.locate_variable(self.program, v)

    def render_settings(self):
        raise NotImplementedError

    def set_properties(self, properties: dict[str, Any] = None):
        if properties is not None:
            for name, data in properties.items():
                if name in self.uniforms.keys():
                    self.uniforms[name].data = data
                elif name in self.settings.keys():
                    self.settings[name] = data
                else:
                    raise RuntimeError("Material has no property", name)

class BasicMaterial(Material):
    def __init__(self):
        vs_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec3 vertexColor;
            out vec3 color;
            void main(){
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
                color = vertexColor;
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            uniform bool useVertexColors;
            in vec3 color;
            out vec4 fragColor;
            void main(){
                vec4 c = vec4(baseColor, 1);
                if(useVertexColors)
                    c *= vec4(color, 1);
                fragColor = c;
            }
        """
        super().__init__(vs_code, fs_code)
        self.uniforms["baseColor"] = Uniform("vec3", [1, 1, 1])
        self.uniforms["useVertexColors"] = Uniform("bool", 0)
        self.locate_uniforms()

    def render_settings(self):
        raise NotImplementedError

class PointBasicMaterial(BasicMaterial):
    def __init__(self, properties = None):
        super().__init__()
        self.settings["drawStyle"] = GL.GL_POINTS
        self.settings["pointSize"] = 4
        self.settings["roundedPoints"] = True
        self.set_properties(properties)

    def render_settings(self):
        GL.glPointSize(self.settings["pointSize"])
        if self.settings["roundedPoints"]:
            GL.glEnable(GL.GL_POINT_SMOOTH)
        else:
            GL.glDisable(GL.GL_POINT_SMOOTH)

class LineBasicMaterial(BasicMaterial):
    def __init__(self, properties = None):
        super().__init__()
        self.settings["drawStyle"] = GL.GL_LINE_STRIP
        self.settings["lineType"] = "connected"
        self.settings["lineWidth"] = 2
        self.set_properties(properties)

    def render_settings(self):
        GL.glLineWidth(self.settings["lineWidth"])
        if self.settings["lineType"] == "connected":
            self.settings["drawStyle"] = GL.GL_LINE_STRIP
        elif self.settings["lineType"] == "loop":
            self.settings["drawStyle"] = GL.GL_LINE_LOOP
        elif self.settings["lineType"] == "segmented":
            self.settings["drawStyle"] = GL.GL_LINES
        else:
            raise ValueError("Invalid lineType", self.settings["lineType"])

class SurfaceBasicMaterial(BasicMaterial):
    def __init__(self, properties = None):
        super().__init__()
        self.settings["drawStyle"] = GL.GL_TRIANGLES
        self.settings["doubleSided"] = False
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 2
        self.set_properties(properties)

    def render_settings(self):
        if self.settings["doubleSided"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        if self.settings["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(self.settings["lineWidth"])