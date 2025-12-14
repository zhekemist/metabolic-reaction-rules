"""
- contains all the code needed to import mod
- no cluttered import sections anymore
"""

import os
import sys
import subprocess

os.environ["BABEL_LIBDIR"] += ":/usr/lib64/openbabel3"

TALAX_PATH = "/home/talax/xtof/local/Mod"
if os.path.exists(TALAX_PATH):
    mod_loc = TALAX_PATH + "/bin/mod"
    mod_lib = TALAX_PATH + "/lib64"
else:
    mod_loc = (
        subprocess.run(["which", "mod"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip("\n")
    )
    if len(mod_loc) == 0:
        print("MØD not found.")
        sys.exit()
    mod_lib = os.path.join(os.path.split(mod_loc)[0], "../lib64")
sys.path.append(mod_lib)
import mod  # NOQA
