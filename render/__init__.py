from enum import Enum
import numpy as np
from OpenGL.GL import *
import pygame
from sys import exit, stderr

class Base:
    def __init__(self, width: int = 512, height: int = 512, caption: str = "Graphics Window", icon_path: str | None = None, max_fps: int = 60):
        pygame.init()
        self.size = self.width, self.height = width, height
        self.flags = pygame.DOUBLEBUF | pygame.OPENGL
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        self.screen = pygame.display.set_mode(self.size, self.flags)
        pygame.display.set_caption(caption)
        if icon_path is not None:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        self.running = True
        self.clock = pygame.time.Clock()
        self.input = Input()
        self.max_fps = max_fps
        self.delta = 1 / max_fps

    def initialize(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def run(self):
        self.initialize()
        while self.running:
            self.input.update()
            if self.input.quit:
                self.running = False
                break
            self.update()
            pygame.display.flip()
            self.delta = self.clock.tick(self.max_fps) / 1000
        pygame.quit()
        exit(0)

class Input:
    def __init__(self):
        self.quit = False
        self.keys_down = self.keys_pressed = self.keys_up = set()

    def update(self):
        self.keys_down = self.keys_up = set()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                self.keys_down.add(event.key)
                self.keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_up.add(event.key)
                try:
                    self.keys_pressed.remove(event.key)
                except KeyError:
                    pass

    def is_key_down(self, key_name: str | None):
        return key_name in map(pygame.key.name, self.keys_down)

    def is_key_pressed(self, key_name: str | None):
        return key_name in map(pygame.key.name, self.keys_pressed)

    def is_key_up(self, key_name: str | None):
        return key_name in map(pygame.key.name, self.keys_up)

class Attribute:
    class Type(Enum):
        INT   = 1
        FLOAT = 2
        VEC2  = 3
        VEC3  = 4
        VEC4  = 5

    def __init__(self, data_type: Type, data: list | tuple | float):
        self.data_type = data_type
        self.data = data
        self.buffer = glGenBuffers(1)
        self.upload_data()

    def upload_data(self):
        data = np.array(self.data).astype(np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def assoc_var(self, prog_ref, var_name: str):
        var_ref = glGetAttribLocation(prog_ref, var_name)
        if var_ref == -1:
            print(f"Variable {var_name} not found.", file = stderr)
            return
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        if self.data_type is Attribute.Type.INT:
            glVertexAttribPointer(var_ref, 1, GL_INT, False, 0, None)
        elif self.data_type is Attribute.Type.FLOAT:
            glVertexAttribPointer(var_ref, 1, GL_FLOAT, False, 0, None)
        elif self.data_type is Attribute.Type.VEC2:
            glVertexAttribPointer(var_ref, 2, GL_FLOAT, False, 0, None)
        elif self.data_type is Attribute.Type.VEC3:
            glVertexAttribPointer(var_ref, 3, GL_FLOAT, False, 0, None)
        elif self.data_type is Attribute.Type.VEC4:
            glVertexAttribPointer(var_ref, 4, GL_FLOAT, False, 0, None)
        else:
            raise ValueError(f"Variable type {self.data_type} not recognized.")
        glEnableVertexAttribArray(var_ref)

class Uniform:
    class Type(Enum):
        INT       = 1
        BOOL      = 1
        FLOAT     = 2
        VEC2      = 3
        VEC3      = 4
        VEC4      = 5
        MAT4      = 6
        SAMPLER2D = 7

    def __init__(self, data_type: Type, data: list | tuple | float | np.ndarray | None):
        self.data_type = data_type
        self.data = data
        self.var = None

    def locate_variable(self, prog_ref, var_name: str):
        self.var = glGetUniformLocation(prog_ref, var_name)
        if self.var == -1:
            self.var = None
            raise NameError(f"Variable {var_name} not found.")

    def upload_data(self):
        if self.var is None:
            raise UnboundLocalError("Variable reference not set.")
        if self.data_type is Uniform.Type.INT:
            glUniform1i(self.var, self.data)
        elif self.data_type is Uniform.Type.FLOAT:
            glUniform1f(self.var, self.data)
        elif self.data_type is Uniform.Type.VEC2:
            glUniform2f(self.var, *self.data)
        elif self.data_type is Uniform.Type.VEC3:
            glUniform3f(self.var, *self.data)
        elif self.data_type is Uniform.Type.VEC4:
            glUniform4f(self.var, *self.data)
        elif self.data_type is Uniform.Type.MAT4:
            glUniformMatrix4fv(self.var, 1, GL_TRUE, self.data)
        elif self.data_type is Uniform.Type.SAMPLER2D:
            obj, unit = self.data
            glActiveTexture(GL_TEXTURE0 + unit)
            glBindTexture(GL_TEXTURE_2D, obj)
            glUniform1i(self.var, unit)
        else:
            raise ValueError(f"Variable type {self.data_type} not recognized.")

class Texture:
    def __init__(self, filename: str = None, properties: dict[str, Constant] = None):
        self.w, self.h = 0, 0
        self.data: str | None = None
        self.tex = glGenTextures(1)
        self.properties = {"magFilter": GL_LINEAR, "minFilter": GL_LINEAR_MIPMAP_LINEAR, "wrap": GL_CLAMP_TO_BORDER, "informat": GL_RGBA, "format": GL_RGBA}
        self.set_properties(properties)
        if filename is not None:
            self.load_image(pygame.image.load(filename))
            self.upload()

    def load_image(self, surface: pygame.Surface):
        self.w, self.h = surface.get_size()
        self.data = pygame.image.tostring(surface, "RGBA", True)

    def set_properties(self, properties):
        if properties is not None:
            for k, v in properties.items():
                if k in self.properties.keys():
                    self.properties[k] = v
                else:
                    raise RuntimeError("Texture has no property", k)

    def upload(self):
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexImage2D(GL_TEXTURE_2D, 0, self.properties["informat"], self.w, self.h, 0, self.properties["format"], GL_UNSIGNED_BYTE, self.data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.properties["magFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.properties["minFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.properties["wrap"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.properties["wrap"])