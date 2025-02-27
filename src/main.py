import toml
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

import gui
import gui.vlc
from gpio import GPIOSignals
import uri

app = QApplication([])

# Configure App
config = toml.load("./config.toml")
uri.check_valid_config_uris(config)

# GPIO
gpio = GPIOSignals()

# Create Player
player = gui.vlc.PlayerWindow(config, gpio)

# Trigger Fake GPIO
gpio.trigger_gpio(1)

# Show Window
if config["Window"]["Fullscreen"]:
    player.showFullScreen()
else:
    player.show()
    player.resize(640, 480)

# Run App
app.exec()