#!/usr/bin/python3

import sys
import os

BRIGHTNESS     = "/sys/class/backlight/amdgpu_bl0/brightness"
MAX_BRIGHTNESS = "/sys/class/backlight/amdgpu_bl0/max_brightness"

def usage():
    print("Usage:", sys.argv[0], "<brightness change>")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit(1)

    try:
        brightness_change = int(sys.argv[1])
    except ValueError:
        usage()
        exit(1)

    if not os.path.isfile(BRIGHTNESS) or not os.path.isfile(MAX_BRIGHTNESS):
        print("Unable to find one of the following files:", outfile=sys.stderr)
        print(BRIGHTNESS, outfile=sys.stderr)
        print(MAX_BRIGHTNESS, outfile=sys.stderr)
        exit(2)

    with open(MAX_BRIGHTNESS, 'r') as f:
        max_brightness = int(f.read())

    with open(BRIGHTNESS, 'r') as f:
        old_brightness = int(f.read())

    new_brightness = old_brightness + brightness_change
    new_brightness = min(new_brightness, max_brightness)
    new_brightness = max(new_brightness, 0)

    def write_new_brightness():
        with open(BRIGHTNESS, 'w') as f:
            f.write(str(new_brightness))

    try:
        write_new_brightness()
    except EnvironmentError:
        os.system("gksu chmod a+rw " + BRIGHTNESS)
        write_new_brightness()
