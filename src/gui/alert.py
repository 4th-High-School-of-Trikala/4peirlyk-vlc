from PyQt5.QtWidgets import QMessageBox

def show_alert(msg, config):
    QMessageBox.critical(None, f'{config["Window"]["Title"]} - Alert', msg, QMessageBox.StandardButton.Ok)
