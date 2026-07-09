"""Simple formatter panel: lê JSON/XML da área de transferência (ou stdin)
e exibe em um painel Tkinter com formatação.
"""
import sys
import json
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.ttk as ttk
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
    root.geometry("980x640")
    root.minsize(860, 520)
    root.configure(bg="#f7f8fb")
    root.attributes("-topmost", bool(always_on_top))

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Card.TFrame", background="#f7f8fb")
    style.configure("Header.TLabel", background="#f7f8fb", foreground="#111827", font=("Segoe UI Semibold", 16))
    style.configure("SubHeader.TLabel", background="#f7f8fb", foreground="#6b7280", font=("Segoe UI", 10))
    style.configure("Action.TButton", font=("Segoe UI", 10), padding=8)
    style.configure("Toggle.TCheckbutton", background="#f7f8fb", foreground="#111827", font=("Segoe UI", 10))
    style.configure("Status.TLabel", background="#eef2ff", foreground="#1e3a8a", font=("Segoe UI", 9), padding=6)

    header = ttk.Frame(root, style="Card.TFrame", padding=(18, 16, 18, 10))
    header.pack(fill=tk.X)

    title_label = ttk.Label(header, text=title, style="Header.TLabel")
    title_label.pack(anchor=tk.W)

    subtitle = ttk.Label(
        header,
        text="JSON/XML formatter panel — copie, salve ou mantenha sempre visível.",
        style="SubHeader.TLabel",
    )
    subtitle.pack(anchor=tk.W, pady=(6, 0))

    ctrl = ttk.Frame(root, style="Card.TFrame", padding=(14, 10))
    ctrl.pack(fill=tk.X, padx=18, pady=(0, 6))

    def set_status(message: str) -> None:
        status_label.config(text=message)

    def do_copy():
        try:
            value = text.get("1.0", tk.END)
            if pyperclip:
                pyperclip.copy(value)
            else:
                root.clipboard_clear()
                root.clipboard_append(value)
            set_status("Conteúdo copiado para a área de transferência.")
        except Exception as exc:
            messagebox.showerror("Copy failed", str(exc))
            set_status("Falha ao copiar.")

    def do_save():
        try:
            fn = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*")],
                title="Salvar conteúdo formatado",
            )
            if not fn:
                set_status("Salvamento cancelado.")
                return
            with open(fn, "w", encoding="utf-8") as fh:
                fh.write(text.get("1.0", tk.END).rstrip() + "\n")
            messagebox.showinfo("Saved", f"Saved to {fn}")
            set_status(f"Salvo em {fn}")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))
            set_status("Falha ao salvar.")

    def do_close():
        root.destroy()

    copy_btn = ttk.Button(ctrl, text="Copy", style="Action.TButton", command=do_copy)
    copy_btn.pack(side=tk.LEFT, padx=(0, 8))

    save_btn = ttk.Button(ctrl, text="Save", style="Action.TButton", command=do_save)
    save_btn.pack(side=tk.LEFT, padx=(0, 8))

    close_btn = ttk.Button(ctrl, text="Close", style="Action.TButton", command=do_close)
    close_btn.pack(side=tk.LEFT, padx=(0, 8))

    top_var = tk.BooleanVar(value=bool(always_on_top))

    def toggle_top() -> None:
        root.attributes("-topmost", bool(top_var.get()))
        set_status("Always on top: " + ("enabled" if top_var.get() else "disabled"))

    top_cb = ttk.Checkbutton(ctrl, text="Always on top", variable=top_var, command=toggle_top, style="Toggle.TCheckbutton")
    top_cb.pack(side=tk.LEFT, padx=(0, 8))

    text_frame = ttk.Frame(root, style="Card.TFrame")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 8))

    text = tk.Text(
        text_frame,
        wrap=tk.NONE,
        font=("Consolas", 11),
        background="#0f172a",
        foreground="#f8fafc",
        insertbackground="#f8fafc",
        relief=tk.FLAT,
        padx=12,
        pady=12,
    )
    text.insert("1.0", formatted)
    text.configure(state=tk.NORMAL)
    text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text.config(yscrollcommand=scrollbar.set)

    status_bar = ttk.Frame(root, style="Card.TFrame", padding=(18, 0, 18, 8))
    status_bar.pack(fill=tk.X)
    status_label = ttk.Label(status_bar, text="Ready", style="Status.TLabel")
    status_label.pack(fill=tk.X)

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

    show_panel(raw, title="Raw Content", always_on_top=always_on_top)


if __name__ == "__main__":
    main()
