import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import time
import board
import digitalio
import microcontroller

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

duckyCommands = {
    'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,
    '0': Keycode.ZERO, '1': Keycode.ONE, '2': Keycode.TWO, '3': Keycode.THREE,
    '4': Keycode.FOUR, '5': Keycode.FIVE, '6': Keycode.SIX, '7': Keycode.SEVEN,
    '8': Keycode.EIGHT, '9': Keycode.NINE,
    'MINUS': Keycode.MINUS, 'EQUALS': Keycode.EQUALS,
    'LBRACKET': Keycode.LEFT_BRACKET, 'RBRACKET': Keycode.RIGHT_BRACKET,
    'BACKSLASH': Keycode.BACKSLASH, 'SEMICOLON': Keycode.SEMICOLON,
    'QUOTE': Keycode.QUOTE, 'GRAVE': Keycode.GRAVE_ACCENT,
    'COMMA': Keycode.COMMA, 'PERIOD': Keycode.PERIOD, 'SLASH': Keycode.FORWARD_SLASH,
}

def exe(Payload_Script):
    import usb_hid
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    mouse = Mouse(usb_hid.devices)

    defaultDelay = 0
    stringDelay = 0
    previousLine = ""
    errorCount = 0

    def setLed(state):
        led.value = state

    def blinkLed(count, delay_ms):
        for _ in range(count):
            led.value = True
            time.sleep(delay_ms / 1000)
            led.value = False
            time.sleep(delay_ms / 1000)

    def convertLine(line):
        newline = []
        for key in filter(None, line.split(" ")):
            key = key.upper()
            command_keycode = duckyCommands.get(key, None)
            if command_keycode is not None:
                newline.append(command_keycode)
            elif hasattr(Keycode, key):
                newline.append(getattr(Keycode, key))
            else:
                print(f"Unknown key: <{key}>")
        return newline

    def runScriptLine(line):
        for k in line:
            kbd.press(k)
        kbd.release_all()

    def sendString(line):
        if stringDelay > 0:
            for char in line:
                layout.write(char)
                time.sleep(stringDelay / 1000)
        else:
            layout.write(line)

    def parseLine(line):
        nonlocal defaultDelay, stringDelay, errorCount
        line = line.strip()
        if not line:
            return

        if line.startswith("REM") or line.startswith("#"):
            return

        try:
            if line.startswith("DELAY "):
                time.sleep(float(line[6:]) / 1000)
            elif line.startswith("STRING "):
                sendString(line[7:])
            elif line.startswith("DEFAULT_DELAY "):
                defaultDelay = int(line[14:])
            elif line.startswith("DEFAULTDELAY "):
                defaultDelay = int(line[13:])
            elif line.startswith("STRINGDELAY "):
                stringDelay = int(line[12:])
            elif line.startswith("STRING_DELAY "):
                stringDelay = int(line[13:])
            elif line.startswith("MOUSE_MOVE "):
                parts = line.split()
                x = int(parts[1])
                y = int(parts[2]) if len(parts) > 2 else 0
                mouse.move(x=x, y=y)
            elif line.startswith("MOUSE_CLICK"):
                mouse.click(Mouse.LEFT_BUTTON)
            elif line.startswith("MOUSE_RIGHTCLICK"):
                mouse.click(Mouse.RIGHT_BUTTON)
            elif line.startswith("MOUSE_MIDDLECLICK"):
                mouse.click(Mouse.MIDDLE_BUTTON)
            elif line.startswith("MOUSE_SCROLL "):
                parts = line.split()
                wheel = int(parts[1])
                mouse.move(wheel=wheel)
            elif line.startswith("MOUSE_DOWN"):
                mouse.press(Mouse.LEFT_BUTTON)
            elif line.startswith("MOUSE_UP"):
                mouse.release(Mouse.LEFT_BUTTON)
            elif line.startswith("MOUSE_MOVE_TO "):
                parts = line.split()
                x = int(parts[1])
                y = int(parts[2])
                steps = int(parts[3]) if len(parts) > 3 else 10
                for _ in range(steps):
                    sx = max(-127, min(127, x // steps))
                    sy = max(-127, min(127, y // steps))
                    mouse.move(x=sx, y=sy)
                    time.sleep(0.01)
            elif line.startswith("LED_ON"):
                setLed(True)
            elif line.startswith("LED_OFF"):
                setLed(False)
            elif line.startswith("LED_BLINK"):
                parts = line.split()
                count = int(parts[1]) if len(parts) > 1 else 5
                delay = int(parts[2]) if len(parts) > 2 else 500
                blinkLed(count, delay)
            elif line.startswith("REBOOT"):
                microcontroller.reset()
            elif line.startswith("WAIT_FOR_BUTTON"):
                while True:
                    time.sleep(0.1)
            else:
                newScriptLine = convertLine(line)
                if newScriptLine:
                    runScriptLine(newScriptLine)
        except Exception as e:
            errorCount += 1
            print(f"Error on line: {line} - {e}")

    time.sleep(0.5)

    duckyScript = Payload_Script
    for line in duckyScript:
        line = line.rstrip()
        if line.startswith("REPEAT "):
            count = int(line[7:])
            for _ in range(count):
                parseLine(previousLine)
                time.sleep(defaultDelay / 1000)
        else:
            parseLine(line)
            previousLine = line
        time.sleep(defaultDelay / 1000)

    print("Done")
    return errorCount
