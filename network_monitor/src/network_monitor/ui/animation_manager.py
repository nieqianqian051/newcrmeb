from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QTableWidgetItem
from PyQt6.QtGui import QColor

class AnimationManager:
    """Manages UI animations for the network monitor application"""
    
    def __init__(self):
        self._animations = {}  # Store active animations
        
    def fade_in(self, widget: QWidget, duration: int = 500) -> None:
        """
        Fade in a widget smoothly
        
        Args:
            widget: The widget to animate
            duration: Animation duration in milliseconds
        """
        if not widget:
            return
            
        if widget in self._animations:
            self._animations[widget].stop()
            
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._animations[widget] = animation
        animation.start()
        
        # Cleanup after animation
        animation.finished.connect(lambda: self._cleanup_animation(widget))
        
    def flash_status(self, widget: QWidget, color: QColor, duration: int = 1000) -> None:
        """
        Flash a widget's background color to indicate status change
        
        Args:
            widget: The widget to animate
            color: The color to flash
            duration: Animation duration in milliseconds
        """
        if not widget:
            return
            
        if widget in self._animations:
            self._animations[widget].stop()
            
        if isinstance(widget, QTableWidgetItem):
            original_background = widget.background()
            widget.setBackground(color)
            QTimer.singleShot(duration, lambda: widget.setBackground(original_background))
        else:
            original_style = widget.styleSheet()
            widget.setStyleSheet(f"background-color: {color.name()};")
            QTimer.singleShot(duration, lambda: widget.setStyleSheet(original_style))
        
    def slide_in(self, widget: QWidget, direction: str = 'right', duration: int = 500) -> None:
        """
        Slide in a widget from a direction
        
        Args:
            widget: The widget to animate
            direction: The direction to slide from ('right', 'left', 'up', 'down')
            duration: Animation duration in milliseconds
        """
        if not widget:
            return
            
        if widget in self._animations:
            self._animations[widget].stop()
            
        pos = widget.pos()
        size = widget.size()
        
        # Set start position based on direction
        if direction == 'right':
            widget.move(pos.x() + size.width(), pos.y())
        elif direction == 'left':
            widget.move(pos.x() - size.width(), pos.y())
        elif direction == 'up':
            widget.move(pos.x(), pos.y() - size.height())
        elif direction == 'down':
            widget.move(pos.x(), pos.y() + size.height())
            
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setEndValue(pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._animations[widget] = animation
        animation.start()
        
        # Cleanup after animation
        animation.finished.connect(lambda: self._cleanup_animation(widget))
        
    def _cleanup_animation(self, widget: QWidget) -> None:
        """
        Clean up completed animations
        
        Args:
            widget: The widget whose animation has completed
        """
        if widget in self._animations:
            del self._animations[widget]
