from core import Attribute, Base, Uniform
from core.Matrices import *
from core.OpenGLUtil import *
from OpenGL.GL import *
from math import pi

class App(Base):
    def __init__(self):
        super().__init__(caption = "Pyokki")

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        print("Starting Pyokki!")
        vs_code = """
            in vec3 position;
            uniform mat4 projectionMatrix;
            uniform mat4 modelMatrix;
            void main(){
                gl_Position = projectionMatrix * modelMatrix * vec4(position, 1);
            }
        """
        fs_code = """
            out vec4 fragColor;
            void main(){
                fragColor = vec4(1, 1, 0, 1);
            }
        """
        self.prog = initialize_program(vs_code, fs_code)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        pos = [[   0,  0.2, 0],
               [ 0.1, -0.2, 0],
               [-0.1, -0.2, 0]]
        self.vertices = len(pos)
        p = Attribute("vec3", pos)
        p.assoc_var(self.prog, "position")
        m = translation(0, 0, -1)
        self.model = Uniform("mat4", m)
        self.model.locate_variable(self.prog, "modelMatrix")
        per = perspective()
        self.proj = Uniform("mat4", per)
        self.proj.locate_variable(self.prog, "projectionMatrix")

    def update(self):
        ms = 1/60
        rs = pi/60
        g = identity3d()
        if self.input.is_key_pressed("w"):
            g = translation(0, ms, 0) @ g
        if self.input.is_key_pressed("s"):
            g = translation(0, -ms, 0) @ g
        if self.input.is_key_pressed("d"):
            g = translation(ms, 0, 0) @ g
        if self.input.is_key_pressed("a"):
            g = translation(-ms, 0, 0) @ g
        if self.input.is_key_pressed("q"):
            g = z_rotation(rs) @ g
        if self.input.is_key_pressed("e"):
            g = z_rotation(-rs) @ g
        self.model.data = g @ self.model.data
        l = identity3d()
        if self.input.is_key_pressed("i"):
            l = translation(0, ms, 0) @ l
        if self.input.is_key_pressed("k"):
            l = translation(0, -ms, 0) @ l
        if self.input.is_key_pressed("l"):
            l = translation(ms, 0, 0) @ l
        if self.input.is_key_pressed("j"):
            l = translation(-ms, 0, 0) @ l
        if self.input.is_key_pressed("u"):
            l = z_rotation(rs) @ l
        if self.input.is_key_pressed("o"):
            l = z_rotation(-rs) @ l
        self.model.data = self.model.data @ l
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.prog)
        self.proj.upload_data()
        self.model.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertices)

if __name__ == "__main__":
    App().run()