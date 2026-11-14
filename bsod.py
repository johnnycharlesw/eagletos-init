import shutil
def bsod(message):
    print("\x1b[44m")
    print(message)
    # Source - https://stackoverflow.com/a/2084521
    # Posted by Joril, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-11-13, License - CC BY-SA 4.0
    for i in range(1,(shutil.get_terminal_size().lines) - len(message.split("\n"))):
        print()
    
    while True:
        pass

if __name__ == "__main__":
    bsod("A problem happened and EagletOS has shut down to prevent further problems to your computer.")