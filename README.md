# 4peirlyk PyVLC Player
Το πρόγραμμα πίσω απο τον «3D Εκτυπωμένος Χάρτης για Προσβασιμότητα στην Πολιτιστική Κληρονομιά των Τρικάλων», του Ομίλου «ΙοΤ & Ρομποτική» του 4ου Πειραματικού ΓΕΛ Τρικάλων.
Γραμμένο σε Python, απο τους μαθητές του Ομίλου, για να τρέχει στα Raspberry Pi.

## Οργάνωση του Project

```bash
.
├── config.toml: Player Configuration
├── requirements.txt: Python Project Requirments
└── src: Source File Directory
    ├── gpio.py: GPIO Related Logic
    ├── gui: GUI Widget Directory
    │   ├── alert.py: Alert Popup
    │   └── vlc.py: VLC Player Logic
    ├── main.py: Entrypoint
    ├── qr.py: QR Code Generation Logic
    └── uri.py: URI Validation Logic
```

## Demo

```mermaid
sequenceDiagram
  participant Display
  participant Script
  participant RPI
  actor User

  Note over Script,RPI: Startup Procedure
  Script ->> Script: Preload Media and Check URL Validity

  Script ->> RPI: Configure GPIO Pins
  Script ->> Script: Register Playable Media and Callbacks

  Script ->> Display: Register PyQT Window and Hook VLC
  Script ->> Display: Play IDLE Media

  Note over Script,RPI: On Button Press Procedure
  User ->> RPI: Press on Button
  RPI -->> Script: Calls Callback
  Script ->> Script: Loads Target From Config
  Script ->> Script: Generate QR Code from Config
  Script ->> Display: Set Media from Preloaded List
  Script ->> Display: Overlay QR Code

  Note over Script,RPI: When Media Playback Finished
  Script ->> Display: Set Media to IDLE
  Script ->> Display: Hide QR Code
```
