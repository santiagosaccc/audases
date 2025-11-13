
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsPathItem, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QColor, QMouseEvent, QPainter, QPainterPath
from PySide6.QtCore import Qt, QPointF, QEvent

class ControlPoint(QGraphicsEllipseItem):
    def __init__(self, x, y, radius=6):
        super().__init__(x - radius/2, y - radius/2, radius, radius)
        self.setBrush(QColor("#e74c3c"))
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable | QGraphicsEllipseItem.ItemSendsGeometryChanges)
        self.setZValue(1)

class PatternCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor("#f0f0f0"))
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.pen = QPen(QColor("#2c3e50"), 1.5)
        self.mode = None
        self.points = []
        self.preview_path = None
        self.curve_item = None

        self.scene().installEventFilter(self)

    def set_mode(self, mode):
        self.mode = mode
        self.points.clear()
        if self.preview_path:
            self.scene().removeItem(self.preview_path)
            self.preview_path = None
        if self.curve_item:
            self.scene().removeItem(self.curve_item)
            self.curve_item = None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            pos = self.mapToScene(event.pos())
            if self.mode == "curve":
                dot = ControlPoint(pos.x(), pos.y())
                self.scene().addItem(dot)
                self.points.append(dot)

                if len(self.points) == 3:
                    self.update_curve()

            elif self.mode == "line":
                self.points = [pos]
                self.preview_path = QGraphicsLineItem()
                self.preview_path.setPen(self.pen)
                self.scene().addItem(self.preview_path)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.mode == "line" and self.points:
            end = self.mapToScene(event.pos())
            self.preview_path.setLine(self.points[0].x(), self.points[0].y(), end.x(), end.y())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.mode == "line" and self.points:
            end = self.mapToScene(event.pos())
            final_line = QGraphicsLineItem(self.points[0].x(), self.points[0].y(), end.x(), end.y())
            final_line.setPen(self.pen)
            self.scene().addItem(final_line)
            self.scene().removeItem(self.preview_path)
            self.preview_path = None
            self.points.clear()

    def update_curve(self):
        print("Actualizando curva...")
        if self.mode == "curve" and len(self.points) == 3:
            path = QPainterPath()
            path.moveTo(self.points[0].scenePos())
            path.cubicTo(self.points[1].scenePos(), self.points[1].scenePos(), self.points[2].scenePos())
            if self.curve_item:
                self.scene().removeItem(self.curve_item)
            self.curve_item = QGraphicsPathItem(path)
            self.curve_item.setPen(self.pen)
            self.scene().addItem(self.curve_item)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.GraphicsSceneMouseMove and self.mode == "curve":
            self.update_curve()
        return False

