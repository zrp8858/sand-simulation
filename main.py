import sys
from typing import override

import numpy as np
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class SandGrid:
    """
    Logical representation of the grid of sand.
    Keeps track of which pixels are sand and which are not.
    """

    def __init__(self, width, height):
        """
        Initializes the grid to all zeroes (non-sand).
        :param width: Width of the grid.
        :param height: Height of the grid.
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)

    def update_grid(self):
        """
        Updates the entire grid of sand.
        Moves particles down that have empty spaces below them.
        """
        for y in range(self.height - 2, -1, -1):
            for x in range(self.width):
                if self.grid[y, x] == 1:
                    self.update_pixel(x, y)

    def update_pixel(self, x, y):
        """
        Updates a single pixel on the grid.
        Moves it down if there is an empty space below it, or below left and right.
        :param x: x-coordinate of the pixel.
        :param y: y-coordinate of the pixel.
        """
        if y + 1 < self.height and self.grid[y + 1, x] == 0:
            self.grid[y, x] = 0
            self.grid[y + 1, x] = 1

        elif x > 0 and y + 1 < self.height and self.grid[y + 1, x - 1] == 0:
            self.grid[y, x] = 0
            self.grid[y + 1, x - 1] = 1

        elif (
            x < self.width - 1 and y + 1 < self.height and self.grid[y + 1, x + 1] == 0
        ):
            self.grid[y, x] = 0
            self.grid[y + 1, x + 1] = 1


class SandWidget(QWidget):
    """
    Visual representation of the sand.
    """

    def __init__(self, width, height):
        """
        Initializes the widget, including a logical representation of it as a SandGrid.
        :param width: Width of the grid.
        :param height: Height of the grid.
        """
        super().__init__()
        self.cell_size = 10
        self.grid_width = width
        self.grid_height = height
        self.setFixedSize(
            self.grid_width * self.cell_size, self.grid_height * self.cell_size
        )

        self.sand_grid = SandGrid(width, height)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def tick(self):
        """
        Updates the grid logically and then visually.
        """
        self.sand_grid.update_grid()
        self.update()

    def add_sand(self, event):
        """
        Adds a particle of sand to the grid.
        :param event: The event that caused the sand to be added.
        """
        x = event.x() // self.cell_size
        y = event.y() // self.cell_size

        if 0 <= x < self.sand_grid.width and 0 <= y < self.sand_grid.height:
            self.sand_grid.grid[y, x] = 1

    @override(QWidget)
    def mousePressEvent(self, event):
        """
        When the mouse is clicked, adds sand to the grid under the mouse.
        :param event: The mouse press event.
        """
        self.add_sand(event)

    @override(QWidget)
    def mouseMoveEvent(self, event):
        """
        When the mouse is moved, checks if the mouse is pressed.
        If so, adds sand to the grid under the mouse.
        :param event: The mouse move event.
        """
        if event.buttons() & Qt.LeftButton:
            self.add_sand(event)

    @override(QWidget)
    def paintEvent(self, event):
        """
        When a paint event happens (triggered by update() usually),
        updates the visual representation of the grid to match the logical representation.
        :param event: The paint event.
        """
        painter = QPainter(self)

        rgb = np.zeros((self.grid_height, self.grid_width, 3), dtype=np.uint8)

        rgb[self.sand_grid.grid == 1] = [189, 149, 3]
        rgb[self.sand_grid.grid == 0] = [30, 30, 30]

        self._rgb = rgb

        image = QImage(
            self._rgb.data,
            self.grid_width,
            self.grid_height,
            3 * self.grid_width,
            QImage.Format_RGB888,
        )

        painter.drawImage(self.rect(), image)


class MainWindow(QMainWindow):
    """
    The main window of the application.
    """

    def __init__(self):
        """
        Initializes the main window.
        """
        super().__init__()

        # Initialize window
        self.setWindowTitle("Sand Simulation")
        self.setGeometry(0, 0, 500, 500)

        # Set up the sand widget
        self.sand_widget = SandWidget(50, 50)
        self.setCentralWidget(self.sand_widget)


def main():
    """
    Driver, starts up the application and main window.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
