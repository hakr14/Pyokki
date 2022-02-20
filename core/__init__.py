import numpy as np
from OpenGL.GL import *
import pygame
from sys import exit
from typing import Iterable

class Base:
    def __init__(self, width: int = 512, height: int = 512, caption: str = "Graphics Window"):
        pygame.init()
        self.size = self.width, self.height = width, height
        self.flags = pygame.DOUBLEBUF | pygame.OPENGL
        self.screen = pygame.display.set_mode(self.size, self.flags)
        pygame.display.set_caption(caption)
        self.running = True
        self.clock = pygame.time.Clock()
        self.input = Input()

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
            self.clock.tick(60)
        pygame.quit()
        exit(0)

class Input:
    def __init__(self):
        self.quit = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

class Attribute:
    def __init__(self, data_type: str, data: Iterable | int | float):
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
            raise NameError(f"Variable {var_name} not found.")
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        if self.data_type == "int":
            glVertexAttribPointer(var_ref, 1, GL_INT, False, 0, None)
        elif self.data_type == "float":
            glVertexAttribPointer(var_ref, 1, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(var_ref, 2, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec3":
            glVertexAttribPointer(var_ref, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec4":
            glVertexAttribPointer(var_ref, 4, GL_FLOAT, False, 0, None)
        else:
            raise ValueError(f"Variable type {self.data_type} not recognized.")
        glEnableVertexAttribArray(var_ref)