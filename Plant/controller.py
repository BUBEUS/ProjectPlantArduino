import tkinter as tk
from .model import PlantModel
from .view import SystemView


class SystemController:

    def __init__(self):
        self.model = PlantModel()
        self.root=tk.Tk()
        self.view = SystemView(self.root, self)




    def run(self) -> None:
        """Runs the main GUI application loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = SystemController()
    app.run()