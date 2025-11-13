
# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar
from PySide6.QtGui import QAction
from src.drawing.canvas import PatternCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PatternCAD - Estilo Audaces")
        self.setGeometry(100, 100, 1000, 700)

        self.canvas = PatternCanvas()
        self.setCentralWidget(self.canvas)

        self.init_toolbar()

    def init_toolbar(self):
        toolbar = QToolBar("Herramientas")
        self.addToolBar(toolbar)

        line_action = QAction("Linea", self)
        line_action.setCheckable(True)
        line_action.triggered.connect(lambda checked: self.canvas.set_mode("line" if checked else None))
        toolbar.addAction(line_action)

        curve_action = QAction("Curva", self)
        curve_action.setCheckable(True)
        curve_action.triggered.connect(lambda checked: self.canvas.set_mode("curve" if checked else None))
        toolbar.addAction(curve_action)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

