import pygame
import sys

class Base:
    def __init__(self, width: int = 512, height: int = 512, name: str = "Graphics Window"):
        pygame.init()
        self.size = self.width, self.height = width, height
        self.flags = pygame.DOUBLEBUF | pygame.OPENGL
        self.screen = pygame.display.set_mode(self.size, self.flags)
        pygame.display.set_caption(name)
        self.running = True
        self.clock = pygame.time.Clock()
        self.input = Input()

    def initialize(self):
        pass

    def update(self):
        pass

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
        sys.exit(0)

class Input:
    def __init__(self):
        self.quit = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True