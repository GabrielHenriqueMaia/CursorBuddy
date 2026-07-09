"""Simple formatter panel: lê JSON/XML da área de transferência (ou stdin)
e exibe em um painel Tkinter com formatação.
"""
import sys
import json
import tkinter as tk
import tkinter.scrolledtext as st
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


def show_panel(formatted: str, title: str = "Formatted Data") -> None:
    root = tk.Tk()
    root.title(title)
    root.geometry("900x600")

    text = st.ScrolledText(root, wrap=tk.NONE, font=("Consolas", 11))
    text.insert("1.0", formatted)
    text.configure(state=tk.DISABLED)
    text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


def main():
    raw = get_input_text()
    if not raw or not raw.strip():
        print("No input detected.")
        return

    formatted = try_format_json(raw)
    if formatted:
        show_panel(formatted, title="Formatted JSON")
        return

    formatted = try_format_xml(raw)
    if formatted:
        show_panel(formatted, title="Formatted XML")
        return

    # Default: show raw
    show_panel(raw, title="Raw Content")


if __name__ == "__main__":
    main()
