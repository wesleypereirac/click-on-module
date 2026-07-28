import subprocess
from time import sleep

subprocess.run([
    "ydotool",
    "mousemove",
    "-x",
    "100",
    "-y",
    "0"
])

sleep(1)