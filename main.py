from core import Base
from core.OpenGLUtil import *
from OpenGL import GL

class App(Base):
    def __init__(self):
        super().__init__(name = "Pyokki")

    def initialize(self):
        print("Starting Pyokki!")
        vsCode = """
            void main(){
                gl_Position = vec4(0, 0, 0, 1);
            }
        """
        fgCode = """
            void main(){
                gl_FragColor = vec4(1, 1, 0, 1);
            }
        """
        self.program = initialize_program(vsCode, fgCode)

    def update(self):
        GL.glUseProgram(self.program)
        GL.glDrawArrays(GL.GL_POINTS, 0, 1)

if __name__ == "__main__":
    App().run()