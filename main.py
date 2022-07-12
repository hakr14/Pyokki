from render import Base
from render.geometry import Cylindrical
from render.materials import SurfaceBasicMaterial
from render.objects import Camera, Controller, Mesh, Scene
from render.render import Renderer

class App(Base):
    def __init__(self):
        super().__init__(caption = "Pyokki")

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        print("Starting Pyokki!")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera()
        geo = Cylindrical(x_rad_top = 1.5, x_rad_bottom = 0.5, z_rad_top = -0.3, z_rad_bottom = 2, height = 1.75)
        mat = SurfaceBasicMaterial({"useVertexColors": 1, "doubleSided": 1})
        self.mesh = Mesh(geo, mat)
        self.scene.add(self.mesh)
        self.move = Controller({Controller.Moves.FORWARD: "w", Controller.Moves.BACK: "s",
                                Controller.Moves.LEFT: "a", Controller.Moves.RIGHT: "d",
                                Controller.Moves.TURN_LEFT: "q", Controller.Moves.TURN_RIGHT: "e",
                                Controller.Moves.UP: "r", Controller.Moves.DOWN: "f",
                                Controller.Moves.LOOK_UP: "t", Controller.Moves.LOOK_DOWN: "g"})
        self.move.add(self.camera)
        self.scene.add(self.move)
        self.move.set_position(0, 0, 4)

    def update(self):
        self.move.update(self.input, self.delta)
        self.renderer.render(self.scene, self.camera)

if __name__ == "__main__":
    App().run()