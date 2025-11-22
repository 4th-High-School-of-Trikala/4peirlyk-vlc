from PyQt5.QtCore import QObject, pyqtSignal
import RPi.GPIO

# GPIO Signals for communicating with Qt
class GPIOSignals(QObject):
    gpioTriggerVideo = pyqtSignal(str)

    def __init__(self, config):
        QObject.__init__(self)
        self.config = config

    def trigger_video(self, gpio):
        print(f"GPIO {gpio} was pressed")
        self.gpioTriggerVideo.emit(self.config["GPIO"][str(gpio)]["Target"])

def register_gpio_pins(config, signal: GPIOSignals):
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    for gpio in config["GPIO"]:
        RPi.GPIO.setup(int(gpio), RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        RPi.GPIO.add_event_detect(int(gpio), RPi.GPIO.FALLING, bouncetime=600)
        RPi.GPIO.add_event_callback(int(gpio), signal.trigger_video)
        print(f"[gpio.py] Added GPIO Callback for GPIO{gpio}")
