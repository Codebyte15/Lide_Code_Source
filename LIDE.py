import ast
import queue
import string
import shutil
import tempfile
import colorama
import requests
import platform
import importlib
import tkinter as tk
from pathlib import Path
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog, messagebox, simpledialog, ttk
import os, re, sys, time, zipfile, threading, subprocess, webbrowser

class lide:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.update()
        self.root.state("zoomed")
        self.root.update_idletasks()
        self.root.minsize(500, 500)
        self.root.maxsize(5000, 5000)
        self.VERSION = "v3.0.0_stable"
        try: 
            self.root.wm_iconbitmap("icon/lide.ico")
        except Exception:
            pass
        self.root.title("LIDE - (Lightweight Internal Development Editor) v3.0.0_stable")
        self.BASE_URL = "https://github.com/Codebyte15/Lide_Code/releases/download"
        self.tree = None
        self.style = None
        self.editor = None
        self.zoom = int(18)
        self.open_tabs = {}
        self.menubar = None
        self.top_bar = None
        self.RUN_CMD = "cmd"
        self.run_menu = None
        self.log_file = None
        self.temp_dir = None
        self.terminal = None
        self.is_saved = True
        self.tab_padding = 5
        self.open_files = []
        self.enter_btn = None
        self.file_type = None
        self.file_menu = None
        self.help_menu = None
        self.tab_frame = None
        self.os_system = None
        self.scrollbar = None
        self.separator = None
        self.tab_canvas = None
        self.status_bar = None
        self.tree_frame = None
        self.active_tab = None
        self.editor_area = None
        self.plugin_menu = None
        self.editor_frame = None
        self.run_terminal = None
        self.current_file = None
        self.line_numbers = None
        self.License_menu = None
        self.extract_menu = None
        self.run_mode_cmd = False
        self.content_frame = None
        self.run_btn_frame = None
        self._linecount_job = None
        self.preview_editor = None
        self.terminal_frame = None
        self.frame_for_tabs = None
        self.tab_inner_frame = None
        self.Color_mode_name = None
        self.character_label = None
        self.code_runner_btn = None
        self.tab_canvas_frame = None
        self.decompile_editor = None
        self.line_count_label = None
        self.editor_main_frame = None
        self.RUN_INBUILT = "terminal"        
        self.more_settings_tab = None
        self._autosave_running = False
        self.scrollbar_explorer = None
        self.preview_editor_mode = None
        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).parent
            sys.path.insert(0, str(base_dir / "Lib"))
        self.appdata = os.getenv("APPDATA") or os.path.expanduser("~")
        self.lide_app_dir = os.path.join(self.appdata, "LIDE")
        os.makedirs(self.lide_app_dir, exist_ok=True)
        self.settings_path = os.path.join(self.lide_app_dir, "Settings.ini")
        open(self.settings_path, "a", encoding="utf-8").close()
        self.file_name = os.path.join(self.lide_app_dir, "saved_filename.ini")
        open(self.file_name, "a", encoding="utf-8").close()
        self.log_path = os.path.join(self.lide_app_dir, "log.ini")
        open(self.log_path, "a", encoding="utf-8").close()
        self.autosave_path = os.path.join(self.lide_app_dir, "autosave.ini")
        open(self.autosave_path, "a", encoding="utf-8").close()
        self.zoom_in_appdata = os.path.join(self.lide_app_dir, "zoom.ini")
        open(self.zoom_in_appdata, "a", encoding="utf-8").close()
        self.font_path = os.path.join(self.lide_app_dir, "font.ini")
        open(self.font_path, "a", encoding="utf-8").close()
        self.about_path = os.path.join(self.lide_app_dir, "about.ini")
        open(self.about_path, "a", encoding="utf-8").close()
        preview_folder = os.path.join(self.lide_app_dir, "preview")
        os.makedirs(preview_folder, exist_ok=True)
        self.preview_editor_mode = os.path.join(preview_folder, "preview.ini")
        open(self.preview_editor_mode, "a", encoding="utf-8").close()
        self.preview_editor_fontsize_mode = os.path.join(preview_folder, "preview_fontsize.ini")
        open(self.preview_editor_fontsize_mode, "a", encoding="utf-8").close()
        explorer_folder = os.path.join(self.lide_app_dir, "explorer")
        os.makedirs(explorer_folder, exist_ok=True)
        self.explorer_mode = os.path.join(explorer_folder, "explorer.ini")
        open(self.explorer_mode, "a", encoding="utf-8").close()
        self.explorer_directory_mode = os.path.join(explorer_folder, "explorer_directory_mode.ini")
        open(self.explorer_directory_mode, "a", encoding="utf-8").close()
        terminal_folder = os.path.join(self.lide_app_dir, "terminal")
        os.makedirs(terminal_folder, exist_ok=True)
        self.terminal_mode = os.path.join(terminal_folder, "terminal_mode.ini")
        open(self.terminal_mode, "a", encoding="utf-8").close()
        self.terminal_fontsize_mode = os.path.join(terminal_folder, "terminal_fontsize_mode.ini")
        open(self.terminal_fontsize_mode, "a", encoding="utf-8").close()
        self.program_run_mode = os.path.join(terminal_folder, "program_run_mode.ini")
        open(self.program_run_mode, "a", encoding="utf-8").close()
        
        if os.path.exists(self.log_path):
            with open(self.log_path , "a", encoding="utf-8") as f:
                f.write("Logged in at :- " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        
        try:
            with open(self.program_run_mode, "r") as f:
                mode = f.read().strip().lower()
        except FileNotFoundError:
            mode = self.RUN_INBUILT

        if mode not in (self.RUN_INBUILT, self.RUN_CMD):
            mode = self.RUN_INBUILT

        self.run_mode_cmd = (mode == self.RUN_CMD)

        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                for line in f:
                    p = line.strip()
                    if os.path.exists(p):
                        self.open_files.append(p)
            if self.open_files:
                self.current_file = self.open_files[0]
            
        if os.path.exists(self.zoom_in_appdata):
            with open(self.zoom_in_appdata, "r", encoding="utf-8") as f:
                self.zoom_read = f.read().strip()
                try:
                    self.zoom = int(self.zoom_read)
                except ValueError:
                    self.zoom = 17
        self.ctk_safe_fonts = [
            "Consolas",
            "Courier New",
            "Roboto",
            "Arial",
            "Helvetica"
        ]
        if os.path.exists(self.font_path):
            with open(self.font_path, "r", encoding="utf-8") as f:
                self.check_font = f.read().strip()

        if self.check_font in self.ctk_safe_fonts:
            self.font = self.check_font
        else:
            self.font = "Consolas"
            with open(self.font_path, "w", encoding="utf-8") as f:
                f.write("Consolas")
                f.flush()
                os.fsync(f.fileno())
            
        self.BLOCK_KEYWORDS = {
            ".py":  ('def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with', 'async','{','[','('),
            ".c":   ('if', 'else', 'for', 'while', 'do', 'switch', 'case', 'struct', 'union', 'enum', 'goto','{','[','('),
            ".cpp": ('if', 'else', 'for', 'while', 'do', 'switch', 'case', 'struct', 'union', 'enum', 'class', 'try', 'catch','{','[','('),
            ".java":('if', 'else', 'for', 'while', 'do', 'switch', 'case', 'try', 'catch', 'finally', 'class', 'interface', 'enum','{','[','('),
            ".js":  ('if', 'else', 'for', 'while', 'do', 'switch', 'case', 'function', 'class', 'try', 'catch', 'finally','{','[','(')
        }

        self.HIGHLIGHT_RULES = {
            ".py": {
                "keywords": (
                    "def", "class", "if", "elif", "else", "for", "while", "try", "except",
                    "finally", "with", "import", "from", "return", "as", "pass", "raise",
                    "lambda", "yield", "global", "nonlocal", "assert", "del", "in", "is",
                    "not", "and", "or", "break", "continue"
                ),
                "datatypes": ("int", "float", "str", "bool", "list", "dict", "set", "tuple"),
                "builtins": ("print", "len", "range", "open", "super", "self"),
                "booleans": ("True", "False", "None"),
                "colors": {
                    "keyword": "#569CD6",
                    "datatype": "#FFF9C4",
                    "builtin": "#FFF9C4",
                    "boolean": "#FFF9C4",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "decorator": "#C586C0",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                }
            },

            ".c": {
                "keywords": ("if", "else", "for", "while", "return", "switch", "case", "break", "continue","include", "define", "typedef", "struct", "union", "enum"),
                "datatypes": ("int", "float", "double", "char", "void", "short", "long", "unsigned", "signed", "bool"),
                "booleans": ("true", "false"),
                "colors": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                    "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "function": "#DCDCAA"
                }
            },

            ".cpp": {
                "keywords": ("if", "else", "for", "while", "return", "switch", "case", "break", "continue", "try", "catch", "namespace", "using", "new", "delete","include", "define", "typedef", "struct", "union", "enum", "class"),
                "datatypes": ("int", "float", "double", "char", "void", "short", "long", "unsigned", "signed", "bool", "class", "struct"),
                "booleans": ("true", "false"),
                "preprocessor": ("#include", "#define", "#ifdef", "#ifndef", "#endif"),
                "colors": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                    "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "preprocessor": "#C586C0",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                }
            },

            ".java": {
                "keywords": ("class", "public", "private", "protected", "static", "final", "abstract", "try", "catch", "finally", "return", "new", "this", "extends", "implements", "throw", "throws"),
                "datatypes": ("int", "float", "double", "char", "boolean", "long", "void", "byte", "short", "String"),
                "booleans": ("true", "false", "null"),
                "colors": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                }
            },

            ".js": {
                "keywords": ("function", "var", "let", "const", "if", "else", "for", "while", "return", "try", "catch", "finally", "class", "export", "import", "extends", "new", "throw", "await", "async"),
                "datatypes": ("Number", "String", "Boolean", "Array", "Object", "Symbol", "BigInt"),
                "booleans": ("true", "false", "null", "undefined"),
                "colors": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                    "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                }
            }
        }
        self.FILE_TYPE_MAP = {
            ".py": "Python File", ".pyw": "Python File", ".pyc": "Python Compiled File",
            ".java": "Java File", ".class": "Java Compiled File",
            ".c": "C File", ".cpp": "C++ File", ".h": "C/C++ Header File", ".hpp": "C++ Header File",
            ".cs": "C# File", ".go": "Go File", ".rs": "Rust File", ".swift": "Swift File",
            ".kt": "Kotlin File", ".m": "Objective-C File", ".r": "R File", ".jl": "Julia File",
            ".dart": "Dart File", ".ts": "TypeScript File", ".tsx": "TypeScript JSX File",
            ".js": "JavaScript File", ".jsx": "JavaScript JSX File", ".php": "PHP File",
            ".rb": "Ruby File", ".pl": "Perl File", ".sh": "Shell Script", ".bat": "Batch File",
            ".ps1": "PowerShell Script", ".lua": "Lua File", ".sql": "SQL File",

            ".html": "HTML File", ".htm": "HTML File", ".xhtml": "XHTML File",
            ".css": "CSS File", ".scss": "SASS File", ".less": "LESS File",
            ".xml": "XML File", ".json": "JSON File", ".yaml": "YAML File", ".yml": "YAML File",
            ".md": "Markdown File", ".rst": "reStructuredText File", ".txt": "Text File",

            ".csv": "CSV File", ".tsv": "TSV File", ".xls": "Excel Spreadsheet", ".xlsx": "Excel Spreadsheet",
            ".ods": "OpenDocument Spreadsheet", ".db": "Database File", ".sqlite": "SQLite Database",
            ".parquet": "Parquet File", ".feather": "Feather File",

            ".doc": "Word Document", ".docx": "Word Document", ".odt": "OpenDocument Text",
            ".pdf": "PDF File", ".rtf": "Rich Text Format", ".tex": "LaTeX File",
            ".ppt": "PowerPoint Presentation", ".pptx": "PowerPoint Presentation", ".odp": "OpenDocument Presentation",

            ".png": "PNG Image", ".jpg": "JPEG Image", ".jpeg": "JPEG Image", ".bmp": "Bitmap Image",
            ".gif": "GIF Image", ".tiff": "TIFF Image", ".ico": "Icon File", ".svg": "SVG Vector Image",
            ".webp": "WEBP Image", ".heic": "HEIC Image",

            ".mp3": "MP3 Audio", ".wav": "WAV Audio", ".flac": "FLAC Audio",
            ".aac": "AAC Audio", ".ogg": "OGG Audio", ".m4a": "M4A Audio",

            ".mp4": "MP4 Video", ".mov": "MOV Video", ".avi": "AVI Video",
            ".mkv": "MKV Video", ".wmv": "WMV Video", ".flv": "FLV Video", ".webm": "WebM Video",

            ".zip": "ZIP Archive", ".rar": "RAR Archive", ".7z": "7-Zip Archive",
            ".tar": "TAR Archive", ".gz": "GZIP Archive", ".bz2": "BZIP2 Archive",
            ".xz": "XZ Archive", ".iso": "ISO Disk Image",

            ".ttf": "TrueType Font", ".otf": "OpenType Font", ".woff": "Web Open Font Format",
            ".woff2": "Web Open Font Format 2",

            ".ini": "INI File", ".cfg": "Configuration File", ".conf": "Configuration File",
            ".log": "Log File", ".env": "Environment File", ".dockerfile": "Dockerfile",
            ".bin": "Binary File", ".dat": "Data File", ".lock": "Lock File",
            ".bak": "Backup File", ".tmp": "Temporary File",
        }

    def add_tab(self, path):
        if not path:
            self.check_no_tabs()
            return

        if path in self.open_tabs:
            self.select_tab(path)
            return

        tab = ctk.CTkFrame(self.tab_inner_frame, fg_color="gray7", corner_radius=0)
        tab.pack(side="left", pady=1)

        btn = ctk.CTkButton(
            tab,
            text=self.shorten(os.path.basename(path)),
            fg_color="transparent",
            font=("Arial", 14),
            width=5,
            height=3,
            corner_radius=0,
            hover_color="gray30",
            command=lambda p=path: self.open_file_given(p)
        )
        btn.pack(side="left")
        tab.btn = btn

        close_btn = ctk.CTkButton(
            tab,
            text="✕",
            width=18,
            fg_color="transparent",
            hover_color="#8B0000",
            corner_radius=0,
            command=lambda p=path: self.close_tab(p)
        )
        close_btn.pack(side="right")

        self.open_tabs[path] = tab
        self.select_tab(path)
    
        if path not in self.open_files:
            self.open_files.append(path)
            with open(self.file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(self.open_files))

        self.tab_inner_frame.update_idletasks()
        self.tab_canvas.configure(scrollregion=self.tab_canvas.bbox("all"))

        self.tab_canvas.xview_moveto(1.0)

    def close_tab(self, path):
        if path not in self.open_tabs:
            return

        self.open_tabs[path].destroy()
        del self.open_tabs[path]

        if path in self.open_files:
            self.open_files.remove(path)
            with open(self.file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(self.open_files))
                f.flush()
                os.fsync(f.fileno())

        if self.current_file == path:
            self.current_file = None

            if not self.open_tabs:
                self.editor.delete("1.0", "end")

        if self.open_tabs:
            next_path = next(iter(self.open_tabs))
            if os.path.exists(next_path):
                dir_path = os.path.dirname(next_path)
                self.refresh_directory_node(dir_path)
                self.open_file_given(next_path)
            else:
                self.close_tab(next_path)
            self.update_line_numbers()
        else:
            self.check_no_tabs()

    def check_no_tabs(self):
        if not self.open_tabs:
            with open(self.file_name, "w", encoding="utf-8") as f:
                f.write("")
                f.flush()
                os.fsync(f.fileno())
            self.update_title()

    def select_tab(self, path):
        for tab in self.open_tabs.values():
            tab.configure(fg_color="gray25")

        if path in self.open_tabs:
            self.open_tabs[path].configure(fg_color="gray40")
            self.active_tab = path
            self.current_file = path
            ext = Path(path).suffix.lower()
            friendly_name = self.FILE_TYPE_MAP.get(ext, f"{ext[1:].upper()} File" if ext else "Unknown File Type")
            self.file_type.configure(text=friendly_name)
            self.update_title()

    def shorten(self, text, max_chars=10):
        return text if len(text) <= max_chars else text[:max_chars-3] + "..."

    def check_update(self):
        threading.Thread(
            target=self._check_update_worker,
            daemon=True
        ).start()

    def check_update(self):
        threading.Thread(
            target=self._check_update_worker,
            daemon=True
        ).start()

    def _check_update_worker(self):
        owner = "Codebyte15"
        repo = "Lide_Code"
        url = f"https://api.github.com/repos/{owner}/{repo}/tags"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            tags = response.json()

            if not tags or not tags[0].get("name"):
                self.root.after(
                    0,
                    lambda: messagebox.showwarning(
                        "Offline / Network Error",
                        "Could not fetch the latest version. Check your internet connection."
                    )
            )
                return

            latest_tag = tags[0]["name"]

            if self.VERSION != latest_tag:
                self.root.after(
                    0,
                    lambda lt=latest_tag: self._show_update_ui(lt)
                )

        except requests.RequestException:
            self.root.after(
                0,
                lambda: messagebox.showwarning(
                    "Offline / Network Error",
                    "Could not fetch the latest version. Check your internet connection."
                )
            )

        except Exception as e:
            self.root.after(
                0,
                lambda err=str(e): messagebox.showerror(
                    "Error",
                    f"Unexpected error:\n{err}"
                )
            )
            
    def _show_update_ui(self, latest_tag):
        self.latest_tag = latest_tag

        self.update_window = ctk.CTkToplevel(self.root)
        self.update_window.title("Update Available")
        self.update_window.resizable(False, False)
        self.update_window.transient(self.root)
        self.update_window.grab_set()
        self.update_window.attributes("-topmost", True)

        window_width = 400
        window_height = 250
        screen_width = self.update_window.winfo_screenwidth()
        screen_height = self.update_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.update_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        ctk.CTkLabel(
            self.update_window,
            text="Update Available",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 10))

        details_frame = ctk.CTkFrame(self.update_window)
        details_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            details_frame,
            text=f"Update Name: {latest_tag}",
            font=("Arial", 14)
        ).pack(padx=(20,0),pady=(10, 5), anchor="w")

        try:
            url = f"{self.BASE_URL}/{latest_tag}/LIDE_{latest_tag}-setup.zip"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.head(url, headers=headers, timeout=10)
            total_size = int(r.headers.get("Content-Length", 0))
            total_mb = total_size / (1024 * 1024)
        except:
            total_mb = 0

        ctk.CTkLabel(
            details_frame,
            text=f"File Size: {total_mb:.2f} MB",
            font=("Arial", 14)
        ).pack(padx=(20,0),pady=(5, 10), anchor="w")

        btn_frame = ctk.CTkFrame(self.update_window)
        btn_frame.pack(pady=15)

        yes_btn = ctk.CTkButton(
            btn_frame,
            text="Yes",
            width=100,
            command=lambda: self._start_update_download()
        )
        yes_btn.pack(side="left", padx=20)

        no_btn = ctk.CTkButton(
            btn_frame,
            text="No",
            width=100,
            command=self.update_window.destroy
        )
        no_btn.pack(side="right", padx=20)
        
    def _start_update_download(self):
        self.update_window.destroy()
        self.update_download(self.latest_tag)

    def update_download(self, latest_tag):
        self.cancel_download = False
        self.latest_tag = latest_tag

        self.updater = ctk.CTkToplevel(self.root)
        self.updater.title(f"Updating LIDE to {latest_tag}")
        self.updater.geometry("460x260")
        self.updater.resizable(False, False)
        self.updater.transient(self.root)
        self.updater.grab_set()
        self.updater.attributes("-topmost", True)
        window_width = 460
        window_height = 260
        screen_width = self.updater.winfo_screenwidth()
        screen_height = self.updater.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.updater.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.status_label = ctk.CTkLabel(
            self.updater,
            text="Preparing download..."
        )
        self.status_label.pack(pady=(20, 8))

        self.progress_bar = ctk.CTkProgressBar(
            self.updater,
            width=380
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.info_label = ctk.CTkLabel(
            self.updater,
            text="0% | 0 KB/s"
        )
        self.info_label.pack(pady=5)

        self.cancel_btn = ctk.CTkButton(
            self.updater,
            text="Cancel",
            command=self.cancel_update
        )
        self.cancel_btn.pack(pady=15)

        threading.Thread(
            target=self._download_worker,
            daemon=True
        ).start()

    def cancel_update(self):
        self.cancel_download = True
        self.status_label.configure(text="Cancelling...")

    def _download_worker(self):
        try:
            url = f"{self.BASE_URL}/{self.latest_tag}/LIDE_{self.latest_tag}-setup.zip"
            headers = {"User-Agent": "Mozilla/5.0"}

            self.root.after(
                0,
                lambda: self.status_label.configure(text="Downloading update...")
            )

            r = requests.get(url, stream=True, headers=headers, timeout=30)
            r.raise_for_status()

            total_size = int(r.headers.get("Content-Length", 0))
            total_mb = total_size / (1024 * 1024)

            self.root.after(
                0,
                lambda: self.info_label.configure(
                    text=f"Package size: {total_mb:.2f} MB"
                )
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                zip_path = tmp_path / "LIDE_setup.zip"
                extract_dir = tmp_path / "extracted"
                extract_dir.mkdir(exist_ok=True)

                downloaded = 0
                start_time = time.time()

                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if self.cancel_download:
                            r.close()
                            return

                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                            elapsed = max(time.time() - start_time, 0.1)
                            speed = (downloaded / 1024) / elapsed
                            progress = downloaded / total_size if total_size else 0
                            percent = int(progress * 100)

                            self.root.after(
                                0,
                                lambda p=progress, pe=percent, sp=speed: (
                                    self.progress_bar.set(p),
                                    self.info_label.configure(
                                        text=f"{pe}% | {sp:.1f} KB/s"
                                    )
                                )
                            )

                self.root.after(
                    0,
                    lambda: self.status_label.configure(text="Extracting files...")
                )

                with zipfile.ZipFile(zip_path, "r") as z:
                    self._safe_extract(z, extract_dir)

                for name in os.listdir(extract_dir):
                    if name.lower().endswith(".exe"):
                        subprocess.Popen(
                            [str(extract_dir / name)],
                            shell=True
                        )
                        break

                self.root.after(0, self.root.quit)

        except Exception as e:
            messagebox.showerror(
                "Update Error",
                f"Update failed:\n{e}"
            )
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Update Failed",
                    f"Update failed:\n{e}"
                )
            )
            self.root.after(0, self.updater.destroy)

    def _safe_extract(self, zip_file, target_dir):
        for member in zip_file.infolist():
            member_path = (target_dir / member.filename).resolve()

            if not str(member_path).startswith(str(target_dir.resolve())):
                raise Exception("Unsafe zip content detected")

            if member.is_dir():
                member_path.mkdir(parents=True, exist_ok=True)
                continue

            member_path.parent.mkdir(parents=True, exist_ok=True)
            with zip_file.open(member) as src, open(member_path, "wb") as dst:
                shutil.copyfileobj(src, dst)
            
    def main(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as f:
                self.Color_mode_name = f.read().strip()
                self.Color_Mode(self.Color_mode_name)
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_close)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        self.user_menu = tk.Menu(self.menubar, tearoff=0)
        self.user_menu.add_command(label="Login Info", command=lambda: self.Login_info())
        self.menubar.add_cascade(label="User", menu=self.user_menu)

        self.run_menu = tk.Menu(self.menubar, tearoff=0)
        self.run_menu.add_command(label="Python File", command=lambda: self.run_app())
        self.run_menu.add_command(label="C File", command=lambda: self.run_app())
        self.run_menu.add_command(label="C++ File", command=lambda: self.run_app())
        self.run_menu.add_command(label="Java File", command=lambda: self.run_app())
        self.run_menu.add_command(label="HTML File", command=lambda: self.run_app())
        self.menubar.add_cascade(label="Run", menu=self.run_menu)
        
        self.search_menu = tk.Menu(self.menubar, tearoff=0)
        self.search_menu.add_command(label="Search and Replace", command=lambda: self.search_and_replace())
        self.menubar.add_cascade(label="Search", menu=self.search_menu)
        
        self.extract_menu = tk.Menu(self.menubar, tearoff=0)
        self.extract_menu.add_command(label="Decompile program to hex", command=lambda: self.decompile_app())
        self.extract_menu.add_command(label="Fetch Source from static website", command=lambda: self.fetch_source())
        self.menubar.add_cascade(label="Extract", menu=self.extract_menu)

        self.plugin_menu = tk.Menu(self.menubar, tearoff=0)
        self.plugin_menu.add_command(label="Download Plugins", command=lambda: self.download_plugin())
        self.plugin_menu.add_command(label="Make Plugins", command=lambda: self.Make_plugin())
        self.plugin_menu.add_command(label="Import file as plugin", command=lambda: self.import_file())
        self.plugin_menu.add_separator()
        self.menubar.add_cascade(label="Plugins", menu=self.plugin_menu)
        
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.settings_menu.add_command(label="Preferences",command=self.preferences)
        self.autosave_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.autosave_menu.add_command(label="Start",command=self.start_autosave)
        self.autosave_menu.add_command(label="Stop",command=self.stop_autosave)
        self.autosave_menu.entryconfig("Stop", state="disabled")
        self.settings_menu.add_cascade(label="Autosave",menu=self.autosave_menu)
        self.menubar.add_cascade(label="Settings",menu=self.settings_menu)

        self.License_menu = tk.Menu(self.menubar, tearoff=0)
        self.License_menu.add_command(label="MIT License", command=lambda: self.mit_license())
        self.menubar.add_cascade(label="License", menu=self.License_menu)
        
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.About_section)
        self.help_menu.add_command(label="Show Shortcuts", command=self.Shortcuts_section)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        self.editor_frame = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        self.editor_frame.grid(row=0, column=0, sticky="nsew")

        self.editor_frame.grid_columnconfigure(0, weight=0)
        self.editor_frame.grid_columnconfigure(1, weight=6)
        self.editor_frame.grid_columnconfigure(2, weight=0)
        self.editor_frame.grid_rowconfigure(0, weight=1)

        self.root.grid_rowconfigure(0, weight=4)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.editor_area = ctk.CTkFrame(self.editor_frame, fg_color=self.bg_color)
        self.editor_area.grid(row=0, column=1, sticky="nsew")

        self.frame_for_tabs = ctk.CTkFrame(self.editor_area, fg_color=self.bg_color, height=30)
        self.frame_for_tabs.pack(side="top", fill="x", padx=(50,15))

        self.tab_canvas_frame = ctk.CTkFrame(self.frame_for_tabs, fg_color=self.bg_color)
        self.tab_canvas_frame.pack(side="left", fill="both", expand=True)

        self.tab_canvas = ctk.CTkCanvas(self.tab_canvas_frame, height=30, bg=self.bg_color, highlightthickness=0)
        self.tab_canvas.pack(side="top", fill="both", expand=True)

        self.tab_inner_frame = ctk.CTkFrame(self.tab_canvas,corner_radius=0, fg_color=self.bg_color, height=20)
        self.tab_window = self.tab_canvas.create_window((0, 0), window=self.tab_inner_frame, anchor="nw")

        self.tab_scrollbar = ctk.CTkScrollbar(self.tab_canvas_frame, height=10, corner_radius=1, orientation="horizontal", command=self.tab_canvas.xview)
        self.tab_scrollbar.pack(side="bottom", fill="x")
        self.tab_canvas.configure(xscrollcommand=self.tab_scrollbar.set)

        self.tab_inner_frame.bind("<Configure>", lambda e: self.tab_canvas.configure(scrollregion=self.tab_canvas.bbox("all")))

        self.run_btn_frame = ctk.CTkFrame(self.frame_for_tabs, fg_color=self.bg_color)
        self.run_btn_frame.pack(side="right", fill="y")
        self.code_runner_btn = ctk.CTkButton(
            self.run_btn_frame,
            text="▶",
            font=("Consolas", 16, "bold"),
            text_color=self.fg_color,
            width=1,
            command=lambda: self.run_app()
        )
        self.code_runner_btn.pack(side="right")
    
        self.editor_main_frame = ctk.CTkFrame(self.editor_area, fg_color=self.bg_color)
        self.editor_main_frame.pack(side="top", fill="both", expand=True)

        self.line_numbers = ctk.CTkTextbox(
            self.editor_main_frame,
            width=50,
            fg_color=self.line_num,
            text_color=self.line_num_fg,
            font=("Consolas", self.zoom),
            corner_radius=0,
            border_width=0,
            wrap="none",
            state="disabled",
            activate_scrollbars=False
        )
        self.line_numbers.pack(side="left", fill="y")

        self.editor = ctk.CTkTextbox(
            self.editor_main_frame,
            font=(self.font, self.zoom),
            fg_color=self.color,
            text_color=self.fg_color,
            corner_radius=0,
            border_width=0,
            wrap="none",
            undo=True,
            activate_scrollbars=False,
        )
        self.editor.pack(side="left", fill="both", expand=True)
        self.editor.tag_config("sel", background="#DADADA")
        self.editor._textbox.configure(inactiveselectbackground="#DADADA")

        self.editor.tag_config(
            "sel",
            background="#DADADA"
        )
        self.editor._textbox.configure(
            inactiveselectbackground="#DADADA"
        )
        
        self.scrollbar = ctk.CTkScrollbar(
            self.editor_main_frame, orientation="vertical", fg_color=self.line_num
        )
        self.scrollbar.pack(side="right", fill="y")

        def sync_line_numbers():
            try:
                frac = self.editor.yview()[0]
                self.line_numbers.yview_moveto(frac)
            except Exception:
                messagebox.showerror("Error", "Failed to sync line numbers.")
    
        self.scrollbar.configure(command=lambda *args: (
            self.editor.yview(*args),
            sync_line_numbers()
        ))

        self.editor.configure(yscrollcommand=lambda *args: (
            self.scrollbar.set(*args),
            sync_line_numbers()
        ))

        self.editor.bind("<ButtonRelease-1>", lambda e: sync_line_numbers())

        self.editor.bind("<KeyRelease>", lambda e: sync_line_numbers(), add="+")
        
        self.status_bar = ctk.CTkFrame(self.root, fg_color=self.bg_color, height=24)
        self.status_bar.grid(row=1, column=0, sticky="ew")
        self.root.grid_rowconfigure(1, weight=0)

        self.status_bar.grid_columnconfigure(0, weight=0)
        self.status_bar.grid_columnconfigure(1, weight=1)
        self.status_bar.grid_columnconfigure(2, weight=0) 
        self.status_bar.grid_columnconfigure(3, weight=0)
        self.status_bar.grid_columnconfigure(4, weight=0)

        self.file_type = ctk.CTkLabel(
            master=self.status_bar,
            text="No file is Open",
            font=("Cascadia Mono Light", 14, "bold"),
            text_color=self.fg_color
        )
        self.file_type.grid(row=0, column=0, sticky="w", padx=(10,5), pady=2)

        self.character_label = ctk.CTkLabel(
            master=self.status_bar,
            text="length = 0",
            font=("Cascadia Mono Light", 12, "bold"),
            text_color=self.fg_color
        )
        self.character_label.grid(row=0, column=2, sticky="e", padx=(10,5), pady=2)

        self.line_count_label = ctk.CTkLabel(
            master=self.status_bar,
            text="lines = 0",
            font=("Cascadia Mono Light", 12, "bold"),
            text_color=self.fg_color
        )
        self.line_count_label.grid(row=0, column=3, sticky="e", padx=(10,5), pady=2)

        os_system = platform.system()
        self.os_system = ctk.CTkLabel(
            master=self.status_bar,
            text=f"OS: {os_system}",
            font=("Cascadia Mono Light", 12, "bold"),
            text_color=self.fg_color
        )
        self.os_system.grid(row=0, column=4, sticky="e", padx=(10,10), pady=2)

        self.root.configure(fg_color=self.bg_color)

        if self.current_file:
            self.open_file_given(self.current_file)
            self.update_line_count()
            self.update_title()
            self.highlight_syntax()
            self.update_line_numbers()
            
        try:
            with open(self.autosave_path , "r") as f:
                state = f.read().strip()
                if state == "enabled":
                    self.start_autosave()
            self.check_no_tabs()
        except:
            pass
        
    def has_function(self, filepath, func_name):
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        return any(
            isinstance(node, ast.FunctionDef) and node.name == func_name
            for node in ast.walk(tree)
        )

    def import_file(self):
        location = filedialog.askopenfilename(
            title="Select the file",
            filetypes=(("Python Files", "*.py"),)
        )

        if not location:
            return

        if os.path.exists(location):
            if self.has_function(location, "setup_plugin"):
    
                module_name = os.path.splitext(os.path.basename(location))[0]

                spec = importlib.util.spec_from_file_location(module_name, location)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "setup_plugin"):
                    module.setup_plugin(self)
                self.plugin_menu.add_command(label=module_name)
                messagebox.showinfo("Success", "Plugin has been Imported")

            else:
                messagebox.showwarning("Failed", "Plugin was not imported !!")
            
    def is_terminal_disabled(self):
        if not os.path.exists(self.terminal_mode):
            return False
        try:
            with open(self.terminal_mode) as f:
                return f.read().strip().lower() == "disabled"
        except OSError:
            return False

    def terminal_cli(self):
        if self.is_terminal_disabled():
            return
        
        try:
            with open(self.terminal_fontsize_mode, "r") as f:
                size = f.read().strip()
        except FileNotFoundError:
            size = "10"
        
        if size == "10":
            fontsize = int(10)
        elif size == "12":
            fontsize = int(12)
        elif size == "15":
            fontsize = int(15)
        else:
            fontsize = int(10)

        colorama.init()

        if not hasattr(self, "terminal_queue") or self.terminal_queue is None:
            self.terminal_queue = queue.Queue()

        if hasattr(self, "terminal_frame") and self.terminal_frame is not None:
            try:
                if hasattr(self, "process") and self.process:
                    self.process.kill()
            except Exception:
                messagebox.showerror("Error", "Failed to terminate existing terminal process.")
            self.terminal_frame.destroy()
            self.terminal_frame = None
            return

        if not getattr(self, "current_file", None):
            messagebox.showwarning(
                "No File",
                "Please create or open a file first"
            )
            return

        terminal_bg = self.color
        terminal_fg = self.fg_color
        entry_bg = self.color

        self.terminal_frame = ctk.CTkFrame(self.editor_area, fg_color=terminal_bg, height=280)
        self.terminal_frame.pack(side="bottom", fill="x")
        self.terminal_frame.pack_propagate(False)

        start_dir = os.path.dirname(self.current_file)

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        CREATE_NO_WINDOW = 0x08000000

        self.process = subprocess.Popen(
            ["cmd.exe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,
            cwd=start_dir,
            env=env,
            creationflags=CREATE_NO_WINDOW
        )

        entry_frame = ctk.CTkFrame(self.terminal_frame, fg_color=terminal_bg)
        entry_frame.pack(fill="x", side="bottom")

        self.run_terminal = ctk.CTkEntry(
            entry_frame,
            font=("Consolas", 12),
            fg_color=entry_bg,
            text_color=terminal_fg,
            corner_radius=0,
            border_width=0,
            height=30
        )
        self.run_terminal.pack(side="left", fill="x", expand=True)
        self.run_terminal.focus_set()

        self.enter_btn = ctk.CTkButton(
            entry_frame,
            text="▶",
            width=40,
            height=30,
            corner_radius=0,
            fg_color=entry_bg,
            hover_color="#555555" if getattr(self, "color", "") == "#2B2B2B" else "#D0D0D0",
            text_color=terminal_fg,
            command=lambda: get_focus_on_run()
        )
        self.enter_btn.pack(side="right")

        self.terminal = tk.Text(
            self.terminal_frame,
            font=("Consolas", fontsize),
            bg=terminal_bg,
            fg=terminal_fg,
            insertbackground=terminal_fg,
            wrap="none",
            state="disabled"
        )
        self.terminal.pack(fill="both", expand=True, side="top")
        
        def get_focus_on_run():
            self.run_terminal.focus_set()
            self.run_terminal.event_generate("<Return>")

        def insert_terminal(text):
            self.terminal.configure(state="normal")
            self.terminal.insert("end", text)
            self.terminal.see("end")
            self.terminal.configure(state="disabled")

        def read_process():
            try:
                while True:
                    if not getattr(self, 'process', None):
                        break
                    ch = self.process.stdout.read(1)
                    if ch == "" and self.process.poll() is not None:
                        break
                    if not ch:
                        time.sleep(0.01)
                        continue
                    self.terminal_queue.put(ch)
            except Exception:
                return

        threading.Thread(target=read_process, daemon=True).start()

        def update_gui():
            while not self.terminal_queue.empty():
                insert_terminal(self.terminal_queue.get())
            self.terminal_frame.after(20, update_gui)

        update_gui()

        self.command_history = []
        self.history_index = 0

        def process_input(event, ignore_cls=False):
            cmd = self.run_terminal.get()
            self.run_terminal.delete(0, "end")

            if cmd.strip():
                self.command_history.append(cmd)
                self.history_index = len(self.command_history)

            if not ignore_cls and cmd.lower() == "cls":
                self.terminal.configure(state="normal")
                self.terminal.delete("1.0", "end")
                self.terminal.configure(state="disabled")
                return "break"

            if getattr(self, 'process', None) and self.process.stdin:
                try:
                    self.process.stdin.write(cmd + "\n")
                    self.process.stdin.flush()
                except BrokenPipeError:
                    messagebox.showerror("Error", "Terminal process has terminated.")
                except Exception:
                    messagebox.showerror("Error", "Failed to send command to terminal process.")

            return "break"

        def navigate_history(event):
            if not self.command_history:
                return "break"
            if event.keysym == "Up":
                self.history_index = max(0, self.history_index - 1)
            elif event.keysym == "Down":
                self.history_index = min(len(self.command_history), self.history_index + 1)
            if self.history_index < len(self.command_history):
                self.run_terminal.delete(0, "end")
                self.run_terminal.insert(0, self.command_history[self.history_index])
            else:
                self.run_terminal.delete(0, "end")
            return "break"
        
        self.run_terminal.bind("<Return>", process_input)
        self.run_terminal.bind("<Up>", navigate_history)
        self.run_terminal.bind("<Down>", navigate_history)
        self.run_terminal.bind("<Control-c>", lambda e: self.process.kill() if getattr(self, 'process', None) else None)

    def explorer(self):
        try:
            with open(self.explorer_mode, "r") as f:
                mode = f.read().strip().lower()
        except FileNotFoundError:
            mode = ""

        if mode == "disable":
            return

        def get_drives():
            return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

        def sync_drive_menu():
            drive = os.path.splitdrive(self.current_path)[0] + "\\"
            if drive in get_drives():
                self.drive_menu.set(drive)

        if not getattr(self, "tree_frame", None) or not self.tree_frame.winfo_exists():
            if getattr(self, "current_file", None) and os.path.isfile(self.current_file):
                self.current_path = os.path.dirname(self.current_file)
            else:
                try:
                    with open(self.explorer_directory_mode, "r") as f:
                        take = f.read().strip().upper()
                except FileNotFoundError:
                    take = ""
                self.current_path = take + "\\" if take and os.path.exists(take + "\\") else os.path.abspath(os.sep)

            def get_node_path(node):
                return self.tree.item(node, "values")[0] if self.tree.item(node, "values") else None

            def on_expand(event):
                node = self.tree.focus()
                children = self.tree.get_children(node)
                if children and self.tree.item(children[0], "text") == "Loading...":
                    self.tree.delete(children[0])
                    path = get_node_path(node)
                    if path:
                        self.load_directory(path, node)

            def on_double_click(event):
                node = self.tree.focus()
                path = get_node_path(node)
                if not path:
                    return
                if os.path.isfile(path):
                    self.open_file_given(path)
                elif os.path.isdir(path):
                    self.current_path = path
                    self.tree.delete(*self.tree.get_children())
                    self.load_directory(path)
                    sync_drive_menu()

            def go_parent():
                parent = os.path.dirname(self.current_path.rstrip("\\"))
                if os.path.isdir(parent):
                    self.current_path = parent
                    self.tree.delete(*self.tree.get_children())
                    self.load_directory(parent)
                    sync_drive_menu()

            def change_drive(drive):
                self.current_path = drive
                self.tree.delete(*self.tree.get_children())
                self.load_directory(drive)

            def new_file():
                node = self.tree.focus()
                name = simpledialog.askstring("Input", "Enter file name with extension:")
                if not name:
                    return
                folder_path = get_node_path(node) if node else self.current_path
                if not os.path.isdir(folder_path):
                    folder_path = os.path.dirname(folder_path)
                if not folder_path:
                    return
                self.current_file = os.path.join(folder_path, name)
                try:
                    open(self.current_file, "w").close()
                    if node:
                        self.tree.delete(*self.tree.get_children(node))
                        self.load_directory(folder_path, node)
                    else:
                        self.tree.delete(*self.tree.get_children())
                        self.load_directory(folder_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot create file:\n{e}")
                    return
                self.editor.delete("1.0", "end")
                self.highlight_syntax()
                self.is_saved = True
                with open(self.file_name, "w") as f:
                    f.write(self.current_file)
                self.update_title()
                self.update_preview_content()
                self.add_tab(self.current_file)
            
            def new_folder():
                node = self.tree.focus()
                name = simpledialog.askstring("Input", "Enter folder name:")
                if not name:
                    return

                folder_path = get_node_path(node) if node else self.current_path
                if not os.path.isdir(folder_path):
                    folder_path = os.path.dirname(folder_path)

                if not folder_path:
                    return

                new_dir = os.path.join(folder_path, name)

                try:
                    os.makedirs(new_dir, exist_ok=False)
                    self.refresh_directory_node(folder_path)
            
                except FileExistsError:
                    messagebox.showwarning("Folder Exists", "A folder with this name already exists.")
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot create folder:\n{e}")
            
            def delete_folder():
                node = self.tree.focus()
                if not node:
                    messagebox.showwarning("Delete", "No folder selected.")
                    return

                path = get_node_path(node)
                if not path or not os.path.exists(path):
                    messagebox.showerror("Delete", "Selected folder does not exist.")
                    return

                if not os.path.isdir(path):
                    messagebox.showwarning("Delete", "Selected item is not a folder.")
                    return

                if not messagebox.askyesno(
                    "Delete Folder",
                    f"Are you sure you want to permanently delete the folder:\n\n{os.path.basename(path)} ?"
                ):
                    return

                try:
                    if getattr(self, "current_file", None):
                        if self.current_file.startswith(path):
                            self.editor.delete("1.0", "end")
                            self.close_tab(self.current_file)
                            self.current_file = None
                            self.is_saved = True
                            self.update_title()
                            self.update_preview_content()
            
                    shutil.rmtree(path)

                    parent_node = self.tree.parent(node)
                    refresh_node = parent_node
                    refresh_path = os.path.dirname(path)

                    self.tree.delete(*self.tree.get_children(refresh_node))
                    self.load_directory(refresh_path, refresh_node)

                except Exception as e:
                    messagebox.showerror("Error", f"Cannot delete folder:\n{e}")

            def delete_file():
                node = self.tree.focus()
                if not node:
                    messagebox.showwarning("Delete", "No file/folder selected.")
                    return
                path = get_node_path(node)
                if not path or not os.path.exists(path):
                    messagebox.showerror("Delete", "Selected file/folder does not exist.")
                    return
                if not messagebox.askyesno("Delete", f"Are you sure you want to delete '{os.path.basename(path)}'?"):
                    return
                try:
                    if getattr(self, "current_file", None) == path:
                        self.editor.delete("1.0", "end")
                        self.current_file = None
                        self.close_tab(path)
                        self.is_saved = True
                        self.update_title()
                        self.update_preview_content()
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    parent_node = self.tree.parent(node)
                    refresh_node, refresh_path = parent_node, os.path.dirname(path)
                    while refresh_node:
                        parent_path = get_node_path(refresh_node)
                        if parent_path and os.path.exists(parent_path):
                            refresh_path = parent_path
                            break
                        refresh_node = self.tree.parent(refresh_node)
                    self.tree.delete(*self.tree.get_children(refresh_node))
                    self.load_directory(refresh_path, refresh_node)
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot delete:\n{e}")
            
            def periodic_check():
                self.highlight_active_file()
                self.root.after(1000, periodic_check) 

            self.tree_frame = ctk.CTkFrame(self.editor_frame, width=300, fg_color=self.bg_color)
            self.tree_frame.grid(row=0, column=0, sticky="ns")
            
            self.top_bar = ctk.CTkFrame(self.tree_frame, fg_color=self.bg_color)
            self.top_bar.pack(fill="x")
            
            self.path_frame = ctk.CTkFrame(
                self.tree_frame,
                fg_color="gray12",
                height=28
            )
            self.path_frame.pack(fill="x", padx=4, pady=(0, 4))

            self.path_label = ctk.CTkLabel(
                self.path_frame,
                text=self.current_path,
                anchor="w",
                font=("Consolas", 10),
                text_color="gray80"
            )
            self.path_label.pack(fill="x", padx=6)

            self.drive_menu = ctk.CTkOptionMenu(
                self.top_bar,
                values=get_drives(),
                width=70,
                command=change_drive
            )
            self.drive_menu.pack(side="left", padx=4, pady=2)

            self.parent_btn = ctk.CTkButton(
                self.top_bar,
                text="⬅ Parent",
                height=30,
                fg_color="gray10",
                hover_color="gray20",
                command=go_parent
            )
            self.parent_btn.pack(side="right", padx=4, pady=2)

            self.style = ttk.Style()
            self.style.theme_use("clam")
            self.style.configure(
                "Treeview",
                background=getattr(self, "tree_bg", "white"),
                foreground=getattr(self, "tree_fg", "black"),
                fieldbackground=getattr(self, "tree_bg", "white"),
                font=("Consolas", 10, "bold"),
                rowheight=24
            )
            self.style.map("Treeview", background=[("selected", getattr(self, "tree_select_bg", "#c0c0c0"))])

            self.tree = ttk.Treeview(self.tree_frame)
            self.tree.pack(fill="both", expand=True)

            self.scrollbar_explorer = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
            self.scrollbar_explorer.pack(side="right", fill="y")
            self.tree.configure(yscrollcommand=self.scrollbar_explorer.set)

            self.menu = tk.Menu(self.tree, tearoff=0)
            self.menu.add_command(label="New File", command=new_file)
            self.menu.add_command(label="New Folder", command=new_folder)
            self.menu.add_command(label="Delete File", command=delete_file)
            self.menu.add_command(label="Delete Folder", command=delete_folder)

            self.tree.bind("<<TreeviewOpen>>", on_expand)
            self.tree.bind("<Double-1>", on_double_click)
            self.tree.bind("<Button-3>", lambda e: self.menu.tk_popup(e.x_root, e.y_root))

            sync_drive_menu()
            self.load_directory(self.current_path)
            self.root.after(1000, periodic_check)
            
    def load_directory(self,path, parent_node=""):
        if hasattr(self, "path_label") and self.path_label.winfo_exists():
            self.path_label.configure(
                text=self.current_file if self.current_file else path
            )

        try:
            items = sorted(os.listdir(path))
        except Exception:
            self.tree.insert(parent_node, "end", text="⚠️ Access Denied")
            return
        for item in items:
            full_path = os.path.join(path, item)
            try:
                if os.path.isdir(full_path):
                    node = self.tree.insert(parent_node, "end", text=f"📁 {item}", values=(full_path,), open=False)
                    self.tree.insert(node, "end", text="Loading...")
                else:
                    self.tree.insert(parent_node, "end", text=f"📄 {item}", values=(full_path,))
            except Exception:
                messagebox.showwarning("Warning", f"Cannot access: {full_path}")
    
    def refresh_directory_node(self, dir_path):
        if not self.tree or not dir_path:
            return

        dir_path = os.path.normpath(os.path.abspath(dir_path))
        if not os.path.isdir(dir_path):
            return

        def find_node(node=""):
            for n in self.tree.get_children(node):
                values = self.tree.item(n, "values")
                if values:
                    node_path = os.path.normpath(os.path.abspath(values[0]))
                    if node_path == dir_path:
                        return n
                found = find_node(n)
                if found:
                    return found
            return None
    
        node = find_node()
    
        if node:
            self.tree.delete(*self.tree.get_children(node))
            self.load_directory(dir_path, node)
            self.tree.item(node, open=True)
        else:
            self.tree.delete(*self.tree.get_children())
            self.load_directory(dir_path)
        
    def highlight_active_file(self):
        if not self.tree_frame:
            return
        current = getattr(self, "current_file", None)
        if not current:
            return
        name = os.path.basename(current)

        def walk(node=""):
            for c in self.tree.get_children(node):
                if self.tree.item(c, "text").endswith(name):
                    self.tree.selection_set(c)
                    self.tree.see(c)
                    return True
                if walk(c):
                    self.tree.item(c, open=True)
                    return True
            return False

        walk()
    
    def search_and_replace(self):
        window = tk.Toplevel(self.root)
        window.title("Find & Replace")
        window.geometry("400x200")
        window.resizable(False, False)
        window.attributes("-topmost", True)
        window.iconbitmap("icon/lide.ico")
        window.configure(bg="gray20")

        style = ttk.Style(window)
        style.theme_use('clam')

        style.configure("TFrame", background="gray20")
        style.configure("TLabel", background="gray20", foreground="white")
        style.configure("TCheckbutton", background="gray20", foreground="white")
        style.configure("TButton", background="gray30", foreground="white")

        frame = ttk.Frame(window, padding=15)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Find:").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(frame, text="Replace with:").grid(row=1, column=0, sticky="e", pady=5)

        find_entry = ttk.Entry(frame, width=30)
        find_entry.grid(row=0, column=1, pady=5, padx=5)
        replace_entry = ttk.Entry(frame, width=30)
        replace_entry.grid(row=1, column=1, pady=5, padx=5)

        options_frame = ttk.Frame(frame)
        options_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

        case_var = tk.BooleanVar(value=True)
        whole_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Case-Sensitive", variable=case_var).grid(row=0, column=0, padx=(0,10))
        ttk.Checkbutton(options_frame, text="Whole Word", variable=whole_var).grid(row=0, column=1)

        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(buttons_frame, text="Replace All", command=lambda: [self.replace_all_in_text(
            find_entry.get(),
            replace_entry.get(),
            case_var.get(),
            whole_var.get()
        ), window.destroy()]).grid(row=0, column=0, padx=5)

        ttk.Button(buttons_frame, text="Cancel", command=window.destroy).grid(row=0, column=1, padx=5)
    
        find_entry.focus_set()    

    def replace_all_in_text(self, target, replacement, case_sensitive=True, whole_word=True):
        if not target:
            return

        content = self.editor.get("1.0", tk.END)
    
        pattern = r'\b' + re.escape(target) + r'\b' if whole_word else re.escape(target)
        flags = 0 if case_sensitive else re.IGNORECASE

        new_content = re.sub(pattern, replacement, content, flags=flags)
    
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", new_content) 
        self.highlight_syntax()        
    
    def preview(self):
        try:
            with open(self.preview_editor_mode, "r") as f:
                mode = f.read().strip().lower()
        except FileNotFoundError:
            mode = ""

        if mode == "disable":
            return
        
        try:
            with open(self.preview_editor_fontsize_mode, "r") as f:
                size = f.read().strip()
        except FileNotFoundError:
            size = "5"
        
        if size == "5":
            fontsize = int(5)
        elif size == "10":
            fontsize = int(10)
        elif size == "15":
            fontsize = int(15)
        else:
            fontsize = int(5)

        if not hasattr(self, 'preview_editor') or self.preview_editor is None:
            self.preview_editor = ctk.CTkTextbox(
                master=self.editor_frame,
                font=("Consolas", fontsize),
                fg_color=self.color,
                text_color=self.fg_color,
                corner_radius=0,
                border_width=0,
                state="disabled"
            )
            self.preview_editor.grid(row=0, column=2, sticky="nsew", pady=(41,0))
            self.root.grid_columnconfigure(1, weight=0)
            self.update_preview_content()
        
    def update_preview_content(self):
        if self.preview_editor and self.preview_editor.winfo_ismapped():
            content = self.editor.get("1.0", "end-1c")
            self.preview_editor.configure(state="normal")
            self.preview_editor.delete("1.0", "end")
            self.preview_editor.insert("1.0", content)
            self.preview_editor.configure(state="disabled")
        return

    def update_line_count(self, content=None, char_count=None):
        if content is None:
            content = self.editor.get("1.0", "end-1c")

        if char_count is None:
            char_count = len(content)

        line_count = int(self.editor.index("end-1c").split(".")[0])

        self.line_count_label.configure(text=f"lines = {line_count}")
        self.character_label.configure(text=f"length = {char_count}")
        
    def update_line_numbers(self, event=None):
        if not self.line_numbers or not self.editor:
            return
        first_frac = self.line_numbers.yview()[0]

        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        total_lines = int(self.editor.index('end-1c').split('.')[0])
        line_numbers_text = "\n".join(str(i) for i in range(1, total_lines + 1))
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.configure(state="disabled")

        self.line_numbers.yview_moveto(first_frac) 
    
    def new_file(self):
        name = simpledialog.askstring("Input", "Enter file name with extension:")
        if not name:
            return

        folder = filedialog.askdirectory(title="Select folder to save file")
        if not folder:
            return
        
        folder = os.path.normpath(folder)
        self.current_file = os.path.join(folder, name)

        try:
            open(self.current_file, "w").close()
            self.refresh_directory_node(folder)

        except Exception as e:
            messagebox.showerror("Error", f"Cannot create file:\n{e}")
            return

        self.editor.delete("1.0", "end")
        self.highlight_syntax()
        self.is_saved = True
        self.open_file_given(self.current_file)
        self.update_title()
        self.update_preview_content()
        self.add_tab(self.current_file)

        self.highlight_active_file()

    def open_file(self):
        path = filedialog.askopenfilename(title="Select a file", filetypes=(("All files", "*.*"),))
        if not path:
            return
        self._load_file_mainthread(path)

    def open_file_given(self, path_taken):
        path = path_taken
        if not path:
            return
        self._load_file_mainthread(path)

    def _load_file_mainthread(self, path):
        already_open = path in self.open_tabs
        self.current_file = path
        self.add_tab(path)

        ext = Path(path).suffix.lower()
        friendly_name = self.FILE_TYPE_MAP.get(ext, f"{ext[1:].upper()} File" if ext else "Unknown File Type")
        self.file_type.configure(text=friendly_name)

        if not os.path.exists(path):
            self.close_tab(path)
            return

        file_size = os.path.getsize(path)
        loading_window = None

        if file_size >= 51200 and not already_open:
            if not messagebox.askyesno("Permission", "Do you want to load this large file?"):
                self.close_tab(path)
                return

            loading_window = tk.Toplevel(self.root)
            loading_window.overrideredirect(True)
            loading_window.attributes("-topmost", True)
            loading_window.geometry(f"200x50+{self.root.winfo_x() + self.root.winfo_width() // 2 - 100}+{self.root.winfo_y() + self.root.winfo_height() // 2 - 25}")
            tk.Label(loading_window, text="Loading...", font=("Arial", 14)).pack(expand=True, fill="both")
            loading_window.update()

        def load_task():
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                self.root.after(0, lambda: finalize_load(content))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Read Error: {e}"))
                if loading_window: self.root.after(0, loading_window.destroy)
    
        def finalize_load(content):
            try:
                self.editor.configure(undo=False) 
                self.editor.delete("1.0", "end")
                
                self.editor.insert("1.0", content)
            
                self.editor.configure(undo=True)
                self.editor.edit_modified(False)

                self.update_title()
                self.update_line_count()
                self.update_line_numbers()
                self.highlight_active_file()
            
                self.root.after(50, self.highlight_syntax)

                with open(self.file_name, "w", encoding="utf-8") as f_ref:
                    f_ref.write(path)
            
            except:
                self.close_tab(path)

            finally:
                if loading_window:
                    loading_window.destroy()

        threading.Thread(target=load_task, daemon=True).start()

    def save_file(self, event=None):
        path = self.current_file
        try:
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            with open(self.settings_path, "w", encoding="utf-8") as f:
                f.write(getattr(self, "Colorbutton", ""))
                f.flush()
                os.fsync(f.fileno())
        except (PermissionError, OSError) as e:
            messagebox.showwarning("Access Denied", f"Cannot save settings:\n{e}")
            self.close_tab(path)
        if not self.current_file:
            return
        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", "end-1c"))
                f.flush()
                os.fsync(f.fileno())
            self.is_saved = True
        except (PermissionError, OSError) as e:
            messagebox.showwarning("Access Denied", f"Cannot save file:\n{self.current_file}\n{e}")
            self.close_tab(path)
            return "break"
        try:
            with open(self.file_name, "w") as f:
                f.write(self.current_file)
                f.flush()
                os.fsync(f.fileno())
        except (PermissionError, OSError) as e:
            messagebox.showwarning("Access Denied", f"Cannot update file reference:\n{self.file_name}\n{e}")
            self.close_tab(path)

        self.update_title()
        return "break"
        
    def _autosave_loop(self):
        if not getattr(self, "_autosave_running", False):
            return

        try:
            if getattr(self, "is_loading_file", False):
                return

            if not self.current_file or self.is_saved:
                return

            content = self.editor.get("1.0", "end-1c")
    
            if not content.strip():
                return

            autosave_dir = os.path.join(self.appdata, "LIDE", "autosave")
            os.makedirs(autosave_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.basename(self.current_file)
            backup_path = os.path.join(
                autosave_dir, f"{filename}_{timestamp}.bak"
            )
            
            self.save_file()

            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(content)

        except Exception as e:
            print("Autosave error:", e)

        finally:
            self.root.after(30000, self._autosave_loop)
    
    def start_autosave(self):
        messagebox.showinfo("Autosave Started", "Autosave Started")
        try:
            with open(self.autosave_path , "w") as f:
                f.write("enabled")
                f.flush()
                os.fsync(f.fileno())
        except:
            pass
        self._autosave_running = True
        self.autosave_menu.entryconfig("Start", state="disabled")
        self.autosave_menu.entryconfig("Stop", state="normal")
        self.root.after(1, self._autosave_loop)

    def stop_autosave(self):
        messagebox.showinfo("Autosave Stopped", "Autosave Stopped")
        try:
            with open(self.autosave_path , "w") as f:
                f.write("disabled")
                f.flush()
                os.fsync(f.fileno())
        except:
            pass
        self._autosave_running = False
        self.autosave_menu.entryconfig("Start", state="normal")
        self.autosave_menu.entryconfig("Stop", state="disabled")

    def run_app(self):
        self.save_file()
        current_file = self.current_file

        if not current_file:
            messagebox.showwarning("No File", "Create or open a file first!")
            return

        ext = os.path.splitext(current_file)[1].lower()
        path = os.path.dirname(current_file) or "."

        try:
            if ext == ".py":
                python_exe = shutil.which("python") or shutil.which("python3")
                if not python_exe:
                    messagebox.showerror("Python Not Found", "Python is not installed.")
                    return
                cmd = f'"{python_exe}" -u "{current_file}"'

            elif ext == ".c":
                exe = os.path.splitext(current_file)[0] + ".exe"
                cmd = f'gcc "{current_file}" -o "{exe}" && "{exe}"'

            elif ext in (".cpp", ".cc", ".cxx"):
                exe = os.path.splitext(current_file)[0] + ".exe"
                cmd = f'g++ "{current_file}" -o "{exe}" && "{exe}"'

            elif ext == ".java":
                name = os.path.splitext(os.path.basename(current_file))[0]
                cmd = f'cd /d "{path}" && javac "{os.path.basename(current_file)}" && java {name}'

            elif ext in (".html", ".htm"):
                webbrowser.open(current_file)
                return

        except Exception as e:
            messagebox.showerror("Run Error", str(e))
        
        if getattr(self, "run_mode_cmd", False):
            subprocess.Popen(
                f'cmd /k "{cmd}"', 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            return

        if not hasattr(self, "terminal_frame") or self.terminal_frame is None:
            self.terminal_cli()
        try:
            self.run_terminal.delete(0, "end")
            self.run_terminal.insert(0, cmd)
            self.terminal_frame.after(50, lambda: self.run_terminal.event_generate("<Return>", when="tail"))
        except:
            messagebox.showerror("Terminal", "Terminal is disabled \n Enable the terminal or Change the execution program")
    
    def _update_syntax_colors(self, is_dark_mode):
        if is_dark_mode:
            colors = {
                ".py": {
                    "keyword": "#569CD6",
                    "datatype": "#FFF9C4",
                    "builtin": "#FFF9C4",
                    "boolean": "#FFF9C4",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "decorator": "#C586C0",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                },
                ".c": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                    "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "function": "#DCDCAA"
                },
                ".cpp": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                    "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "preprocessor": "#C586C0",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                },
                ".java": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                    "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                },
                ".js": {
                    "keyword": "#569CD6",
                    "datatype": "#4FC1FF",
                    "boolean": "#569CD6",
                    "string": "#CE9178",
                    "comment": "#6A9955",
                    "number": "#B5CEA8",
                    "operator": "#D4D4D4",
                    "class": "#4EC9B0",
                    "function": "#DCDCAA"
                }
            }
        else:
            colors = {
                ".py": {
                    "keyword": "#0000FF",
                    "datatype": "#795E26",
                    "builtin": "#795E26",
                    "boolean": "#0000FF",
                    "string": "#A31515",
                    "comment": "#008000",
                    "number": "#098658",
                    "operator": "#000000",
                    "decorator": "#AF00DB",
                    "class": "#267F99",
                    "function": "#795E26"
                },
                ".c": {
                    "keyword": "#0000FF",
                    "datatype": "#267F99",
                    "boolean": "#0000FF",
                    "string": "#A31515",
                    "comment": "#008000",
                    "number": "#098658",
                    "operator": "#000000",
                    "function": "#795E26"
                },
                ".cpp": {
                    "keyword": "#0000FF",
                    "datatype": "#267F99",
                    "boolean": "#0000FF",
                    "string": "#A31515",
                    "comment": "#008000",
                    "number": "#098658",
                    "operator": "#000000",
                    "preprocessor": "#AF00DB",
                    "class": "#267F99",
                    "function": "#795E26"
                },
                ".java": {
                    "keyword": "#0000FF",
                    "datatype": "#267F99",
                    "boolean": "#0000FF",
                    "string": "#A31515",
                    "comment": "#008000",
                    "number": "#098658",
                    "operator": "#000000",
                    "class": "#267F99",
                    "function": "#795E26"
                },
                ".js": {
                    "keyword": "#0000FF",
                    "datatype": "#267F99",
                    "boolean": "#0000FF",
                    "string": "#A31515",
                    "comment": "#008000",
                    "number": "#098658",
                    "operator": "#000000",
                    "class": "#267F99",
                    "function": "#795E26"
                }
            }
        
        for ext in self.HIGHLIGHT_RULES:
            if "colors" in self.HIGHLIGHT_RULES[ext]:
                self.HIGHLIGHT_RULES[ext]["colors"].update(colors[ext])
    
    def preferences(self):
        self.preferences_tab = tk.Toplevel(self.root)
        self.preferences_tab.title("Settings")
        self.preferences_tab.attributes("-topmost", True)
        try:
            self.preferences_tab.iconbitmap("icon/lide.ico")
        except:
            pass
        self.preferences_tab.configure(bg="gray20")
        self.preferences_tab.resizable(False, False)

        width, height = 600, 300
        ws = self.preferences_tab.winfo_screenwidth()
        hs = self.preferences_tab.winfo_screenheight()
        x = (ws // 2) - (width // 2)
        y = (hs // 2) - (height // 2)
        self.preferences_tab.geometry(f"{width}x{height}+{x}+{y}")

        options_tab = tk.Frame(self.preferences_tab, bg="gray20", width=200)
        options_tab.grid(row=0, column=0, sticky="ns")
        options_tab.grid_propagate(False)

        show_window = tk.Frame(self.preferences_tab, bg="gray50")
        show_window.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=10)

        show_window.grid_rowconfigure(0, weight=1)
        show_window.grid_rowconfigure(1, weight=1)
        show_window.grid_rowconfigure(2, weight=1)
        show_window.grid_rowconfigure(3, weight=1)
        show_window.grid_columnconfigure(0, weight=1)
        show_window.grid_columnconfigure(1, weight=1)
        show_window.grid_columnconfigure(2, weight=1)

        label = tk.Label(
            show_window,
            text="SETTINGS",
            font=("Arial", 40, "bold"),
            bg="gray50"
        )
        label.grid(row=1, column=1, pady=(0, 15), sticky ="nsew")

        self.preferences_tab.grid_rowconfigure(0, weight=1)
        self.preferences_tab.grid_columnconfigure(1, weight=1)

        def show_heading(title):
            for widget in show_window.winfo_children():
                widget.destroy()
        
            heading_frame = tk.Frame(show_window, bg="gray30", padx=10, pady=10)
            heading_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0,10))

            heading = tk.Label(
                heading_frame,
                text=title,
                font=("Arial", 15, "bold"),
                bg="gray30",
                fg="white"
            )
            heading.pack(anchor="w")

        def style_option():
            show_heading("STYLE SETTINGS")

            dark_frame = tk.Frame(show_window, bg="gray50", pady=5)
            dark_frame.grid(row=1, column=0, sticky="w")

            tk.Label(
                    dark_frame,
                    text="Dark Mode:",
                    font=("Arial", 12),
                    bg="gray50"
            ).pack(side="left", padx=(0, 10))

            dark_mode_var = tk.StringVar()
            if self.color in ("#1E1E1E", "#252526"):
                dark_mode_var.set("Enable")
            else:
                dark_mode_var.set("Disable")

            def change_dark_mode():
                selected = dark_mode_var.get()
                if selected == "Enable":
                    if self.color in ("#FFFFFF", "white"):
                            self.Dark_Mode()
                else:
                    if self.color in ("#1E1E1E", "#252526"):
                            self.Dark_Mode()

            tk.Radiobutton(
                    dark_frame,
                    text="Enable",
                    variable=dark_mode_var,
                    value="Enable",
                    bg="gray50",
                    fg="white",
                    selectcolor="gray20",
                    activebackground="gray50",
                    command=change_dark_mode
            ).pack(side="left")

            tk.Radiobutton(
                    dark_frame,
                    text="Disable",
                    variable=dark_mode_var,
                    value="Disable",
                    bg="gray50",
                    fg="white",
                    selectcolor="gray20",
                    activebackground="gray50",
                    command=change_dark_mode
            ).pack(side="left")

            change_font = tk.Label(
                show_window,
                text="Change Font",
                font=("Arial", 12),
                bg="gray50"
            )
            change_font.grid(row=2, column=0, sticky="w", pady=5)
            
            change_font_button = tk.Button(
                show_window,
                text="Change:-",
                font=("Arial", 10),
                bg="gray50",
                command=lambda: self.Font_Mode()
            )
            change_font_button.grid(row=2, column=0, sticky="w", pady=5, padx=(120,0))

        def explorer_option():
            show_heading("EXPLORER SETTINGS")

            explorer_settings_frame = tk.Frame(show_window, bg="gray50", pady=5)
            explorer_settings_frame.grid(row=1, column=0, sticky="w")

            tk.Label(
                explorer_settings_frame,
                text="Explorer:",
                font=("Arial", 12),
                bg="gray50",
                fg="white"
            ).grid(row=0, column=0, padx=(0, 10), sticky="w")

            try:
                with open(self.explorer_mode, "r") as f:
                    mode = f.read().strip().lower()
            except FileNotFoundError:
                mode = ""

            explorer_var = tk.StringVar(
                value="Disable" if mode == "disable" else "Enable"
            )

            def toggle_explorer():
                selected = explorer_var.get()
        
                with open(self.explorer_mode, "w") as f:
                    f.write("" if selected == "Enable" else "disable")
                    f.flush()
                    os.fsync(f.fileno())

                if selected == "Enable":
                    if not getattr(self, "tree_frame", None) or not self.tree_frame.winfo_exists():
                        self.explorer()
                else:
                    if getattr(self, "tree_frame", None) and self.tree_frame.winfo_exists():
                        self.tree_frame.destroy()
                        self.tree_frame = None
                    self.style = None

            tk.Radiobutton(
                explorer_settings_frame,
                text="Enable",
                variable=explorer_var,
                value="Enable",
                bg="gray50",
                fg="white",
                selectcolor="gray20",
                activebackground="gray50",
                command=toggle_explorer
            ).grid(row=0, column=1, padx=5)

            tk.Radiobutton(
                explorer_settings_frame,
                text="Disable",
                variable=explorer_var,
                value="Disable",
                bg="gray50",
                fg="white",
                selectcolor="gray20",
                activebackground="gray50",
                command=toggle_explorer
            ).grid(row=0, column=2, padx=5)

            explorer_drive_frame = tk.Frame(show_window, bg="gray50", pady=5)
            explorer_drive_frame.grid(row=2, column=0, sticky="w")

            tk.Label(
                explorer_drive_frame,
                text="Start Drive:",
                font=("Arial", 12),
                bg="gray50",
                fg="white"
            ).grid(row=0, column=0, padx=(0, 10), sticky="w")

            try:
                with open(self.explorer_directory_mode, "r") as f:
                    current_drive = f.read().strip().upper()
            except FileNotFoundError:
                current_drive = "C"

            available_drives = [d for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

            drive_var = tk.StringVar(value=current_drive if current_drive in available_drives else available_drives[0])

            def select_drive():
                selected = drive_var.get()
                with open(self.explorer_directory_mode, "w") as f:
                    f.write(selected)
                    f.flush()
                    os.fsync(f.fileno())

                if getattr(self, "tree_frame", None) and self.tree_frame.winfo_exists():
                    self.tree_frame.destroy()
                    self.tree_frame = None

                self.explorer()

            for col, d in enumerate(available_drives, start=1):
                tk.Radiobutton(
                    explorer_drive_frame,
                    text=f"{d}:\\",
                    variable=drive_var,
                    value=d,
                    bg="gray50",
                    fg="white",
                    selectcolor="gray20",
                    activebackground="gray50",
                    command=select_drive
                ).grid(row=0, column=col, padx=3)
        
        def terminal_option():
            show_heading("TERMINAL SETTINGS")
            
            terminal_settings_frame = tk.Frame(show_window, bg="gray50", pady=5)
            terminal_settings_frame.grid(row=1, column=0, sticky="w")

            tk.Label(
                terminal_settings_frame,
                text="Terminal:- ",
                font=("Arial", 12),
                bg="gray50",
                fg="white"
            ).grid(row=0, column=0, padx=(0, 10), sticky="w")

            try:
                with open(self.terminal_mode, "r") as f:
                    mode = f.read().strip().lower()
            except FileNotFoundError:
                mode = ""

            terminal_var = tk.StringVar(
                value="Disable" if mode == "disabled" else "Enable"
            )

            def toggle_terminal():
                selected = terminal_var.get()
                if selected == "Disable":
                    with open(self.terminal_mode, "w") as f:
                        f.write("disabled")
                        f.flush()
                        os.fsync(f.fileno())

                    if getattr(self, "terminal_frame", None):
                        self.terminal_frame.destroy()
                        self.terminal_frame = None
                else:
                    with open(self.terminal_mode, "w") as f:
                        f.write("")
                        f.flush()
                        os.fsync(f.fileno())
                        
            tk.Radiobutton(
                terminal_settings_frame,
                text="Enable",
                variable=terminal_var,
                value="Enable",
                bg="gray50",
                fg="white",
                selectcolor="gray20",
                activebackground="gray50",
                command=toggle_terminal
            ).grid(row=0, column=1, padx=5)

            tk.Radiobutton(
                terminal_settings_frame,
                text="Disable",
                variable=terminal_var,
                value="Disable",
                bg="gray50",
                fg="white",
                selectcolor="gray20",
                activebackground="gray50",
                command=toggle_terminal
            ).grid(row=0, column=2, padx=5)
            
            terminal_fontsize_frame = tk.Frame(show_window, bg="gray50", pady=5)
            terminal_fontsize_frame.grid(row=2, column=0, sticky="w")

            tk.Label(
                terminal_fontsize_frame,
                text="Terminal Font Size:",
                font=("Arial", 12),
                bg="gray50",
                fg="white"
            ).pack(side="left", padx=(0,10))

            try:
                with open(self.terminal_fontsize_mode, "r") as f:
                    saved_size = f.read().strip()
            except FileNotFoundError:
                saved_size = "10"

            terminal_fontsize_var = tk.StringVar(value=saved_size)

            def toggle_terminal_fontsize():
                selected = terminal_fontsize_var.get()
                with open(self.terminal_fontsize_mode, "w") as f:
                    f.write(selected)
                    f.flush()
                    os.fsync(f.fileno())

                if self.terminal_frame and self.terminal:
                    self.terminal.configure(font=("Consolas", int(selected)))

            for size in ("10", "12", "15"):
                tk.Radiobutton(
                    terminal_fontsize_frame,
                    text=size,
                    variable=terminal_fontsize_var,
                    value=size,
                    bg="gray50",
                    fg="white",
                    selectcolor="gray20",
                    activebackground="gray50",
                    command=toggle_terminal_fontsize
                ).pack(side="left")
            
            exec_mode_frame = tk.Frame(show_window, bg="gray50", pady=5)
            exec_mode_frame.grid(row=3, column=0, sticky="w")

            tk.Label(
                exec_mode_frame,
                text="Execute Programs in:- ",
                font=("Arial", 12),
                bg="gray50",
                fg="white"
            ).grid(row=0, column=0, padx=(0, 10), sticky="w")

            try:
                with open(self.program_run_mode, "r") as f:
                    saved_mode = f.read().strip().lower()
            except FileNotFoundError:
                saved_mode = self.RUN_INBUILT

            if saved_mode not in (self.RUN_INBUILT, self.RUN_CMD):
                saved_mode = self.RUN_INBUILT

            program_run_var = tk.StringVar(
                value="In-built Terminal" if saved_mode == self.RUN_INBUILT else "CMD"
            )

            def toggle_program_run_mode():
                selected = program_run_var.get()
            
                mode = self.RUN_CMD if selected == "CMD" else self.RUN_INBUILT

                with open(self.program_run_mode, "w") as f:
                    f.write(mode)
                    f.flush()
                    os.fsync(f.fileno())

                self.run_mode_cmd = (mode == self.RUN_CMD)

            tk.Radiobutton(
                exec_mode_frame,
                text="In-built Terminal",
                variable=program_run_var,
                value="In-built Terminal",
                bg="gray50",
                fg="white",
                selectcolor="gray20",
                activebackground="gray50",
                command=toggle_program_run_mode
            ).grid(row=0, column=1, padx=5)

            tk.Radiobutton(
                exec_mode_frame,
                text="CMD",
                variable=program_run_var,
                value="CMD",
                bg="gray50",
                fg="white",
                selectcolor="gray20",
                activebackground="gray50",
                command=toggle_program_run_mode
            ).grid(row=0, column=2, padx=5)

        def preview_option():
            show_heading("PREVIEW SETTINGS")
    
            preview_frame = tk.Frame(show_window, bg="gray50", pady=5)
            preview_frame.grid(row=1, column=0, sticky="w")

            tk.Label(
                preview_frame,
                text="Preview Editor:",
                font=("Arial", 12),
                bg="gray50",
                fg="white"
            ).pack(side="left", padx=(0,10))

            try:
                with open(self.preview_editor_mode, "r") as f:
                    mode = f.read().strip().lower()
            except FileNotFoundError:
                mode = ""

            preview_var = tk.StringVar(value="Disable" if mode == "disable" else "Enable")

            def toggle_preview():
                selected = preview_var.get()

                with open(self.preview_editor_mode, "w") as f:
                    f.write("" if selected == "Enable" else "disable")
                    f.flush()
                    os.fsync(f.fileno())

                if selected == "Enable":
                    self.preview()
                else:
                    if self.preview_editor and self.preview_editor.winfo_exists():
                        self.preview_editor.destroy()
                        self.preview_editor = None

            for val in ("Enable", "Disable"):
                tk.Radiobutton(
                    preview_frame,
                    text=val,
                    variable=preview_var,
                    value=val,
                    bg="gray50",
                    fg="white",
                    selectcolor="gray20",
                    activebackground="gray50",
                    command=toggle_preview
                ).pack(side="left")

            preview_fontsize_frame = tk.Frame(show_window, bg="gray50", pady=5)
            preview_fontsize_frame.grid(row=2, column=0, sticky="w")

            tk.Label(
                preview_fontsize_frame,
                text="Preview Font Size:",
                font=("Arial", 12),
                bg="gray50",
                fg="white"
            ).pack(side="left", padx=(0,10))

            try:
                with open(self.preview_editor_fontsize_mode, "r") as f:
                    saved_size = f.read().strip()
            except FileNotFoundError:
                saved_size = "5"

            preview_fontsize_var = tk.StringVar(value=saved_size)

            def toggle_preview_fontsize():
                selected = preview_fontsize_var.get()
                with open(self.preview_editor_fontsize_mode, "w") as f:
                    f.write(selected)
                    f.flush()
                    os.fsync(f.fileno())

                if self.preview_editor and self.preview_editor.winfo_exists():
                    self.preview_editor.configure(font=("Arial", int(selected)))

            for size in ("5", "10", "15"):
                tk.Radiobutton(
                    preview_fontsize_frame,
            text=size,
                    variable=preview_fontsize_var,
                    value=size,
                    bg="gray50",
                    fg="white",
                    selectcolor="gray20",
                    activebackground="gray50",
                    command=toggle_preview_fontsize
                ).pack(side="left")

        option1 = tk.Button(
            options_tab,
            text="Styles",
            bg="gray20",
            fg="white",
            bd=2,
            width=25,
            height=3,
            activebackground="gray50",
            command=style_option
        )
        option1.grid(row=0, column=0, padx=7, pady=(20,10))
        
        option2 = tk.Button(
            options_tab,
            text="Explorer",
            bg="gray20",
            fg="white",
            bd=2,
            width=25,
            height=3,
            activebackground="gray50",
        command=explorer_option
        )
        option2.grid(row=1, column=0, padx=7, pady=(0,10))
        
        option3 = tk.Button(
            options_tab,
            text="Terminal",
            bg="gray20",
            fg="white",
            bd=2,
            width=25,
            height=3,
            activebackground="gray50",
            command=terminal_option
        )
        option3.grid(row=2, column=0, padx=7, pady=(0,12))
        
        option4 = tk.Button(
            options_tab,
            text="Preview",
            bg="gray20",
            fg="white",
            bd=2,
            width=25,
            height=3,
            activebackground="gray50",
            command=preview_option
        )
        option4.grid(row=3, column=0, padx=7, pady=(0,12))

        def on_enter(e):
            option1['bg'] = "gray35"

        def on_leave(e):
            option1['bg'] = "gray20"
    
        option1.bind("<Enter>", on_enter)
        option1.bind("<Leave>", on_leave)
    
    def Dark_Mode(self):
        if self.color in ("#FFFFFF", "white"):
            self.color = "#1E1E1E"
            self.fg_color = "#D4D4D4"
            self.bg_color = "#252526"
            self.tree_bg = "#2D2D30"
            self.tree_fg = "#CCCCCC"
            self.tree_select_bg = "#094771"
            self.Colorbutton = "Dark Mode"
            self.line_num = "#2D2D30"
            self.line_num_fg = "#858585"
            ctk.set_appearance_mode("dark")
            self.Color_mode_name = "dark mode"
            is_dark = True
        else:
            self.color = "#FFFFFF"
            self.fg_color = "#000000"
            self.bg_color = "#F3F3F3"
            self.tree_bg = "#FFFFFF"
            self.tree_fg = "#000000"
            self.tree_select_bg = "#B5D5FF"
            self.Colorbutton = "Default Mode"
            self.line_num = "#F3F3F3"
            self.line_num_fg = "#6E6E6E"
            ctk.set_appearance_mode("light")
            self.Color_mode_name = "default mode"
            is_dark = False
        
        self._update_syntax_colors(is_dark)

        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, "w") as f:
            f.write(self.Colorbutton)

        if self.editor:
            self.editor.configure(fg_color=self.color, text_color=self.fg_color)
        self.root.configure(fg_color=self.bg_color)
        if self.content_frame:
            self.content_frame.configure(fg_color=self.bg_color)
        if self.editor_area:
            self.editor_area.configure(fg_color=self.bg_color)
        if self.status_bar:
            self.status_bar.configure(fg_color=self.bg_color)
        if self.preview_editor:
            self.preview_editor.configure(fg_color=self.color, text_color=self.fg_color)
        if self.line_numbers:
            self.line_numbers.configure(fg_color=self.line_num, text_color=self.line_num_fg)
        if self.line_count_label:
            self.line_count_label.configure(text_color=self.fg_color)
        if self.character_label:
            self.character_label.configure(text_color=self.fg_color)
        if self.scrollbar:
            self.scrollbar.configure(fg_color=self.line_num)
        if self.top_bar:
            self.top_bar.configure(fg_color=self.bg_color)
        if self.tab_frame:
            self.tab_frame.configure(fg_color=self.bg_color)
        if self.editor_frame:
            self.editor_frame.configure(fg_color=self.bg_color)
        if self.tree_frame:
            self.tree_frame.configure(fg_color=self.bg_color)
        if self.file_type:
            self.file_type.configure(text_color=self.fg_color)
        if self.tab_inner_frame:
            self.tab_inner_frame.configure(fg_color=self.bg_color)
        if self.tab_canvas:
            self.tab_canvas.configure(bg=self.bg_color)
        if self.tab_canvas_frame:
            self.tab_canvas_frame.configure(fg_color=self.bg_color)
        if self.frame_for_tabs:
            self.frame_for_tabs.configure(fg_color=self.bg_color)
        if self.run_btn_frame:
            self.run_btn_frame.configure(fg_color=self.bg_color)
        if self.code_runner_btn:
            self.code_runner_btn.configure(text_color=self.fg_color)
        if self.editor_main_frame:
            self.editor_main_frame.configure(fg_color=self.bg_color)
        if self.os_system:
            self.os_system.configure(text_color=self.fg_color)
        if self.tree:
            self.style.configure("Treeview",
                                 background=self.tree_bg,
                                 foreground=self.tree_fg,
                                 fieldbackground=self.tree_bg)
            self.style.map("Treeview", background=[("selected", self.tree_select_bg)])

        if hasattr(self, "terminal_frame") and self.terminal_frame:
            terminal_bg = "#2D2D30" if is_dark else "#FFFFFF"
            terminal_fg = "#D4D4D4" if is_dark else "#000000"
            entry_bg = "#2D2D30" if is_dark else "#FFFFFF"
            hover_bg = "#094771" if is_dark else "#B5D5FF"

            self.terminal_frame.configure(fg_color=terminal_bg)
            if hasattr(self, "terminal"):
                self.terminal.configure(bg=terminal_bg, fg=terminal_fg, insertbackground=terminal_fg)
            if hasattr(self, "run_terminal"):
                self.run_terminal.configure(fg_color=entry_bg, text_color=terminal_fg)
            if hasattr(self, "enter_btn"):
                self.enter_btn.configure(fg_color=entry_bg, hover_color=hover_bg, text_color=terminal_fg)

        if self.editor and self.current_file:
            self.highlight_syntax()

    def Color_Mode(self, mode):
        if mode.lower() == "default mode":
            self.color = "#FFFFFF" 
            self.fg_color = "#1E1E1E" 
            self.bg_color = "#F5F5F5"     
            self.tree_bg = "#FFFFFF"
            self.tree_fg = "#1E1E1E"
            self.tree_select_bg = "#CCE4FF"
            self.Colorbutton = "Default Mode"
            self.line_num = "#F5F5F5"
            self.line_num_fg = "#7A7A7A"
            ctk.set_appearance_mode("light")
            self.Color_mode_name = "dark mode"
            is_dark = False
        else:
            self.color = "#1E1E1E" 
            self.fg_color = "#D4D4D4" 
            self.bg_color = "#2A2A2A" 
            self.tree_bg = "#252526"
            self.tree_fg = "#CCCCCC"
            self.tree_select_bg = "#094771"
            self.Colorbutton = "Dark Mode"
            self.line_num = "#2A2A2A"
            self.line_num_fg = "#858585"
            ctk.set_appearance_mode("dark")  
            self.Color_mode_name = "default mode"            
            is_dark = True

        self._update_syntax_colors(is_dark)

        if self.editor:
            self.editor.configure(fg_color=self.color, text_color=self.fg_color)
        self.root.configure(fg_color=self.bg_color)
        if self.content_frame:
            self.content_frame.configure(fg_color=self.bg_color)
        if self.editor_area:
            self.editor_area.configure(fg_color=self.bg_color)
        if self.status_bar:
            self.status_bar.configure(fg_color=self.bg_color)
        if self.preview_editor:
            self.preview_editor.configure(fg_color=self.color, text_color=self.fg_color)
        if self.line_numbers:
            self.line_numbers.configure(fg_color=self.line_num, text_color=self.line_num_fg)
        if self.line_count_label:
            self.line_count_label.configure(text_color=self.fg_color)
        if self.character_label:
            self.character_label.configure(text_color=self.fg_color)
        if self.scrollbar:
            self.scrollbar.configure(fg_color=self.line_num)
        if self.top_bar:
            self.top_bar.configure(fg_color=self.bg_color)
        if self.tab_frame:
            self.tab_frame.configure(fg_color=self.bg_color)
        if self.editor_frame:
            self.editor_frame.configure(fg_color=self.bg_color)
        if self.tree_frame:
            self.tree_frame.configure(fg_color=self.bg_color)
        if self.file_type:
            self.file_type.configure(text_color=self.fg_color)
        if self.tab_inner_frame:
            self.tab_inner_frame.configure(fg_color=self.bg_color)
        if self.tab_canvas:
            self.tab_canvas.configure(bg=self.bg_color)
        if self.tab_canvas_frame:
            self.tab_canvas_frame.configure(fg_color=self.bg_color)
        if self.frame_for_tabs:
            self.frame_for_tabs.configure(fg_color=self.bg_color)
        if self.run_btn_frame:
            self.run_btn_frame.configure(fg_color=self.bg_color)
        if self.code_runner_btn:
            self.code_runner_btn.configure(text_color=self.fg_color)
        if self.editor_main_frame:
            self.editor_main_frame.configure(fg_color=self.bg_color)
        if self.os_system:
            self.os_system.configure(text_color=self.fg_color)
        if self.tree:
            self.style.configure("Treeview",
                                 background=self.tree_bg,
                                 foreground=self.tree_fg,
                                 fieldbackground=self.tree_bg)
            self.style.map("Treeview", background=[("selected", self.tree_select_bg)])

        if hasattr(self, "terminal_frame") and self.terminal_frame:
            terminal_bg = "#2D2D30" if is_dark else "#FFFFFF"
            terminal_fg = "#D4D4D4" if is_dark else "#000000"
            entry_bg = "#2D2D30" if is_dark else "#FFFFFF"
            hover_bg = "#094771" if is_dark else "#B5D5FF"

            self.terminal_frame.configure(fg_color=terminal_bg)
            if hasattr(self, "terminal"):
                self.terminal.configure(bg=terminal_bg, fg=terminal_fg, insertbackground=terminal_fg)
            if hasattr(self, "run_terminal"):
                self.run_terminal.configure(fg_color=entry_bg, text_color=terminal_fg)
            if hasattr(self, "enter_btn"):
                self.enter_btn.configure(fg_color=entry_bg, hover_color=hover_bg, text_color=terminal_fg)

        if self.editor and self.current_file:
            self.highlight_syntax()
            
    def Font_Mode(self):
        self.font_mode = tk.Toplevel(self.root)
        self.font_mode.attributes("-topmost", True)
        self.font_mode.iconbitmap("icon/lide.ico")
        self.font_mode.configure(bg="gray20")
        self.font_mode.resizable(False, False)
        self.font_mode.title("Font Settings")
        self.fonts = self.ctk_safe_fonts
        self.selected_font = tk.StringVar(value=self.fonts[0])
        self.rows = 5
        self.cols = 2

        self.index = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.index < len(self.fonts):
                    tk.Radiobutton(
                        self.font_mode,
                        text=self.fonts[self.index],
                        variable=self.selected_font,
                        value=self.fonts[self.index],
                        bg="gray20",
                        fg="white",
                        selectcolor="gray35",
                        anchor="w",
                        width=18,
                        padx=0,
                        pady=10
                    ).grid(row=r, column=c, sticky="w")
                self.index += 1
        def change_font():
            chosen = self.selected_font.get()
            print("Selected font:", chosen)
            with open(self.font_path, "w") as f:
                f.write(chosen)
                f.flush()
                os.fsync(f.fileno())
            font = ctk.CTkFont(family=chosen, size=self.zoom)
            self.editor.configure(font=font)
            self.font_mode.destroy()
            
        btn = tk.Button(self.font_mode, text="Change",font=('Arial',10),bg="gray15",fg="white",bd=2,width=20, command=change_font)
        btn.grid(row=8,column=1)
    
    def decompile_app(self):
        data = filedialog.askopenfilename(
            title="Select the file",
            filetypes=(("All Files", "*."), ("All files", "*.*")),
        )
        if not data:
            return
        data_size = os.path.getsize(data) 
        if data_size >= 20971520:
            messagebox.showinfo("Large File", "The file is too large")
            return
        try:
            with open(data, "rb") as f:
                binary_data = f.read()
            hex_data = binary_data.hex(" ").upper()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the file: {e}")
            return
        if self.decompile_editor is not None:
            try:
                self.decompile_editor.destroy()
            except Exception:
                self.decompile_editor = None      
        self.decompile_editor = ctk.CTkToplevel(self.root)
        self.decompile_editor.configure(bg="gray15")
        self.decompile_editor.attributes('-topmost', True)
        self.decompile_editor.resizable(False, False)
        self.decompile_editor.geometry("600x500")
        self.decompile_editor.iconbitmap("icon/lide.ico")
        self.decompile_editor.title(data)
        self.text_decompile = ctk.CTkTextbox(
            self.decompile_editor,
            font=("Consolas", 12),
            fg_color="gray15",
            text_color ="white",
            wrap="word"
        )
        self.text_decompile.insert("0.0", hex_data)
        self.text_decompile.pack(fill="both", expand=True)
    
    def fetch_source(self):

        url = simpledialog.askstring(
            title="Fetch HTML Source",
            prompt="Enter website URL (static site only):",
            parent=self.root
        )

        if not url:
            return

        if not url.startswith(("http://", "https://")):
            messagebox.showerror(
                "Invalid URL",
            "URL must start with http:// or https://"
            )
            return
    
        save_path = filedialog.asksaveasfilename(
            title="Save HTML As",
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")]
        )
    
        if not save_path:
            return
    
        def task():
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/120.0.0.0 Safari/537.36"
                }

                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(response.text)

                self.root.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Success",
                        f"HTML saved successfully:\n\n{save_path}"
                    )
                )
                self.refresh_directory_node(os.path.dirname(save_path))

            except Exception as e:
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Fetch Error"
                    )
                )

        threading.Thread(
            target=task,
            daemon=True
        ).start()
    
    def download_plugin(self):
        check = messagebox.askyesno(
            "Plugin Updater",
            "This will open the Plugin Updater to download plugins.\nDo you want to continue?"
        )
        if not check:
            messagebox.showinfo("Cancelled", "Plugin download was cancelled.")
            return

        base_path = Path(sys.argv[0]).parent.resolve()

        exe_path = base_path / "updater" / "plugin_installer.exe"
        py_path  = base_path / "updater" / "plugin_installer.py"

        try:
            if exe_path.exists():
                subprocess.Popen([str(exe_path)], shell=True)
                self.on_close_without_prompt()
                return

            if py_path.exists():
                subprocess.Popen([sys.executable, str(py_path)], shell=True)
                self.on_close_without_prompt()
                return

            messagebox.showerror(
                "Error",
                f"Plugin updater not found.\n\n"
                f"Checked:\n{exe_path}\n{py_path}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to launch plugin updater:\n{e}"
            )

    def Make_plugin(self):
        plugin_txt ="""
                                          Documentation ( optional)
                                          
    # The Basic Funtion For Entry
    
    compatible_version = "v3.0.0_pre_release"
    
    def setup_plugin(IDE):
    
        ""  rest of the code ""
    
    
    # IDE CONTAINS ALL THE ELEMENTS UNDER CLASS "IDE" OF THE MAIN SCRIPT.
    
    # ROOT IS THE MAIN AREA WHERE THE WINDOW IS RUNNING
    
    # REMEMBER THE PLUGINS MUST CONTAIN ONLY THE IMPORTED LIBRARIES IN THE MAIN APP
    
    # ON LATER UPDATES MORE LIBRARIES WILL BE ADDED
    
    TO UPLOAD THE PLUGIN 
    
    MESSAGE ME ON @astro_moinak INSTAGRAM ACCOUNT"""
        self.plugin_root = ctk.CTkToplevel(self.root)
        self.plugin_root.attributes("-topmost", True)
        self.plugin_root.geometry("700x600")
        self.plugin_root.title("Make Plugins")
        self.plugin_root.resizable(False, False)
        self.plugin_txt_area = ctk.CTkTextbox(self.plugin_root,font=('Arial',15),text_color=self.fg_color,fg_color=self.bg_color)
        self.plugin_txt_area.pack(expand=True, fill='both')
        self.plugin_txt_area.insert("1.0", plugin_txt)
        self.plugin_txt_area.configure(state="disabled")
    

    def plugin(self):
        script_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
        plugin_folder = script_dir / "plugins"
        loaded_plugins = {}

        if not plugin_folder.exists():
            return

        for folder in plugin_folder.iterdir():
            if not folder.is_dir():
                continue

            plugin_file = folder / f"{folder.name}.py"
            if not plugin_file.exists():
                continue

            try:
                spec = importlib.util.spec_from_file_location(folder.name, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if not hasattr(module, "setup_plugin"):
                    raise Exception("setup_plugin() not found")
                if not hasattr(module, "compatible_version"):
                    raise Exception("compatible_version not defined")
                if module.compatible_version != self.VERSION:
                    raise Exception(
                        f"Incompatible plugin "
                        f"(plugin: {module.compatible_version}, editor: {self.VERSION})"
                    )

                module.setup_plugin(self)
                loaded_plugins[folder.name] = module

                self.plugin_menu.add_command(label=folder.name)

            except Exception as e:
                messagebox.showerror(
                    "Plugin Load Error",
                    f"Error loading plugin '{folder.name}':\n{e}"
                )
                
    def update_title(self):
        name = self.current_file if self.current_file else "Untitled"
        if not self.is_saved:
            name = "*" + name
        
        if hasattr(self, "path_label") and self.path_label.winfo_exists():
            self.path_label.configure(
                text=self.current_file if self.current_file else ""
            )

        self.root.title(f"{name} - LIDE(Lightweight Internal Development Editor) v3.0.0_stable")

    def on_text_change(self,event=None):
        try:
            if self.editor.edit_modified():
                self.is_saved = False
                self.update_title()
                self.editor.edit_modified(False)
                self.update_preview_content()
                self.update_line_numbers()
        except Exception:
            self.is_saved = False
            self.update_title()
    
    def on_close(self):
        result = messagebox.askyesnocancel("Confirm Exit","Do you want to save before exiting?\nUnsaved changes will be lost.")
        if result is True:
            try:
                self.save_file()
                self.root.destroy()
            except:
                messagebox.showerror("Error", "Process cant be killed")
        elif result is False:
            try:
                self.root.destroy()
            except:
                messagebox.showerror("Error", "Process cant be killed")
        
    def on_close_without_prompt(self):
        try:
            self.save_file()
            self.root.destroy()
        except:
            messagebox.showerror("Error", "Process cant be killed")

    def auto_indent(self,event=None):
        ext = os.path.splitext(self.current_file or "")[1].lower()
        keywords = self.BLOCK_KEYWORDS.get(ext, self.BLOCK_KEYWORDS[".py"])
        index = self.editor.index("insert")
        line_start = f"{index.split('.')[0]}.0"
        current_line = self.editor.get(line_start, f"{line_start} lineend")
        leading_spaces = len(current_line) - len(current_line.lstrip(' '))
        increase_indent = False
        stripped = current_line.strip()
    
        for kw in keywords:
            if ext == ".py":
                if stripped.startswith(kw) and stripped.endswith(':'):
                    increase_indent = True
                    break
            else:
                if stripped.startswith(kw) or stripped.endswith(kw):
                    increase_indent = True
                    break

        self.editor.insert("insert", "\n")
        spaces = ' ' * leading_spaces
        if increase_indent:
            spaces += ' ' * 4
        self.editor.insert("insert", spaces)
        return "break"
        
    def highlight_syntax(self, event=None):
        if hasattr(self, "_highlight_job"):
            self.editor.after_cancel(self._highlight_job)

        self._highlight_current_line()

        self._chunk_line = 1
        self._highlight_job = self.editor.after(50, self._highlight_chunk)


    def _highlight_current_line(self):
        index = self.editor.index("insert")
        line = index.split(".")[0]
        start = f"{line}.0"
        end = f"{line}.end"

        text = self.editor.get(start, end)

        ext = os.path.splitext(self.current_file or "")[1].lower()
        rules = self.HIGHLIGHT_RULES.get(ext, self.HIGHLIGHT_RULES[".py"])
        colors = rules["colors"]

        for tag in colors:
            self.editor.tag_remove(tag, start, end)

        def apply(pattern, tag, flags=0):
            for match in re.finditer(pattern, text, flags):
                self.editor.tag_add(
                    tag,
                    f"{start}+{match.start()}c",
                    f"{start}+{match.end()}c",
                )
    
        if ext == ".py":
            apply(r"#.*", "comment")
        else:
            apply(r"//.*", "comment")
            apply(r"/\*[\s\S]*?\*/", "comment", re.DOTALL)

        apply(r"(['\"]{3})([\s\S]*?)\1", "string", re.DOTALL)
        apply(r"(['\"])(?:(?=(\\?))\2.)*?\1", "string")
        apply(r"\b\d+(\.\d+)?\b", "number")
        apply(r"[+\-*/%=<>!~&|^]+", "operator")
    
        for token_type in ("keywords", "datatypes", "builtins", "booleans"):
            for word in rules.get(token_type, []):
                apply(rf"\b{re.escape(word)}\b", token_type[:-1])

        apply(r"class\s+([A-Za-z_]\w*)", "class")
        apply(r"def\s+([A-Za-z_]\w*)", "function")
        apply(r"function\s+([A-Za-z_]\w*)", "function")


    def _highlight_chunk(self, chunk_size=1000):
        total_lines = int(self.editor.index("end-1c").split(".")[0])

        if self._chunk_line > total_lines:
            return 

        start = self._chunk_line
        end = min(start + chunk_size - 1, total_lines)

        start_index = f"{start}.0"
        end_index = f"{end}.0"
        text = self.editor.get(start_index, end_index)

        ext = os.path.splitext(self.current_file or "")[1].lower()
        rules = self.HIGHLIGHT_RULES.get(ext, self.HIGHLIGHT_RULES[".py"])
        colors = rules["colors"]

        for tag, color in colors.items():
            self.editor.tag_config(tag, foreground=color)
            self.editor.tag_remove(tag, start_index, end_index)

        def apply(pattern, tag, flags=0):
            for match in re.finditer(pattern, text, flags):
                self.editor.tag_add(
                    tag,
                    f"{start_index}+{match.start()}c",
                    f"{start_index}+{match.end()}c"
                )

        if ext == ".py":
            apply(r"#.*", "comment")
        else:
            apply(r"//.*", "comment")
            apply(r"/\*[\s\S]*?\*/", "comment", re.DOTALL)

        apply(r"(['\"]{3})([\s\S]*?)\1", "string", re.DOTALL)
        apply(r"(['\"])(?:(?=(\\?))\2.)*?\1", "string")
        apply(r"\b\d+(\.\d+)?\b", "number")
        apply(r"[+\-*/%=<>!~&|^]+", "operator")

        for token_type in ("keywords", "datatypes", "builtins", "booleans"):
            for word in rules.get(token_type, []):
                apply(rf"\b{re.escape(word)}\b", token_type[:-1])

        apply(r"class\s+([A-Za-z_]\w*)", "class")
        apply(r"def\s+([A-Za-z_]\w*)", "function")
        apply(r"function\s+([A-Za-z_]\w*)", "function")
        self._chunk_line = end + 1
        self._highlight_job = self.editor.after(500, self._highlight_chunk)

    def combined_key_release(self,event=None):

        self._highlight_current_line()

        if self._linecount_job is not None:
            try:
                self.root.after_cancel(self._linecount_job)
            except Exception:
                pass
        self._linecount_job = self.root.after(100, self.update_line_count)

        return "break"
    
    def Login_info(self):
        if os.path.exists(self.log_path):
            try:
                os.startfile(self.log_path)
            except:
                messagebox.showerror("Error", "Problem in Showing Log file")

    def show_popup(self, title, message, font_name="Arial", font_size=14):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        try:
            popup.iconbitmap("icon/lide.ico")
        except:
            pass
        popup.resizable(False, False)
        popup.configure(bg="gray20")
    
        popup.transient(self.root)
        popup.grab_set()

        label = tk.Label(
            popup,
            text=message,
            font=("Consolas", font_size),
            justify="left",
            wraplength=450,
            bg="gray20",
            fg="white" 
        )
        label.pack(padx=30, pady=20)

        ok_button = tk.Button(
            popup,
            text="OK",
            font=("Arial", font_size),
            bg="#0078D7",
            fg="white",
            activebackground="#005A9E",
            activeforeground="white",
            relief="flat",
            command=popup.destroy
        )
        ok_button.pack(pady=(0, 20), ipadx=10, ipady=5)

        popup.update_idletasks()
        w = popup.winfo_width()
        h = popup.winfo_height()
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        self.root.wait_window(popup)
        
    def check_new_version_features(self):
        os.makedirs(os.path.dirname(self.about_path), exist_ok=True)
        if not os.path.exists(self.about_path):
            open(self.about_path, "w").close()

        with open(self.about_path, "r+") as f:
            current_version = f.read().strip()

            if current_version != "v3.0.0_stable":
                f.seek(0)
                f.truncate()
                f.write("v3.0.0_stable")
                f.flush()

                self.show_popup(
                    "New Version v3.0.0_stable",
                    """LIDE v3.0.0_stable Features

In this new version, you will get:
1) Chunk Syntax Highlighter
2) In-Built Terminal :- Ctrl + , 
3) Bug Fixes with Responsive UI
4) Multifile Management in one session
5) Update System Improvement
6) Select And Replace keywords
7) More Control Over Widgets by\n    (Settings > Preferences)
8) Fetch Data From Static Html Websites
9) Better File Management
10) Built In Explorer with (file , folder) create and delete options.""",
                    font_size=14
                )
    
    def mit_license(self):
        self.show_popup(
            "MIT License",
            """MIT License

Copyright (c) [2025] [Moinak Debnath]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE""",
            font_size=11
        )

    def About_section(self):
        self.show_popup(
            "About",
            """LIDE is a Simple Text Editor
  It is specially designed for:-\n
1) Less RAM usage
2) Fast startup
3) Begginners
4) With Modern Features like:- 
   Syntax Highlighting
   Plugin System 
   Terminal 
   Explorer 
   Preview Pane
   Auto Indent.
""",
            font_size=14
        )

    def Shortcuts_section(self):
        self.show_popup(
            "Shortcuts",
            """Shortcuts are listed below:
1) SAVE FILE - Ctrl + S
2) NEW FILE - Ctrl + N
3) OPEN FILE - Ctrl + O
4) Terminal - Ctrl + ,""",
            font_size=14
        )
        
    def on_editor_mousewheel(self,event):
        ctrl_pressed = (event.state & 0x4) != 0 
    
        if ctrl_pressed:
            if hasattr(event, 'delta'):
                self.zoom += 1 if event.delta > 0 else -1
            else:
                if event.num == 4:
                    self.zoom += 1
                elif event.num == 5:
                    self.zoom -= 1
    
            self.zoom = max(5, min(self.zoom, 70))
            with open(self.zoom_in_appdata, "w") as f:
                f.write(str(self.zoom))
    
            self.editor.configure(font=("Consolas", self.zoom))
            if self.line_numbers:
                self.line_numbers.configure(font=("Consolas", self.zoom))
            self.update_line_numbers()
            return "break"
        else:
            if hasattr(event, 'delta'):
                scroll_units = int(-1 * (event.delta / 120))
                self.editor.yview_scroll(scroll_units, "units")
                self.line_numbers.yview_scroll(scroll_units, "units")
            else:
                if event.num == 4:
                    self.editor.yview_scroll(-1, "units")
                    self.line_numbers.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.editor.yview_scroll(1, "units")
                    self.line_numbers.yview_scroll(1, "units")
    
            editor_fraction = self.editor.yview()
            self.scrollbar.set(editor_fraction[0], editor_fraction[1])
            return "break"
            
LIDE = lide()
LIDE.main()
LIDE.preview()
LIDE.explorer()
LIDE.check_new_version_features()
LIDE.root.after(1000, lambda: LIDE.plugin())
LIDE.root.after(50, lambda: LIDE.check_update())
LIDE.root.after(100, lambda: LIDE.root.state("zoomed"))
LIDE.editor.bind("<MouseWheel>", lambda e: LIDE.on_editor_mousewheel(e))
LIDE.editor.bind("<Button-4>", lambda e: LIDE.on_editor_mousewheel(e))
LIDE.editor.bind("<Button-5>", lambda e: LIDE.on_editor_mousewheel(e))
LIDE.root.bind("<Control-s>", lambda e: LIDE.save_file())
LIDE.root.bind("<Control-n>", lambda e: LIDE.new_file())
LIDE.root.bind("<Control-o>", lambda e: LIDE.open_file())
LIDE.root.bind("<Control-,>", lambda e: LIDE.terminal_cli())
LIDE.editor.bind("<<Modified>>", LIDE.on_text_change)
LIDE.editor.bind("<<Paste>>", lambda e: LIDE.root.after(100,LIDE.highlight_syntax()))
LIDE.editor.bind("<<Cut>>", lambda e: LIDE.highlight_syntax()) 
LIDE.editor.bind("<KeyRelease>", LIDE.combined_key_release, add="+")
LIDE.editor.bind("<BackSpace>", lambda e: LIDE.update_line_numbers())
LIDE.editor.bind("<Configure>", lambda e: LIDE.update_line_numbers())
LIDE.editor.bind("<Return>", LIDE.auto_indent, add="+")
LIDE.editor.bind("<Control-z>", lambda e: LIDE.editor.event_generate("<<Undo>>"))
LIDE.editor.bind("<Control-y>", lambda e: LIDE.editor.event_generate("<<Redo>>"))
LIDE.root.protocol("WM_DELETE_WINDOW", LIDE.on_close)
LIDE.root.mainloop()