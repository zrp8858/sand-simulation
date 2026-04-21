import sys
import numpy as np
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class SandGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)

    def update_grid(self):
        for y in range(self.height - 2, -1, -1):
            for x in range(self.width):
                if self.grid[y, x] == 1:
                    self.update_pixel(x, y)

    def update_pixel(self, x, y):
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
    def __init__(self, width, height):
        super().__init__()
        self.cell_size = 10
        self.grid_width = width
        self.grid_height = height
        self.setFixedSize(
            self.grid_width * self.cell_size,
            self.grid_height * self.cell_size
        )
        self.sand_grid = SandGrid(width, height)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def tick(self):
        self.sand_grid.update_grid()
        self.update()

    def add_sand(self, event):
        x = event.x() // self.cell_size
        y = event.y() // self.cell_size

        if 0 <= x < self.sand_grid.width and 0 <= y < self.sand_grid.height:
            self.sand_grid.grid[y, x] = 1

    def mousePressEvent(self, event):
        self.add_sand(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.add_sand(event)

    def paintEvent(self, event):
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
            QImage.Format_RGB888
        )

        painter.drawImage(self.rect(), image)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize window
        self.setWindowTitle("Sand Simulation")
        self.setGeometry(0, 0, 500, 500)

        # Set up the sand widget
        self.sand_widget = SandWidget(50, 50)
        self.setCentralWidget(self.sand_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
