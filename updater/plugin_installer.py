import ctypes
import sys
import threading
import shutil
import subprocess
import zipfile
import requests
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------------------------------
# PATH SETUP (EXE-SAFE)
# -------------------------------------------------
exe_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
project_root = exe_dir.parent                # LIDE/
plugins_dir = project_root / "plugins"      # LIDE/plugins
plugins_dir.mkdir(parents=True, exist_ok=True)

exe_file = project_root / "LIDE.exe"
icon_file = project_root / "icon" / "lide.ico"

# -------------------------------------------------
# ADMIN CHECK
# -------------------------------------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    params = " ".join(f'"{a}"' for a in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", str(sys.executable), params, None, 1)
    sys.exit(0)

if not is_admin():
    relaunch_as_admin()

# -------------------------------------------------
# TKINTER UI
# -------------------------------------------------
root = tk.Tk()
root.title("Plugin Updater - LIDE")
root.geometry("400x250")
root.configure(bg="#2E2E2E")
root.resizable(False, False)

try:
    root.iconbitmap(icon_file)
except:
    pass

def center(win, w, h):
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

center(root, 400, 250)

opt_python = tk.BooleanVar()
loading_win = None
progress = None
progress_label = None

# -------------------------------------------------
# NETWORK CHECK
# -------------------------------------------------
def is_connected():
    try:
        requests.get("https://github.com", timeout=5)
        return True
    except:
        return False

# -------------------------------------------------
# LOADING WINDOW
# -------------------------------------------------
def show_loading(text):
    global loading_win, progress, progress_label
    loading_win = tk.Toplevel(root)
    loading_win.title("Please wait")
    loading_win.configure(bg="#1E1E1E")
    loading_win.resizable(False, False)
    loading_win.grab_set()
    center(loading_win, 360, 120)

    progress_label = tk.Label(
        loading_win, text=text,
        bg="#1E1E1E", fg="white",
        font=("Segoe UI", 12, "bold")
    )
    progress_label.pack(pady=15)

    progress = ttk.Progressbar(
        loading_win, length=320, mode="determinate"
    )
    progress.pack(pady=10)

def close_loading():
    global loading_win
    if loading_win:
        loading_win.destroy()
        loading_win = None

# -------------------------------------------------
# PLUGIN CONFIG
# -------------------------------------------------
PLUGIN_URLS = {
    "Python_Extension":
        "https://github.com/Codebyte15/LIDE_plugins/releases/download/Python_Extension/Python_Extension.zip"
}

# -------------------------------------------------
# DOWNLOAD + INSTALL
# -------------------------------------------------
def download_and_install(plugin):
    temp_dir = Path(os.environ["TEMP"]) / "LIDE_plugin_temp"
    try:
        if not is_connected():
            messagebox.showerror("No Internet", "Check your network.")
            return

        # Cleanup temp
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True)

        zip_path = temp_dir / f"{plugin}.zip"
        root.after(0, show_loading, f"Downloading {plugin}...")

        # Download
        r = requests.get(PLUGIN_URLS[plugin], stream=True, timeout=30)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
                downloaded += len(chunk)
                percent = int(downloaded * 100 / total) if total else 0
                root.after(0, lambda p=percent: (
                    progress.config(value=p),
                    progress_label.config(text=f"Downloading... {p}%")
                ))

        root.after(0, lambda: progress_label.config(text="Extracting..."))

        # Extract
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(temp_dir)

        src = temp_dir / plugin
        dst = plugins_dir / plugin

        # Remove old plugin if exists
        if dst.exists():
            shutil.rmtree(dst)

        shutil.move(str(src), str(dst))

        messagebox.showinfo("Success", f"{plugin} installed successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    finally:
        # Cleanup temp
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        root.after(0, close_loading)
        root.after(0, launch_lide)
        root.after(0, root.destroy)

# -------------------------------------------------
# LAUNCH LIDE
# -------------------------------------------------
def launch_lide():
    if exe_file.exists():
        subprocess.Popen([str(exe_file)], cwd=str(project_root))
    else:
        messagebox.showerror("Error", f"LIDE.exe not found at {exe_file}")

# -------------------------------------------------
# START INSTALL
# -------------------------------------------------
def start_install():
    if not opt_python.get():
        messagebox.showwarning("No Selection", "Select at least one plugin.")
        return

    threading.Thread(target=download_and_install, args=("Python_Extension",), daemon=True).start()

# -------------------------------------------------
# UI
# -------------------------------------------------
tk.Label(
    root,
    text="Select Plugins to Install",
    font=("Segoe UI", 14, "bold"),
    bg="#2E2E2E",
    fg="white"
).pack(pady=10)

tk.Checkbutton(
    root,
    text="Python_Extension",
    variable=opt_python,
    font=("Segoe UI", 12),
    bg="#2E2E2E",
    fg="white",
    selectcolor="#2E2E2E"
).pack(anchor="w", padx=30)

tk.Button(
    root,
    text="Download & Install",
    command=start_install,
    font=("Segoe UI", 12, "bold"),
    bg="#4CAF50",
    fg="white"
).pack(pady=20, ipadx=10, ipady=5)

root.mainloop()
