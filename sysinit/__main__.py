import metadata
import subprocess
import shlex
import os
import time


print(f"Hello {metadata.EAGLETOS_NAME} version {metadata.EAGLETOS_VERSION}")

while True:
    print("sysinit")
    time.sleep(500)