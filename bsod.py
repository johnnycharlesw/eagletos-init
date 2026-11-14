import shutil
import time
import re
import os
import metadata

def parse_template(template, variables):
    def replace(match):
        name = match.group(1)
        return str(variables.get(name, match.group(0)))

    return re.sub(r"\{\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}\}", replace, template)

def _bsod(message):
    print("\033[2J", end="", flush=True)
    print("\x1b[44m\x1b[37m",end="")
    print(message)
    # Source - https://stackoverflow.com/a/2084521
    # Posted by Joril, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-11-13, License - CC BY-SA 4.0
    for i in range(1,(shutil.get_terminal_size().lines) - len(message.split("\n"))):
        print()
    
    while True:
        time.sleep(3600)

def bsod(message, variables):
    _bsod(parse_template(f"""
A problem happened and {metadata.EAGLETOS_NAME} has shut down to prevent further problems to your computer.

{message}
    """, variables))

def file_bsod(template_path, variables):
    path = os.path.join("error_messages", template_path)

    with open(path, "r", encoding="utf-8") as file:
        template = file.read()

    bsod(template, variables)

if __name__ == "__main__":
    bsod("""If this problem occurs again, try NOT launching random binaries!

Stop code: BSOD_LAUNCHED_MANUALLY
""", {})