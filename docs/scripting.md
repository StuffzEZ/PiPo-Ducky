# PiPo Ducky Scripting Language (picods)

The PiPo Ducky uses a custom scripting language called **picods** (PiPo Ducky Script). It's based on DuckyScript with added support for mouse control, LED feedback, and device management.

---

## Quick Start

Create a `.picods` file with this content:

```
#T> My First Script
#D> Opens Notepad and types hello

DELAY 1000
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 1000
STRING Hello World!
```

Save it to the `/scripts` folder on the CIRCUITPY drive, then run it from the web UI.

---

## Metadata

Metadata goes at the top of your script (one tag per line). It's shown in the web UI script chooser.

| Tag | Purpose | Example |
|-----|---------|---------|
| `#T>` | Title | `#T> Rickroll` |
| `#D>` | Description | `#D> Opens a rickroll in the terminal` |
| `#R>` | Requirements (multiline) | `#R> Windows with curl installed` |
| `#N>` | Notes (multiline) | `#N> Harmless prank, no damage` |

```
#T> Rickroll
#D> Rickroll someone via their terminal
#R> Windows computer
#R> Must have curl installed
#N> Completely harmless
#N> Just plays a music video

DELAY 1000
GUI r
...
```

---

## Commands Reference

### Timing

| Command | Syntax | Description |
|---------|--------|-------------|
| `DELAY` | `DELAY 1000` | Pause for N milliseconds |
| `DEFAULT_DELAY` | `DEFAULT_DELAY 500` | Set delay applied after every line |
| `DEFAULTDELAY` | `DEFAULTDELAY 500` | Alias for DEFAULT_DELAY |
| `STRINGDELAY` | `STRINGDELAY 50` | Set delay between each character when typing |
| `STRING_DELAY` | `STRING_DELAY 50` | Alias for STRINGDELAY |
| `REPEAT` | `REPEAT 5` | Repeat the previous line N times |

```
DEFAULT_DELAY 100    # Wait 100ms between every line
DELAY 2000           # Wait 2 seconds
STRING hello         # Type "hello" with no char delay
STRINGDELAY 100      # Now type slowly
STRING world         # Types "world" with 100ms between each letter
REPEAT 3             # Types "world" 3 more times
```

---

### Keyboard

#### Text & Basic Keys

| Command | Description |
|---------|-------------|
| `STRING text` | Types the text string |
| `ENTER` | Press Enter |
| `TAB` | Press Tab |
| `SPACE` | Press Spacebar |
| `BACKSPACE` / `BKSP` | Press Backspace |
| `DELETE` | Press Delete |
| `ESC` / `ESCAPE` | Press Escape |
| `INSERT` | Press Insert |

#### Modifiers

| Command | Description |
|---------|-------------|
| `GUI` / `WINDOWS` | Windows/Command key |
| `CTRL` / `CONTROL` | Control key |
| `ALT` | Alt key |
| `SHIFT` | Shift key |
| `APP` / `MENU` | Context menu key (right-click menu) |

#### Navigation

| Command | Description |
|---------|-------------|
| `UP` / `UPARROW` | Up arrow |
| `DOWN` / `DOWNARROW` | Down arrow |
| `LEFT` / `LEFTARROW` | Left arrow |
| `RIGHT` / `RIGHTARROW` | Right arrow |
| `HOME` | Home key |
| `END` | End key |
| `PAGEUP` | Page Up |
| `PAGEDOWN` | Page Down |

#### Lock Keys

| Command | Description |
|---------|-------------|
| `CAPSLOCK` | Toggle Caps Lock |
| `NUMLOCK` | Toggle Num Lock |
| `SCROLLLOCK` | Toggle Scroll Lock |
| `PRINTSCREEN` | Print Screen |
| `PAUSE` / `BREAK` | Pause/Break |

#### Function Keys

| Command | Description |
|---------|-------------|
| `F1` - `F12` | Function keys F1 through F12 |

#### Letters & Numbers

| Command | Description |
|---------|-------------|
| `A` - `Z` | Letter keys |
| `0` - `9` | Number keys |

#### Symbols

| Command | Description |
|---------|-------------|
| `MINUS` | `-` key |
| `EQUALS` | `=` key |
| `LBRACKET` | `[` key |
| `RBRACKET` | `]` key |
| `BACKSLASH` | `\` key |
| `SEMICOLON` | `;` key |
| `QUOTE` | `'` key |
| `GRAVE` | `` ` `` key (tilde) |
| `COMMA` | `,` key |
| `PERIOD` | `.` key |
| `SLASH` | `/` key |

#### Key Combos

Space-separated keys are pressed simultaneously:

```
GUI r                # Windows+R (Run dialog)
CTRL ALT DELETE      # Ctrl+Alt+Delete
CTRL SHIFT ESC       # Ctrl+Shift+Esc (Task Manager)
CTRL c               # Copy
CTRL v               # Paste
CTRL z               # Undo
ALT F4               # Close window
GUI l                # Lock screen
SHIFT HOME           # Select to start of line
```

---

### Mouse

| Command | Syntax | Description |
|---------|--------|-------------|
| `MOUSE_MOVE` | `MOUSE_MOVE 100 50` | Move relative (x=right, y=down) |
| `MOUSE_CLICK` | `MOUSE_CLICK` | Left click |
| `MOUSE_RIGHTCLICK` | `MOUSE_RIGHTCLICK` | Right click |
| `MOUSE_MIDDLECLICK` | `MOUSE_MIDDLECLICK` | Middle click |
| `MOUSE_SCROLL` | `MOUSE_SCROLL -5` | Scroll wheel (negative=up, positive=down) |
| `MOUSE_DOWN` | `MOUSE_DOWN` | Hold left button (for drag) |
| `MOUSE_UP` | `MOUSE_UP` | Release left button |
| `MOUSE_MOVE_TO` | `MOUSE_MOVE_TO 200 100 20` | Smooth move to position over N steps |

```
# Move mouse in a square
MOUSE_MOVE 100 0
DELAY 200
MOUSE_MOVE 0 100
DELAY 200
MOUSE_MOVE -100 0
DELAY 200
MOUSE_MOVE 0 -100

# Click
MOUSE_CLICK

# Right-click context menu
MOUSE_RIGHTCLICK

# Scroll down 5 notches
MOUSE_SCROLL 5

# Drag and drop
MOUSE_MOVE 100 100
MOUSE_DOWN
MOUSE_MOVE 300 200
MOUSE_UP

# Smooth movement
MOUSE_MOVE_TO 400 300 30
```

**Note:** Mouse coordinates are relative pixels. Positive X = right, Positive Y = down.

---

### Device Control

| Command | Syntax | Description |
|---------|--------|-------------|
| `LED_ON` | `LED_ON` | Turn on the onboard LED |
| `LED_OFF` | `LED_OFF` | Turn off the onboard LED |
| `LED_BLINK` | `LED_BLINK 5 200` | Blink LED N times with delay (ms) |
| `REBOOT` | `REBOOT` | Reboot the Pico W |
| `WAIT_FOR_BUTTON` | `WAIT_FOR_BUTTON` | Pause forever (unplug to stop) |

```
LED_ON                # LED on
LED_BLINK 3 300       # Blink 3 times, 300ms each
LED_OFF               # LED off

REBOOT                # Restart the device
```

---

### Comments

```
REM This is a comment (ignored)
# This is also a comment (ignored)

DELAY 1000  # Inline comment after a command
```

---

## Complete Examples

### Example 1: Open Notepad and Type
```
#T> Notepad Typing
#D> Opens Notepad and types a message
#R> Windows computer

DELAY 1000
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 1000
STRING Hello from PiPo Ducky!
ENTER
STRING This script was written using the picods language.
```

### Example 2: Mouse Demo
```
#T> Mouse Demo
#D> Moves the mouse in patterns
#R> Desktop with mouse

LED_ON
DELAY 500

MOUSE_MOVE 100 0
DELAY 200
MOUSE_MOVE 0 100
DELAY 200
MOUSE_MOVE -100 0
DELAY 200
MOUSE_MOVE 0 -100
DELAY 200

MOUSE_CLICK
DELAY 500
MOUSE_SCROLL -3

LED_OFF
```

### Example 3: Lock Computer
```
#T> Lock Screen
#D> Locks the Windows computer
#R> Windows

DELAY 500
GUI l
```

### Example 4: Open Browser to URL
```
#T> Open Website
#D> Opens a website in the default browser
#R> Windows

DELAY 1000
GUI r
DELAY 500
STRING https://example.com
ENTER
```

### Example 5: LED Status Feedback
```
#T> LED Feedback
#D> Shows LED feedback during script execution

LED_ON
DELAY 200
LED_OFF

GUI r
DELAY 500
STRING notepad
ENTER

LED_BLINK 3 200
```

---

## Tips

1. **Add delays after actions** - Give the computer time to respond (500-1000ms after opening dialogs)
2. **Use LED feedback** - Turn LED on/off to know when script is running
3. **Test small** - Start with simple scripts, build up complexity
4. **Check requirements** - Some scripts need specific OS or software
5. **Use comments** - Document what your scripts do for future reference
