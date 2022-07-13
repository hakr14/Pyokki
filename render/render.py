from render.objects import Camera, Mesh, Scene
from OpenGL.GL import *

class Renderer:
    def __init__(self, clear_color = (0, 0, 0)):
        glEnable(GL_DEPTH_TEST)
        glClearColor(*clear_color, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    @staticmethod
    def render(scene: Scene, camera: Camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.update_view()
        for obj in scene.descendants():
            if isinstance(obj, Mesh) and obj.visible:
                glUseProgram(obj.material.program)
                glBindVertexArray(obj.vao)
                obj.material.uniforms["modelMatrix"].data = obj.global_transform()
                obj.material.uniforms["viewMatrix"].data = camera.view
                obj.material.uniforms["projectionMatrix"].data = camera.projection
                for u in obj.material.uniforms.values():
                    u.upload_data()
                obj.material.render_settings()
                glDrawArrays(obj.material.settings["drawStyle"], 0, obj.geometry.vertex_count)