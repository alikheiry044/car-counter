import os
import urllib.request

URL = ("https://raw.githubusercontent.com/MicrocontrollersAndMore/"
       "OpenCV_3_Car_Counting_Cpp/master/CarsDrivingUnderBridge.mp4")
PATH = "video/traffic.mp4"

os.makedirs("video", exist_ok=True)

with urllib.request.urlopen(URL, timeout=60) as r:
    total = int(r.headers.get("Content-Length", 0))
    print("Expected size (MB):", total / 1e6)
    with open(PATH, "wb") as f:
        while True:
            chunk = r.read(1024 * 256)
            if not chunk:
                break
            f.write(chunk)

got = os.path.getsize(PATH)
print("Downloaded (MB):", got / 1e6)
print("Complete:", total == 0 or got == total)