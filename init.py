import metadata
import subprocess
import postkrnl_conf
import shlex
import os
import sys
import bsod

print(f"Hello EagletOS version {metadata.EAGLETOS_VERSION}")
os.chdir(os.path.dirname(__file__))

print("Setting up environment variables...")
def parse_kernel_args(args):
    variables = {}

    for arg in shlex.split(args):
        if "=" in arg:
            key, value = arg.split("=", 1)
        else:
            key, value = arg, "1"

        variables[key.upper()] = value

    return variables
cmdline = open("/proc/cmdline")
os.environ.update(parse_kernel_args(str(cmdline.read())))
cmdline.close()
os.environ.update(postkrnl_conf.ENVIRON_VARIABLES)

if os.environ.get("splash"):
    pass

print("Launching userland compartments...")
division_subp = []
for division in postkrnl_conf.DIVISIONS:
    print(f"Spawning {division}")
    try:
        division_subp.append(subprocess.Popen([sys.executable, f"{division}.py"]))
    except OSError:
        bsod.file_bsod("devinit_exit.md", {
            "COMPARTMENT": division,
            "EXIT_CODE": -32768
        })

while True:
    for division in division_subp:
        if division.poll() is not None:
            bsod.file_bsod("devinit_exit.md", {
                "COMPARTMENT": division.args[1],
                "EXIT_CODE": division.returncode
            })