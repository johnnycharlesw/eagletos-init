import metadata
import subprocess
import postkrnl_conf
import shlex
import os
import sys
import bsod
import traceback

def main():
    print(f"Hello EagletOS version {metadata.EAGLETOS_VERSION}")

    print("Setting up environment variables...")
    os.chdir("/")
    print(os.getcwd())
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

        bsod2 = os.environ.get("bsod")
        if bsod2 != None:
            bsod.file_bsod("devinit_exit.md", {
                "COMPARTMENT": division,
                "EXIT_CODE": -32768
            })
        
        try:
            division_subp.append(subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), f"{division}", "__main__.py")]))
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

# Monitor components
try:
    main()
except BaseException as e:
    bsod.file_bsod("init_exception.md", {
        "EXCEPTION_TYPE": type(e).__name__,
        "PYTHON_TRACEBACK": str(traceback.format_exc())
    })