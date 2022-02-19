import pygame

class App:
    def __init__(self):
        self.running = True
        self.screen = None
        self.size = self.weight, self.height = 640, 400

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.running = True

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def update(self):
        pass

    def render(self):
        # first draw the background, then
        # draw each object from a queue
        pass

    def cleanup(self):
        pygame.quit()

    def loop(self):
        # noinspection PySimplifyBooleanCheck
        if self.setup() == False:
            self.running = False
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.render()
        self.cleanup()

if __name__ == "__main__":
    app = App()
    app.loop()