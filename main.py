from core import Attribute, Base, Uniform
from core.OpenGLUtil import *
from math import sin
from OpenGL.GL import *

class App(Base):
    def __init__(self):
        super().__init__(caption = "Pyokki")

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        print("Starting Pyokki!")
        vs_code = """
            in vec2 position;
            uniform vec2 translation;
            void main(){
                vec2 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, 0, 1);
            }
        """
        fg_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main(){
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1);
            }
        """
        self.program = initialize_program(vs_code, fg_code)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        pos = [[0, 0.2], [0.2, -0.2], [-0.2, -0.2]]
        self.vertex_count = len(pos)
        pos_attr = Attribute("vec2", pos)
        pos_attr.assoc_var(self.program, "position")
        self.trans1 = Uniform("vec2", [-0.5, 0])
        self.trans1.locate_variable(self.program, "translation")
        self.trans2 = Uniform("vec2", [0.5, 0])
        self.trans2.locate_variable(self.program, "translation")
        self.color1 = Uniform("vec3", [1, 0, 0])
        self.color1.locate_variable(self.program, "baseColor")
        self.color2 = Uniform("vec3", [0, 0, 1])
        self.color2.locate_variable(self.program, "baseColor")
        self.time = 0

    def update(self):
        glUseProgram(self.program)
        glClear(GL_COLOR_BUFFER_BIT)
        self.time += self.clock.get_time()

        # noinspection PyUnresolvedReferences
        self.trans2.data[1] = sin(self.time/1000)*0.6

        self.trans1.upload_data()
        self.color1.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
        self.trans2.upload_data()
        self.color2.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

if __name__ == "__main__":
    App().run()