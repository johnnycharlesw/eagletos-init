import metadata
import subprocess
import postkrnl_conf
import shlex
import os
import bsod


print(f"Hello EagletOS version {metadata.EAGLETOS_VERSION}")

print("Setting up environment variables...")
os.environ.update(postkrnl_conf.ENVIRON_VARIABLES)

print("Launching userland compartments...")
division_subp = []
for division in postkrnl_conf.DIVISIONS:
    print(f"Spawning {division}")
    try:
        division_subp.append(subprocess.Popen(shlex.split(f"python3 {division}.py")))
    except OSError:
        bsod.bsod(f"Could not spawn division {division}")

while True:
    for division in division_subp:
        if division.poll() is not None:
            bsod.bsod("A process exited!")