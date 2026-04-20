import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class SandWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setToolTip("Hi there")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize window
        self.setWindowTitle("Sand Simulation")
        self.setGeometry(0, 0, 500, 500)

        # Set up the sand widget
        self.sand_widget = SandWidget()
        self.setCentralWidget(self.sand_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
