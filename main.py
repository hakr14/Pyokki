from core import Base

class App(Base):
    def __init__(self):
        super().__init__(name = "Pyokki")

    def initialize(self):
        print("Starting Pyokki!")

    def update(self):
        pass

if __name__ == "__main__":
    App().run()