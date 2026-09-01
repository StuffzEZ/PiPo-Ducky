import board
import digitalio
import storage
import usb_hid

# Use GP15 to control USB visibility
usb_control_pin = digitalio.DigitalInOut(board.GP15)
usb_control_pin.switch_to_input(pull=digitalio.Pull.UP)

# Enable USB HID keyboard and mouse
usb_hid.enable(
    (usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE),
)

if usb_control_pin.value:
    storage.disable_usb_drive()
    print("USB drive is hidden (web mode)")
else:
    print("USB drive is enabled (development mode)")
