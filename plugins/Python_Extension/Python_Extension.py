import tkinter as tk
import customtkinter as ctk
import io, sys
import threading
from functools import partial
import builtins as py_builtins
from pathlib import Path
import traceback
import re

class PythonPlugin:
    def __init__(self):
        self.name = "python_extension"
        self.gui_keywords = [
            "pygame", "arcade", "pyglet", "kivy", "cocos2d", "panda3d", "ursina",
            "moderngl", "pyopengl", "tk.", "tkinter", "ctk.", "customtkinter",
            "Toplevel", "Label", "Button", "Entry", "PyQt4", "PyQt5", "PyQt6",
            "PySide", "PySide2", "PySide6", "QtWidgets", "QMainWindow", "wx.",
            "wxFrame", "wx.Panel", "wx.App", "DearPyGui", "dpg.", "dpg.add_window",
            "matplotlib", "plt.show", "FigureCanvas", "NavigationToolbar2",
            "tkinter.ttk", "PySimpleGUI", "guizero", "kivy.app", "kivy.uix",
            "PyGameZero", "pgzero", "pygcurse", "vtk", "vispy", "glfw", "opengl",
            "mayavi"
        ]

    def run_code(self, IDE, event=None):
        if IDE.current_file is None:
            return
        filename = Path(IDE.current_file)
        if filename.suffix != ".py":
            return
        code = IDE.editor.get("1.0", "end-1c")
        if not code.strip():
            self._display_output(IDE, "There is no code written")
            return
        gui_detected = any(x in code for x in self.gui_keywords)
        if gui_detected:
            self._execute_code_main_thread(IDE, code)
        else:
            threading.Thread(target=self._execute_code_thread, args=(IDE, code), daemon=True).start()

    def _execute_code_thread(self, IDE, code):
        output = io.StringIO()
        old_stdout, old_stderr = sys.stdout, sys.stderr
        try:
            sys.stdout = output
            sys.stderr = output
            exec(code, {"IDE": IDE, "input": partial(self._gui_input, IDE), "__builtins__": py_builtins})
        except Exception:
            output.write(traceback.format_exc())
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        self._display_output(IDE, output.getvalue())

    def _execute_code_main_thread(self, IDE, code):
        output = io.StringIO()
        old_stdout, old_stderr = sys.stdout, sys.stderr
        try:
            sys.stdout = output
            sys.stderr = output
            IDE.plugin_python.configure(state="normal")
            IDE.plugin_python.delete("1.0", "end")
            IDE.plugin_python.configure(state="disabled")
            exec(code, {"IDE": IDE, "input": partial(self._gui_input, IDE), "__builtins__": py_builtins})
        except Exception:
            output.write(traceback.format_exc())
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        self._display_output(IDE, output.getvalue())

    def _gui_input(self, IDE, prompt=""):
        result = []
        event = threading.Event()
        def submit_input():
            result.append(input_box.get())
            try:
                popup.destroy()
            except:
                pass
            event.set()
        popup = ctk.CTkToplevel(IDE.root)
        popup.title("Input Required")
        tk.Label(popup, text=prompt).pack(pady=5)
        input_box = ctk.CTkEntry(popup)
        input_box.pack(pady=5)
        submit_btn = ctk.CTkButton(popup, text="Submit", command=submit_input)
        submit_btn.pack(pady=5)
        popup.protocol("WM_DELETE_WINDOW", submit_input)
        input_box.focus()
        popup.grab_set()
        event.wait()
        return result[0] if result else ""

    def _display_output(self, IDE, text):
        def update_gui():
            file_path = IDE.current_file
            printed = f"{file_path}:- {text}"
            IDE.plugin_python.configure(state="normal")
            IDE.plugin_python.delete("1.0", "end")
            IDE.plugin_python.insert("1.0", printed)
            IDE.plugin_python.configure(state="disabled")
            IDE.plugin_python.see("end")
        IDE.root.after(0, update_gui)

    def start_plugin(self, IDE):
        if IDE.current_file is None:
            return
        filename = Path(IDE.current_file)
        if filename.suffix != ".py":
            if getattr(IDE, "plugin_python", None):
                IDE.plugin_python.destroy()
                IDE.plugin_python = None
            if getattr(IDE, "run_code_button", None):
                IDE.run_code_button.destroy()
                IDE.run_code_button = None
            return
        if getattr(IDE, "plugin_python", None) is None:
            IDE.plugin_python = ctk.CTkTextbox(
                IDE.root, font=("Consolas", 10),
                fg_color=IDE.color, text_color=IDE.fg_color,
                wrap="none", height=200, state='disabled'
            )
            IDE.plugin_python.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        if getattr(IDE, "run_code_button", None) is None:
            IDE.run_code_button = ctk.CTkButton(
                IDE.root, text="Run Code for Python (F5)",
                command=partial(self.run_code, IDE)
            )
            IDE.run_code_button.grid(row=3, column=0, sticky="w", padx=5, pady=(0,5))
            
def auto_close_brackets(event, IDE):
    if IDE.current_file is None: return
    if Path(IDE.current_file).suffix != ".py": return
    if event.keysym in ("BackSpace", "Delete", "Return", "Tab"): return
    try:
        if IDE.editor.tag_ranges("sel"): return
    except: pass
    pairs = {"(": ")", "[": "]", "{": "}", '"': '"', "'": "'"}
    char = event.char
    if char in pairs:
        IDE.editor.insert("insert", pairs[char])
        IDE.editor.mark_set("insert", "insert -1c")

def auto_completion(event, IDE):
    if IDE.current_file is None: return
    if Path(IDE.current_file).suffix != ".py": return
    if event.keysym in ("BackSpace", "Delete", "Return", "Tab",
                        "Shift_L", "Shift_R", "Control_L", "Control_R"):
        return

    try:
        if IDE.editor.tag_ranges("sel"): return
    except: pass
    
    snippets = {
        "for": "for {var} in range({end}):\n    {body}",
        "while": "while {condition}:\n    {body}\n    {update}",
        "def": "def {function_name}({params}):\n    {body}",
        "class": "class {ClassName}:\n    def __init__(self, {params}):\n        {body}",
        "if": "if {condition}:\n    {body}",
        "elif": "elif {condition}:\n    {body}",
        "else": "else:\n    {body}",
        "try": "try:\n    {body}",
        "except": "except {ExceptionType} as {e}:\n    {body}",
        "finally": "finally:\n    {body}",
        "with": "with open('{filename}', '{mode}') as {file_var}:\n    {body}",
        "int": "int(",
        "input": "input(",
        "str": "str(",
        "lambda": "lambda {params}: {expression}",
        "yield": "yield {value}",
        "assert": "assert {condition}, '{message}'",
        "async": "async def {function_name}({params}):\n    {body}",
        "await": "await {coroutine}",
        "pass": "pass",
        "break": "break",
        "continue": "continue",
        "return": "return {value}"
    }


    def replace_snippet():
        cursor_index = IDE.editor.index("insert")
        line_index = cursor_index.split(".")[0]
        line_start = f"{line_index}.0"
        text_before_cursor = IDE.editor.get(line_start, cursor_index)
        words = text_before_cursor.split()
        last_word = words[-1] if words else ""

        if last_word in snippets:
            leading_spaces = len(text_before_cursor) - len(text_before_cursor.lstrip())
            indent = " " * leading_spaces
            start_index = f"{line_index}.{len(text_before_cursor) - len(last_word)}"
            IDE.editor.delete(start_index, cursor_index)
            snippet_lines = snippets[last_word].split("\n")
            snippet_lines = [snippet_lines[0]] + [indent + line for line in snippet_lines[1:]]
            snippet_text = "\n".join(snippet_lines)
            IDE.editor.insert(start_index, snippet_text)
            IDE.editor.mark_set("insert", f"{start_index}+{len(snippet_text)}c")

    IDE.editor.after_idle(replace_snippet)
    
def setup_plugin(IDE):
    plugin = PythonPlugin()
    IDE.root.after(100, lambda: IDE.root.state("zoomed"))
    print("Python Plugin Loaded")

    IDE.root.bind("<F5>", partial(plugin.run_code, IDE), add="+")
    IDE.editor.bind("<Key>", lambda e: auto_close_brackets(e, IDE))
    IDE.editor.bind("<Key>", lambda e: plugin.start_plugin(IDE))
    IDE.editor.bind("<Key>", lambda e: auto_completion(e, IDE))

    plugin.start_plugin(IDE)
