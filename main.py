import sys
from PyQt5.QtCore import QPoint, QRect, QTimer
from PyQt5.QtGui import QImage, QPainter, qRgb
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class SandGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        # spawn line at top
        for x in range(width):
            self.grid[0][x] = 1

    def update_grid(self):
        for y in range(self.height - 2, -1, -1):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    self.update_pixel(x, y)

    def update_pixel(self, x, y):
        if y + 1 < self.height and self.grid[y + 1][x] == 0:
            self.grid[y][x] = 0
            self.grid[y + 1][x] = 1

        elif x > 0 and y + 1 < self.height and self.grid[y + 1][x - 1] == 0:
            self.grid[y][x] = 0
            self.grid[y + 1][x - 1] = 1

        elif (
            x < self.width - 1 and y + 1 < self.height and self.grid[y + 1][x + 1] == 0
        ):
            self.grid[y][x] = 0
            self.grid[y + 1][x + 1] = 1


class SandWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.sand_grid = SandGrid(width, height)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def tick(self):
        self.sand_grid.update_grid()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        image = QImage(self.width, self.sand_grid.height, QImage.Format_RGB32)

        for y in range(self.height):
            for x in range(self.width):
                if self.sand_grid.grid[y][x] == 1:
                    image.setPixel(x, y, qRgb(189, 149, 3))
                else:
                    image.setPixel(x, y, qRgb(30, 30, 30))

        painter.drawImage(self.rect(), image)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize window
        self.setWindowTitle("Sand Simulation")
        self.setGeometry(0, 0, 2000, 2000)

        # Set up the sand widget
        self.sand_widget = SandWidget(500, 500)
        self.setCentralWidget(self.sand_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
