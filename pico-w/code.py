import os
import socketpool
import wifi
import storage
import microcontroller
import board
import digitalio
from duck import exe
from adafruit_httpserver import Server, Request, JSONResponse, POST, Response, GET

ssid = "PiPo_Ducky"
password = "ppod_430d"

print("Creating access point", ssid)
wifi.radio.stop_station()
wifi.radio.start_ap(ssid, password)
print("Access point created!")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

usb_enabled = True
led_pin = digitalio.DigitalInOut(board.LED)
led_pin.direction = digitalio.Direction.OUTPUT

PORTAL_FILE = "/portal/index.html"
DEFAULT_PORTAL = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free WiFi</title>
<style>
body{font-family:Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.card{background:white;padding:40px;border-radius:12px;box-shadow:0 2px 20px rgba(0,0,0,0.1);text-align:center;max-width:400px;width:90%}
h1{color:#1a73e8;margin-bottom:10px}
p{color:#5f6368;margin-bottom:20px}
input{width:100%;padding:12px;border:1px solid #dadce0;border-radius:6px;box-sizing:border-box;margin-bottom:12px;font-size:16px}
button{width:100%;padding:12px;background:#1a73e8;color:white;border:none;border-radius:6px;font-size:16px;cursor:pointer}
button:hover{background:#1557b0}
</style>
</head>
<body>
<div class="card">
<h1>Free WiFi</h1>
<p>Enter your details to connect</p>
<input type="email" placeholder="Email address">
<button onclick="alert('Connected!')">Connect</button>
</div>
</body>
</html>"""

def get_portal_content():
    try:
        with open(PORTAL_FILE, "r") as f:
            return f.read()
    except:
        return DEFAULT_PORTAL

def save_portal_content(content):
    try:
        os.mkdir("/portal")
    except:
        pass
    with open(PORTAL_FILE, "w") as f:
        f.write(content)

def get_storage_info():
    total = 1966080
    used = 0
    try:
        for item in os.listdir("/"):
            try:
                s = os.stat("/" + item)
                used += s[6]
            except:
                pass
        for d in ["/scripts", "/portal", "/lib"]:
            try:
                for item in os.listdir(d):
                    try:
                        s = os.stat(d + "/" + item)
                        used += s[6]
                    except:
                        pass
            except:
                pass
    except:
        pass
    return {"total": total, "used": used, "free": total - used}

# Main admin UI
@server.route("/")
def base(request: Request):
    with open("index.html", "r") as file:
        html_content = file.read()
    return Response(request, html_content, headers={"Content-Type": "text/html"})

# Execute script
@server.route("/api", POST, append_slash=True)
def api(request: Request):
    req = request.json()
    payload = req["content"]
    payload = payload.splitlines()
    errors = exe(payload)
    return JSONResponse(request, {"message": "Done", "errors": errors})

# List scripts
@server.route("/scripts", GET)
def list_scripts(request: Request):
    try:
        files = [f for f in os.listdir("/scripts") if f.endswith(".picods")]
        return JSONResponse(request, {"scripts": files})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

# Get script content
@server.route("/scripts/<filename>", GET)
def get_script(request: Request, filename: str):
    try:
        if ".." in filename or not filename.endswith(".picods"):
            return JSONResponse(request, {"error": "Invalid filename"}, status=400)
        with open(f"/scripts/{filename}", "r") as file:
            content = file.read()
        return Response(request, content, headers={"Content-Type": "text/plain"})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

# Upload script
@server.route("/upload", POST)
def upload_script(request: Request):
    try:
        data = request.json()
        filename = data.get("filename", "")
        content = data.get("content", "")
        if not filename.endswith(".picods"):
            return JSONResponse(request, {"error": "Must be .picods file"}, status=400)
        if ".." in filename or "/" in filename:
            return JSONResponse(request, {"error": "Invalid filename"}, status=400)
        with open(f"/scripts/{filename}", "w") as f:
            f.write(content)
        return JSONResponse(request, {"message": "Script uploaded"})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

# Delete script
@server.route("/delete", POST)
def delete_script(request: Request):
    try:
        data = request.json()
        filename = data.get("filename", "")
        if not filename.endswith(".picods"):
            return JSONResponse(request, {"error": "Invalid filename"}, status=400)
        if ".." in filename or "/" in filename:
            return JSONResponse(request, {"error": "Invalid filename"}, status=400)
        os.remove(f"/scripts/{filename}")
        return JSONResponse(request, {"message": "Script deleted"})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

# Toggle USB storage
@server.route("/toggle_usb", POST)
def toggle_usb(request: Request):
    global usb_enabled
    try:
        if usb_enabled:
            storage.disable_usb_drive()
            usb_enabled = False
            return JSONResponse(request, {"status": "disabled"})
        else:
            storage.enable_usb_drive()
            usb_enabled = True
            return JSONResponse(request, {"status": "enabled"})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

# Storage info
@server.route("/storage", GET)
def storage_info(request: Request):
    return JSONResponse(request, get_storage_info())

# LED control
@server.route("/led", POST)
def led_control(request: Request):
    try:
        data = request.json()
        action = data.get("action", "")
        if action == "on":
            led_pin.value = True
            return JSONResponse(request, {"status": "on"})
        elif action == "off":
            led_pin.value = False
            return JSONResponse(request, {"status": "off"})
        elif action == "blink":
            count = data.get("count", 5)
            delay = data.get("delay", 200)
            for _ in range(count):
                led_pin.value = True
                import time
                time.sleep(delay / 1000)
                led_pin.value = False
                time.sleep(delay / 1000)
            return JSONResponse(request, {"status": "blinked"})
        return JSONResponse(request, {"error": "Invalid action"}, status=400)
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

# Get portal page
@server.route("/api/portal", GET)
def get_portal(request: Request):
    content = get_portal_content()
    return JSONResponse(request, {"content": content})

# Set portal page
@server.route("/api/portal", POST)
def set_portal(request: Request):
    try:
        data = request.json()
        content = data.get("content", "")
        save_portal_content(content)
        return JSONResponse(request, {"message": "Portal updated"})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

# Device status
@server.route("/status", GET)
def device_status(request: Request):
    storage_info = get_storage_info()
    try:
        files = [f for f in os.listdir("/scripts") if f.endswith(".picods")]
        script_count = len(files)
    except:
        script_count = 0
    return JSONResponse(request, {
        "led": led_pin.value,
        "usb": usb_enabled,
        "storage": storage_info,
        "scripts": script_count,
        "ssid": ssid,
        "ip": "192.168.4.1"
    })

# Reboot
@server.route("/reboot", POST)
def reboot(request: Request):
    microcontroller.reset()

# Captive portal probe responses
def serve_portal(request: Request):
    content = get_portal_content()
    return Response(request, content, headers={"Content-Type": "text/html"})

@server.route("/hotspot-detect.html", GET)
def ios_probe(request: Request):
    return serve_portal(request)

@server.route("/generate_204", GET)
def android_probe(request: Request):
    return serve_portal(request)

@server.route("/connecttest.txt", GET)
def windows_probe(request: Request):
    return serve_portal(request)

@server.route("/ncsi.txt", GET)
def windows_probe2(request: Request):
    return serve_portal(request)

@server.route("/success.txt", GET)
def firefox_probe(request: Request):
    return serve_portal(request)

@server.route("/redirect", GET)
def redirect_probe(request: Request):
    return serve_portal(request)

@server.route("/canonical.html", GET)
def chrome_probe(request: Request):
    return serve_portal(request)

# Portal page direct access
@server.route("/portal", GET)
def portal_page(request: Request):
    return serve_portal(request)

print("Starting server...")
server.serve_forever("192.168.4.1", 80)
