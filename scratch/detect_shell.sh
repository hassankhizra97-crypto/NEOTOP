#!/usr/bin/env python3

import os

shell_path = os.environ.get("SHELL")

if shell_path is None:
    print("Could not detect shell")
    exit()

shell = os.path.basename(shell_path)

rc_file = None

if shell == "bash":
    rc_file = "~/.bashrc"

elif shell == "zsh":
    rc_file = "~/.zshrc"

elif shell == "fish":
    rc_file = "~/.config/fish/config.fish"

else:
    print("Unsupported shell:", shell)
    exit()

line = 'export PATH="$HOME/.kawaii/bin:$PATH"'

print(f"Shell detected: {shell}")
print(f"File to edit: {rc_file}")
print("The line to append:")
print(line)
