from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QSlider, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint

import vlc, gpio, uri
import platform
import os
import time
import qr, qrcode

class PlayerWindow(QMainWindow):
    def __init__(self, config, gpio: gpio.GPIOSignals):
        QMainWindow.__init__(self, None)
        self.setWindowTitle(config["Window"]["Title"])
        
        # Init
        self.config = config
        self.media = None
        self.loading = False

        # VLC Player
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.player.audio_set_volume(config["Player"]["Volume"])

        # Connect GPIO Input
        gpio.gpioTriggerVideo.connect(self.handle_gpio_trigger)
        
        # Preload Videos
        self.mediaList = uri.preload_uris(self.config, self.vlcInstance)

        self.init_ui()
        self.set_idle_video()
        self.update_progress_timer.start()
    
    def init_ui(self):
        # Create Widget
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # Create Videoframe
        #��if platform.system() == "Darwin":
         #   self.frame = QMacCocoaViewContainer(0)
        #else:
        self.frame = QFrame()

        # Set Frame Background
        self.palette = self.frame.palette()
        self.palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.frame.setPalette(self.palette)
        self.frame.setAutoFillBackground(True)

        # Progress Slider
        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setMaximum(1000)

        # QR Code
        self.qr = QLabel(self)
        
        # Create Layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.frame)
        
        if self.config["Player"]["ProgressBar"]:
            self.vbox.addWidget(self.progress)
        
        self.widget.setLayout(self.vbox)

        self.update_progress_timer = QTimer()
        self.update_progress_timer.setInterval(100)
        self.update_progress_timer.timeout.connect(self.update_progress)
    
    def update_progress(self):
        pos = int(self.player.get_position() * 1000)
        
        if (pos > 0):
            self.loading = False
        
        self.progress.setValue(pos)

        # If Video is not playing, set idle video
        if not self.player.is_playing() and not self.loading:
            self.set_idle_video()

    # Set Idle Video
    def set_idle_video(self):
        print("SETIDLE")
        self.play("Idle")

    # Handle GPIO Trigger
    def handle_gpio_trigger(self, name):
        self.loading = True
        self.update_progress_timer.stop()
        print(f"GPIO Play Video Triggered: {name}")
        self.play(name)

    # Load and Play
    def play(self, name):
        self.load(name) # Load File
        self.player.play() # Start Player

        self.update_progress_timer.start()

    # Load File
    def load(self, name):
        # Load QR
        qrText = self.config["Videos"][name]["Qr"]
        qrBoxSize = self.config["Player"]["QrBoxSize"]
        qrBorderSize = self.config["Player"]["QrBorderSize"]
        qr_factory = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=qrBoxSize, border=qrBorderSize, image_factory = qr.QrImage)
        qr_factory.add_data(qrText)
        qr_factory.make(fit=True)
        qrPixmap = qr_factory.make_image().pixmap()
        
        self.qr.setPixmap(qrPixmap)
        self.qr.resize(qrPixmap.width(), qrPixmap.height())
        
        # Load Video
        self.load_media(name)

        self.player.set_xwindow(int(self.frame.winId()))
        if platform.system() == "Linux": # for Linux using the X Server
            pass
        elif platform.system() == "Windows": # for Windows
            self.player.set_hwnd(int(self.frame.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.player.set_nsobject(int(self.frame.winId()))
    
    def load_media(self, name):
        self.media = self.mediaList[name]
        self.player.set_media(self.media)
