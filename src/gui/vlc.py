from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMacCocoaViewContainer, QFrame, QSlider
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QTimer

import vlc, gpio
import platform
import os

class PlayerWindow(QMainWindow):
    def __init__(self, config, gpio: gpio.GPIOSignals):
        QMainWindow.__init__(self, None)
        self.setWindowTitle(config["Window"]["Title"])
        
        # Init
        self.config = config
        self.media = None

        # VLC Player
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.player.audio_set_volume(config["Videos"]["Volume"])

        # Connect GPIO Input
        gpio.gpioTriggered.connect(self.handle_gpio_trigger)

        self.init_ui()
        self.set_idle_video()
        self.update_progress_timer.start()
    
    def init_ui(self):
        # Create Widget
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # Create Videoframe
        if platform.system() == "Darwin":
            self.frame = QMacCocoaViewContainer(0)
        else:
            self.frame = QFrame()

        # Set Frame Background
        self.palette = self.frame.palette()
        self.palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.frame.setPalette(self.palette)
        self.frame.setAutoFillBackground(True)

        # Progress Slider
        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setMaximum(1000)

        # Create Layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.frame)
        self.vbox.addWidget(self.progress)
        self.widget.setLayout(self.vbox)

        self.update_progress_timer = QTimer()
        self.update_progress_timer.setInterval(100)
        self.update_progress_timer.timeout.connect(self.update_progress)
    
    def update_progress(self):
        pos = int(self.player.get_position() * 1000)
        self.progress.setValue(pos)

        # If Video is not playing, set idle video
        if not self.player.is_playing():
            self.set_idle_video()

    # Set Idle Video
    def set_idle_video(self):
        src = self.config["Videos"]["Idle"]["Source"]
        self.play_file(src)

    # Handle GPIO Trigger
    def handle_gpio_trigger(self, gpio):
        print(f"GPIO Triggered: {gpio}")

        src = self.config["Videos"][f"GPIO{gpio}"]["Source"]
        self.play_file(src)

    # Load and Play File
    def play_file(self, file):
        self.load_file(file) # Load File
        self.player.play() # Start Player

    # Load File
    def load_file(self, file):
        self.media = self.vlcInstance.media_new(file)
        self.player.set_media(self.media)
        self.media.parse()

        if platform.system() == "Linux": # for Linux using the X Server
            self.player.set_xwindow(int(self.frame.winId()))
        elif platform.system() == "Windows": # for Windows
            self.player.set_hwnd(int(self.frame.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.player.set_nsobject(int(self.frame.winId()))