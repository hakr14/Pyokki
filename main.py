import util
from core import Base
from core.matrices import *

class App(Base):
    def __init__(self):
        super().__init__(caption = "Pyokki")

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        print("Starting Pyokki!")
        m = translation2d(4, 5) @ rotation(pi/3) @ scale2d(1.5)
        print(util.convert_2d_3d(m))
        print(m)

    def update(self):
        pass

if __name__ == "__main__":
    App().run()