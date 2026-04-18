"""This is the current working code to find discords .exe file.
This will be the basis for app locating. This
section gets ran first. """

import os
import glob

def find_discord_exe():
    candidates = []

    # --- Step 1: Known locations (fast path) ---
    local_app = os.environ.get("LOCALAPPDATA")
    if local_app:
        base = os.path.join(local_app, "Discord")
        if os.path.isdir(base):
            paths = glob.glob(os.path.join(base, "app-*", "Discord.exe"))
            candidates.extend(paths)

    program_files = os.environ.get("PROGRAMFILES")
    if program_files:
        pf_path = os.path.join(program_files, "Discord", "Discord.exe")
        if os.path.isfile(pf_path):
            candidates.append(pf_path)

    program_files_x86 = os.environ.get("PROGRAMFILES(X86)")
    if program_files_x86:
        pf86_path = os.path.join(program_files_x86, "Discord", "Discord.exe")
        if os.path.isfile(pf86_path):
            candidates.append(pf86_path)

    # --- If found in known locations ---
    if candidates:
        # Pick the newest version (Discord uses app-* folders)
        best = sorted(candidates, reverse=True)[0]
        return best

    # --- Step 2: Fallback scan (slow but reliable) ---
    search_roots = [
        local_app,
        program_files,
        program_files_x86
    ]

    for root in search_roots:
        if not root or not os.path.isdir(root):
            continue

        for folder, _, files in os.walk(root):
            for file in files:
                if file.lower() == "discord.exe":
                    return os.path.join(folder, file)

    return None

"""This section is a launcher to prove the above
code went and found discords .exe file. This sectioin
gets ran second."""

path = find_discord_exe()

if path:
    print("Discord found at:", path)
else:
    print("Discord not found.")