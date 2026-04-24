import os
import glob

def find_exe(app_name):
    candidates = []

    special_cases = {
        "vscode": "code.exe"
    }

    exe_name = special_cases.get(
        app_name.lower(),
        f"{app_name.lower()}.exe"
    )

    # rest of your search logic stays unchanged

    # --- Step 1: Known locations (fast path) ---
    local_app = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("PROGRAMFILES")
    program_files_x86 = os.environ.get("PROGRAMFILES(X86)")

    search_bases = [
        (local_app, app_name),
        (program_files, app_name),
        (program_files_x86, app_name)
    ]

    for base_root, folder_name in search_bases:
        if not base_root:
            continue

        base_path = os.path.join(base_root, folder_name)
        if os.path.isdir(base_path):
            # Look for versioned folders like app-*
            paths = glob.glob(os.path.join(base_path, "*", exe_name))
            candidates.extend(paths)

            # Also check direct install (no version folder)
            direct_path = os.path.join(base_path, exe_name)
            if os.path.isfile(direct_path):
                candidates.append(direct_path)

    # --- If found in known locations ---
    if candidates:
        # Simple deterministic choice (you can improve later)
        best = sorted(candidates, reverse=True)[0]
        return best

    # --- Step 2: Fallback scan ---
    search_roots = [local_app, program_files, program_files_x86]

    for root in search_roots:
        if not root or not os.path.isdir(root):
            continue

        for folder, _, files in os.walk(root):
            for file in files:
                if file.lower() == exe_name:
                    return os.path.join(folder, file)

    return None


# --- Launcher / validation ---
app = "vscode"  # change this to test others
path = find_exe(app)

if path:
    print(f"{app} found at:", path)
    os.startfile(path)  # actually launch it
else:
    print(f"{app} not found.")