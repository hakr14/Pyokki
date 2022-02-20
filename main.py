from core import Attribute, Base
from core.OpenGLUtil import *
from OpenGL.GL import *

class App(Base):
    def __init__(self):
        super().__init__(caption = "Pyokki")

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        print("Starting Pyokki!")
        vs_code = """
            in vec2 position;
            in vec3 vertexColor;
            out vec3 color;
            void main(){
                gl_Position = vec4(position.x, position.y, 0, 1);
                color = vertexColor;
            }
        """
        fg_code = """
            in vec3 color;
            void main(){
                gl_FragColor = vec4(color.r, color.g, color.b, 1);
            }
        """
        self.program = initialize_program(vs_code, fg_code)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        pos = [[0.8, 0], [0.4, 0.6], [-0.4, 0.6], [-0.8, 0], [-0.4, -0.6], [0.4, -0.6]]
        self.vertex_count = len(pos)
        pos_attr = Attribute("vec2", pos)
        pos_attr.assoc_var(self.program, "position")
        color = [[1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1]]
        color_attr = Attribute("vec3", color)
        color_attr.assoc_var(self.program, "vertexColor")

    def update(self):
        glUseProgram(self.program)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertex_count)

if __name__ == "__main__":
    App().run()