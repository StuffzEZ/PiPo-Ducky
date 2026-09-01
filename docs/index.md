# PiPo Ducky

A powerful WiFi USB Rubber Ducky built on the Raspberry Pi Pico W. Control it wirelessly from any device with a web browser.

---

## What is PiPo Ducky?

PiPo Ducky turns a Raspberry Pi Pico W into a wireless HID device that can:
- **Type text** and press key combinations on the connected computer
- **Control the mouse** with movement, clicks, and scrolling
- **Show a captive portal** to anyone who connects to its WiFi
- **Run scripts** remotely from a web interface

It's like a Bash Bunny, but runs on a $4 Pico W with just a USB cable.

---

## Features

### Keyboard & Mouse HID
The Pico W emulates a USB keyboard and mouse. Send keystrokes, key combos, mouse movements, and clicks to the connected computer.

### Captive Portal
When devices connect to the PiPo_Ducky WiFi, they automatically see a customizable login page (like hotel or airport WiFi). You control what the page shows - a fake login, a real website, or any HTML you want.

### Web Interface
Control everything from your phone or laptop's browser:
- **Scripts Tab** - Write, load, save, and run scripts
- **Portal Tab** - Edit the captive portal HTML
- **Settings Tab** - Control LED, USB storage, device info

### Script Management
- Upload `.picods` scripts from your computer
- Save scripts directly from the web editor
- Load pre-made scripts from the device
- Delete scripts you don't need

### LED Control
Control the onboard LED from scripts or the web UI for visual feedback.

### Storage Bar
See how much space is used on the device at a glance.

### Safety Confirmation
Every script requires confirmation before running, with a warning about what it will do.

---

## How It Works

```
┌──────────────────┐         WiFi AP          ┌──────────────────┐
│   Your Phone/    │ ◄──────────────────────► │    PiPo Ducky    │
│   Laptop         │    192.168.4.1           │    (Pico W)      │
│                  │                           │                  │
│   Web Browser    │   POST /api {script}     │   USB Cable      │
│   opens UI       │ ─────────────────────►   │   to computer    │
│                  │                           │        │         │
└──────────────────┘                           └────────┼────────┘
                                                        │
                                                        ▼
                                                ┌──────────────┐
                                                │  Host PC     │
                                                │  gets keyboard│
                                                │  & mouse input│
                                                └──────────────┘
```

1. Plug the Pico W into a computer via USB
2. The Pico W creates a WiFi access point (`PiPo_Ducky`)
3. Connect to the WiFi from your phone/laptop
4. Open `192.168.4.1` in your browser
5. Write or load a script, click Run
6. The Pico W sends the keyboard/mouse input to the host computer

---

## Installation

### Prerequisites
- Raspberry Pi Pico W
- USB cable
- Computer with a web browser

### Steps

1. **Download CircuitPython**
   Go to [circuitpython.org](https://circuitpython.org) and download the latest CircuitPython `.uf2` file for Pico W.

2. **Flash CircuitPython**
   - Hold the `BOOTSEL` button on the Pico W
   - While holding, plug the USB cable into your computer
   - A drive called `RPI-RP2` will appear
   - Drag the `.uf2` file onto the drive
   - The Pico W will restart automatically

3. **Install PiPo Ducky**
   - A new drive called `CIRCUITPY` will appear
   - Copy all files from the `pico-w` folder to this drive
   - Make sure `code.py`, `duck.py`, `boot.py`, `index.html` are in the root
   - Make sure the `lib` folder is copied with all `.mpy` files inside

4. **Connect**
   - The Pico W will restart and create a WiFi network
   - Connect to `PiPo_Ducky` (password: `ppod_430d`)
   - Open `192.168.4.1` in your browser

5. **Run Scripts**
   - Write a script in the editor, or load one from the library
   - Click **Run** and confirm
   - The script executes on the connected computer

---

## WiFi Credentials

| Setting | Value |
|---------|-------|
| SSID | `PiPo_Ducky` |
| Password | `ppod_430d` |
| IP Address | `192.168.4.1` |

---

## USB Drive Mode

By default, the USB mass storage drive is hidden (stealth mode). To enable it:

1. Connect GP15 to GND on the Pico W (use a jumper wire)
2. Unplug and replug the USB cable
3. The `CIRCUITPY` drive will appear

You can also toggle USB storage from the Settings tab in the web UI.

---

## Script Files

Scripts use the `.picods` file extension. They can be stored in two places:

| Location | Purpose |
|----------|---------|
| `/scripts` on CIRCUITPY drive | On-device scripts, shown in web UI |
| `PiPo-Ducky-scripts/` repo | Community scripts, copy to device |

### Script Format

```
#T> Script Title
#D> Short description
#R> Requirements
#N> Notes

DELAY 1000
GUI r
STRING notepad
ENTER
```

See [Scripting Documentation](scripting.md) for the full command reference.

---

## Web Interface

### Scripts Tab
- **Run** - Execute the script in the editor (requires confirmation)
- **Load** - Browse and load scripts from the device
- **Save** - Save the editor content as a `.picods` file
- **Upload** - Upload a `.picods` file from your computer
- **Help** - Quick reference of all commands

### Portal Tab
Edit the HTML for the captive portal page. This is what people see when they connect to the WiFi. You can put:
- A fake WiFi login page
- A custom HTML page
- A redirect to any website

### Settings Tab
- **LED Control** - Turn the onboard LED on/off or make it blink
- **USB Storage** - Toggle the USB drive visibility
- **Device Info** - Shows WiFi SSID, IP, LED status, script count, storage usage
- **Reboot** - Restart the Pico W

---

## Scripts Library

The `PiPo-Ducky-scripts/` directory contains community-made scripts:

| Script | Description |
|--------|-------------|
| `hello-world.picods` | Opens Notepad and types a greeting |
| `mouse-demo.picods` | Demonstrates mouse movement and clicking |
| `led-blink.picods` | Blinks the LED in a pattern |
| `pipo-alert.picods` | Shows a popup alert |
| `rickroll.picods` | Rickrolls someone via terminal |
| `ctrlpnl.picods` | Opens Control Panel |
| `fake-update.picods` | Shows a fake Windows update screen |
| `fakeshutdown.picods` | Shows a fake shutdown screen |
| `sys-prop.picods` | Opens System Properties |

---

## Contributing Scripts

1. Fork the [PiPo-Ducky-scripts](https://github.com/StuffzEZ/PiPo-Ducky-scripts) repository
2. Create your `.picods` script with metadata (`#T>`, `#D>`, `#R>`, `#N>`)
3. Test it on a real device
4. Submit a Pull Request

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to WiFi | Make sure you're near the Pico W, try forgetting and reconnecting |
| Page won't load | Try `http://192.168.4.1` (not https) |
| Script doesn't work | Add more `DELAY` after actions, check if target software is open |
| LED doesn't blink | Check that `boot.py` is in the root of CIRCUITPY drive |
| USB drive not showing | Connect GP15 to GND, then replug USB |

---

## Credits

- **StuffzEZ** - Original PiPo Ducky project
- **majdsassi** - Pico WiFi Ducky
- CircuitPython, Adafruit HID library

---

## License

GPL v3 - See [LICENSE](LICENSE) for details.
