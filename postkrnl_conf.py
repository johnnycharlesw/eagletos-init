import os
LOCALE = "en_US"

def genpathvar(paths):
    return os.pathsep.join(paths)

DIVISIONS = ["devinit", "sysinit"]
ENVIRON_VARIABLES={
    "AGECHECK": "0",
    "EAGLETOS_RUNLEVEL": "4",
    "PATH": genpathvar([
        "/usr/local/bin",
        "/usr/bin",
        "/bin",
        "/usr/local/sbin",
        "/usr/sbin",
        "/sbin",
        "/usr/local/games",
        "/usr/games",
        "/apps/binfarm"
    ]),
    "SHELL": "/usr/bin/pysh",
    "PWD": os.getcwd(),
    "LANG": LOCALE+".UTF-8"
}