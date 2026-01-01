import tkinter as tk
import customtkinter as ctk
import io, sys, os, tempfile, subprocess, threading, queue, time
from functools import partial
from pathlib import Path
import traceback
import ast

compatible_version = "v3.0.0_stable"

def auto_close_brackets(event, LIDE):
    if LIDE.current_file is None: return
    if Path(LIDE.current_file).suffix != ".py": return
    if event.keysym in ("BackSpace", "Delete", "Return", "Tab"): return
    try:
        if LIDE.editor.tag_ranges("sel"): return
    except: pass
    pairs = {"(": ")", "[": "]", "{": "}", '"': '"', "'": "'"}
    char = event.char
    if char in pairs:
        LIDE.editor.insert("insert", pairs[char])
        LIDE.editor.mark_set("insert", "insert -1c")

def auto_completion(event, LIDE):
    if LIDE.current_file is None: return
    if Path(LIDE.current_file).suffix != ".py": return
    if event.keysym != "space":
        return
    
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
        cursor_index = LIDE.editor.index("insert")
        line_index = cursor_index.split(".")[0]
        line_start = f"{line_index}.0"
        text_before_cursor = LIDE.editor.get(line_start, cursor_index).rstrip()
        words = text_before_cursor.split()
        last_word = words[-1] if words else ""

        if last_word in snippets:
            leading_spaces = len(text_before_cursor) - len(text_before_cursor.lstrip())
            indent = " " * leading_spaces
            start_idx = f"{line_index}.{len(text_before_cursor) - len(last_word)}"
            LIDE.editor.delete(start_idx, cursor_index)
            snippet_lines = snippets[last_word].split("\n")
            snippet_lines = [snippet_lines[0]] + [indent + line for line in snippet_lines[1:]]
            snippet = "\n".join(snippet_lines)
            LIDE.editor.insert(start_idx, snippet)
            LIDE.editor.mark_set("insert", f"{start_idx}+{len(snippet)}c")

    LIDE.editor.after_idle(replace_snippet)

def start(LIDE):
    LIDE.editor.bind("<Key>", lambda e: auto_close_brackets(e, LIDE), add="+")
    LIDE.editor.bind("<Key>", lambda e: auto_completion(e, LIDE), add="+")
    
def setup_plugin(LIDE):
    print("Python Plugin Loaded (Terminal Removed - F5 only)")
    LIDE.root.after(500, lambda: start(LIDE))