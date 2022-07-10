from render import Base, matrices
from render.geometry import Cylindrical
from render.materials import SurfaceBasicMaterial
from render.objects import Camera, Mesh, Scene
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
        self.camera.set_position(0, 0, 4)

    def update(self):
        self.mesh.apply_transformation(matrices.x_rotation(0.04))
        self.mesh.apply_transformation(matrices.y_rotation(0.015))
        self.renderer.render(self.scene, self.camera)

if __name__ == "__main__":
    App().run()