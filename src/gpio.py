from PyQt5.QtCore import QObject, pyqtSignal

# GPIO Signals for communicating with Qt
class GPIOSignals(QObject):
    gpioTriggered = pyqtSignal(int)

    def trigger_gpio(self, gpio):
        self.gpioTriggered.emit(gpio)