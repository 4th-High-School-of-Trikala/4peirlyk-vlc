import toml
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

import gui
import gui.vlc
from gpio import GPIOSignals, register_gpio_pins
import uri
import qrcode

app = QApplication([])

# Configure App
config = toml.load("./config.toml")
uri.check_valid_config_uris(config)

# GPIO
gpio = GPIOSignals(config)
register_gpio_pins(config, gpio)

# Create Player
player = gui.vlc.PlayerWindow(config, gpio)

# Show Window
if config["Window"]["Fullscreen"]:
    player.showFullScreen()
else:
    player.show()
    player.resize(640, 480)

# Run App
app.exec()
