from core import Attribute, Base, Uniform
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
            uniform vec2 translation;
            void main(){
                vec2 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, 0, 1);
            }
        """
        fg_code = """
            out vec4 fragColor;
            void main(){
                fragColor = vec4(1, 1, 0, 1);
            }
        """
        self.program = initialize_program(vs_code, fg_code)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        positions = [[0, 0.2], [0.2, -0.2], [-0.2, -0.2]]
        pos = Attribute("vec2", positions)
        pos.assoc_var(self.program, "position")
        self.count = len(positions)
        self.trans = Uniform("vec2", [0, 0])
        self.trans.locate_variable(self.program, "translation")

    # noinspection PyUnresolvedReferences
    def update(self):
        glUseProgram(self.program)
        glClear(GL_COLOR_BUFFER_BIT)
        move_speed = 0.0075
        if self.input.is_key_pressed("left"):
            self.trans.data[0] -= move_speed
        if self.input.is_key_pressed("right"):
            self.trans.data[0] += move_speed
        if self.input.is_key_pressed("down"):
            self.trans.data[1] -= move_speed
        if self.input.is_key_pressed("up"):
            self.trans.data[1] += move_speed
        self.trans.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.count)

if __name__ == "__main__":
    App().run()