"""Simple formatter panel: lê JSON/XML da área de transferência (ou stdin)
e exibe em um painel Tkinter com formatação.
"""
import sys
import json
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import filedialog, messagebox
from typing import Optional

try:
    import pyperclip
except Exception:
    pyperclip = None


def try_format_json(text: str) -> Optional[str]:
    try:
        obj = json.loads(text)
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception:
        return None


def try_format_xml(text: str) -> Optional[str]:
    try:
        from xml.dom import minidom

        dom = minidom.parseString(text)
        return dom.toprettyxml(indent="  ")
    except Exception:
        return None


def get_input_text() -> str:
    # Prefer clipboard if available and non-empty
    if pyperclip:
        try:
            data = pyperclip.paste()
            if data and data.strip():
                return data
        except Exception:
            pass

    # Else, read from stdin if piped
    if not sys.stdin.isatty():
        return sys.stdin.read()

    # Fallback: prompt the user to paste into stdin
    print("Paste JSON or XML content, then press Ctrl-D (Ctrl-Z on Windows) to end:")
    return sys.stdin.read()


def show_panel(formatted: str, title: str = "Formatted Data", always_on_top: bool = False) -> None:
    root = tk.Tk()
    root.title(title)
    root.geometry("900x600")
    root.attributes("-topmost", bool(always_on_top))

    # Top controls frame
    ctrl = tk.Frame(root)
    ctrl.pack(fill=tk.X, padx=6, pady=6)

    def do_copy():
        try:
            if pyperclip:
                pyperclip.copy(text.get("1.0", tk.END))
            else:
                root.clipboard_clear()
                root.clipboard_append(text.get("1.0", tk.END))
            messagebox.showinfo("Copied", "Content copied to clipboard")
        except Exception as e:
            messagebox.showerror("Copy failed", str(e))

    def do_save():
        try:
            fn = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*")] ,
            )
            if not fn:
                return
            with open(fn, "w", encoding="utf-8") as fh:
                fh.write(text.get("1.0", tk.END))
            messagebox.showinfo("Saved", f"Saved to {fn}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))

    def do_close():
        root.destroy()

    copy_btn = tk.Button(ctrl, text="Copy", command=do_copy)
    copy_btn.pack(side=tk.LEFT, padx=4)

    save_btn = tk.Button(ctrl, text="Save", command=do_save)
    save_btn.pack(side=tk.LEFT, padx=4)

    close_btn = tk.Button(ctrl, text="Close", command=do_close)
    close_btn.pack(side=tk.LEFT, padx=4)

    top_var = tk.BooleanVar(value=bool(always_on_top))

    def toggle_top():
        root.attributes("-topmost", bool(top_var.get()))

    top_cb = tk.Checkbutton(ctrl, text="Always on top", variable=top_var, command=toggle_top)
    top_cb.pack(side=tk.LEFT, padx=10)

    # Text area
    text = st.ScrolledText(root, wrap=tk.NONE, font=("Consolas", 11))
    text.insert("1.0", formatted)
    text.configure(state=tk.NORMAL)
    text.pack(fill=tk.BOTH, expand=True)

    # Start mainloop
    root.mainloop()


def main(always_on_top: bool = False):
    raw = get_input_text()
    if not raw or not raw.strip():
        print("No input detected.")
        return

    formatted = try_format_json(raw)
    if formatted:
        show_panel(formatted, title="Formatted JSON", always_on_top=always_on_top)
        return

    formatted = try_format_xml(raw)
    if formatted:
        show_panel(formatted, title="Formatted XML", always_on_top=always_on_top)
        return

    # Default: show raw
    show_panel(raw, title="Raw Content", always_on_top=always_on_top)


if __name__ == "__main__":
    main()
