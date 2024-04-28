# Python 3
from PyQt5.QtCore import pyqtSignal, QObject
from pynput.keyboard import Listener as KeyboardListener
from pynput import mouse
from Model.InputEvent import KeystrokeEvent, MouseMoveEvent, MouseClickEvent, MouseScrollEvent
from Model.Point import Point


# Docs:
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://pynput.readthedocs.io/en/latest/mouse.html

# Records keyboard strokes
class KeyboardEventMonitor(QObject):
    listener: KeyboardListener = None
    is_running = False
    
    on_press_callback = None
    on_release_callback = None
    print_callback = None
    
    signal_main = pyqtSignal(KeystrokeEvent, name='emit_event_on_main')
    
    def __init__(self):
        super(KeyboardEventMonitor, self).__init__()
        self.signal_main.connect(self.emit_event_on_main)
    
    def setup(self, on_press_callback, on_release_callback):
        self.reset()
        self.on_press_callback = on_press_callback
        self.on_release_callback = on_release_callback
    
    def start(self):
        assert self.listener is not None
        assert not self.is_running
        
        self.print("EventMonitor start")
        
        self.is_running = True
        
        self.listener.start()
    
    def stop(self):
        assert self.is_running
        
        self.print("stop")
        
        self.is_running = False
        self.listener.stop()
        self.listener = None
    
    def reset(self):
        assert not self.is_running
        
        self.print("reset monitor")
        self.is_running = False
        
        if self.listener is not None:
            self.listener.stop()
        
        self.listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
    
    def join(self):
        assert self.is_running

        self.print("join")
        
        self.listener.wait()
        self.listener.join()
    
    def on_press(self, key):
        if not self.is_running: return False
        self.print(f"{key} pressed")
        
        self.signal_main.emit(KeystrokeEvent(True, key))
        
        return self.is_running
    
    def on_release(self, key):
        if not self.is_running: return False
        self.print(f"{key} released")
        
        self.signal_main.emit(KeystrokeEvent(False, key))
        
        return self.is_running
    
    def emit_event_on_main(self, value):
        if value.is_pressed:
            self.on_press_callback(value)
        else:
            self.on_release_callback(value)
    
    def print(self, string):
        if self.print_callback is not None:
            self.print_callback(string)

# Record mouse movement
class MouseEventMonitor(QObject):
    listener: mouse.Listener = None
    is_running = False
    
    on_move_callback = None
    on_press_callback = None
    on_release_callback = None
    on_scroll_callback = None
    print_callback = None
    
    signal_main_move = pyqtSignal(MouseMoveEvent, name='emit_event_on_main_move')
    signal_main_click = pyqtSignal(MouseClickEvent, name='emit_event_on_main_click')
    signal_main_scroll = pyqtSignal(MouseScrollEvent, name='emit_event_on_main_scroll')
    
    def __init__(self):
        super(MouseEventMonitor, self).__init__()
        self.signal_main_move.connect(self.emit_event_on_main_move)
        self.signal_main_click.connect(self.emit_event_on_main_click)
        self.signal_main_scroll.connect(self.emit_event_on_main_scroll)
    
    def setup(self, on_move_callback, on_press_callback, on_release_callback, on_scroll_callback):
        self.reset()
        self.on_move_callback = on_move_callback
        self.on_press_callback = on_press_callback
        self.on_release_callback = on_release_callback
        self.on_scroll_callback = on_scroll_callback
    
    def start(self):
        assert self.listener is not None
        assert not self.is_running

        self.print("start")

        self.is_running = True

        self.listener.start()
    
    def stop(self):
        assert self.is_running
        
        self.print("stop")
        
        self.is_running = False
        self.listener.stop()
        self.listener = None

    def join(self):
        assert self.is_running
        
        self.print("join")
        
        self.listener.wait()
        self.listener.join()
    
    def on_move(self, x, y) -> bool:
        if not self.is_running: return False
        self.print(f"({x}, {y}) moved")
        
        self.signal_main_move.emit(MouseMoveEvent(Point(x, y)))
        
        return self.is_running
    
    def on_click(self, x, y, key, is_pressed) -> bool:
        if not self.is_running: return False
        self.print(f"{key} {'pressed' if is_pressed else 'released'}")
        
        self.signal_main_click.emit(MouseClickEvent(is_pressed, key, Point(x, y)))
        
        return self.is_running
    
    def on_scroll(self, x, y, dx, dy) -> bool:
        if not self.is_running: return False
        self.print(f"scrolled by ({x}, {y}) by ({dx}, {dy})")
        
        self.signal_main_scroll.emit(MouseScrollEvent(Point(x, y), Point(dx, dy)))
        
        return self.is_running
    
    def reset(self):
        assert not self.is_running
        
        self.print("reset monitor")
        
        self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
    
    def emit_event_on_main_move(self, event):
        self.on_move_callback(event)
    
    def emit_event_on_main_click(self, event):
        if event.is_pressed:
            self.on_press_callback(event)
        else:
            self.on_release_callback(event)
    
    def emit_event_on_main_scroll(self, event):
        self.on_scroll_callback(event)
    
    def print(self, string):
        if self.print_callback is not None:
            self.print_callback(string)

