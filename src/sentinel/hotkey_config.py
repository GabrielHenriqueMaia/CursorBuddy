"""Configuração simples de hotkey para o CursorBuddy."""
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

HOTKEY_FILE = os.path.join(os.path.dirname(__file__), os.pardir, "format_hotkey.ahk")

DEFAULT_HOTKEY = "^!f"


def render_ahk(hotkey: str) -> str:
    return f"; AutoHotkey script gerado pelo CursorBuddy\n" \
           f"; Pressione {hotkey} para abrir o panel de formatação\n" \
           f"SetWorkingDir, %A_ScriptDir%\n" \
           f"{hotkey}::\n" \
           f"    Run, %A_ScriptDir%\\run.bat format --always-on-top, , Hide\n" \
           f"    Return\n"


class HotkeyConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CursorBuddy Hotkey Config")
        self.geometry("460x220")
        self.resizable(False, False)
        self.configure(bg="#f5f7fb")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Card.TFrame", background="#f5f7fb")
        self.style.configure("Header.TLabel", background="#f5f7fb", foreground="#0f172a", font=("Segoe UI Semibold", 14))
        self.style.configure("Normal.TLabel", background="#f5f7fb", foreground="#334155", font=("Segoe UI", 10))
        self.style.configure("Action.TButton", font=("Segoe UI", 10), padding=8)
        self.style.configure("Entry.TEntry", fieldbackground="#ffffff", foreground="#0f172a", padding=5)

        frame = ttk.Frame(self, style="Card.TFrame", padding=(18, 16, 18, 18))
        frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(frame, text="Hotkey Config", style="Header.TLabel")
        header.pack(anchor=tk.W)

        subtitle = ttk.Label(frame, text="Escolha a hotkey para abrir o painel de formatação.", style="Normal.TLabel")
        subtitle.pack(anchor=tk.W, pady=(6, 14))

        entry_frame = ttk.Frame(frame, style="Card.TFrame")
        entry_frame.pack(fill=tk.X)

        label = ttk.Label(entry_frame, text="Hotkey (AutoHotkey format):", style="Normal.TLabel")
        label.pack(anchor=tk.W)

        self.hotkey_var = tk.StringVar(value=DEFAULT_HOTKEY)
        self.entry = ttk.Entry(entry_frame, textvariable=self.hotkey_var, style="Entry.TEntry", width=28)
        self.entry.pack(anchor=tk.W, pady=(6, 12))

        self.save_btn = ttk.Button(frame, text="Salvar hotkey", style="Action.TButton", command=self.save_hotkey)
        self.save_btn.pack(anchor=tk.W)

        self.status_label = ttk.Label(frame, text="", style="Normal.TLabel")
        self.status_label.pack(anchor=tk.W, pady=(12, 0))

        self.load_hotkey()

    def load_hotkey(self):
        try:
            with open(HOTKEY_FILE, "r", encoding="utf-8") as fh:
                data = fh.read()
            first_line = next((line for line in data.splitlines() if "::" in line), None)
            if first_line:
                hotkey = first_line.split("::", 1)[0].strip()
                self.hotkey_var.set(hotkey)
        except FileNotFoundError:
            self.hotkey_var.set(DEFAULT_HOTKEY)
        except Exception:
            self.hotkey_var.set(DEFAULT_HOTKEY)

    def save_hotkey(self):
        hotkey = self.hotkey_var.get().strip()
        if not hotkey:
            messagebox.showwarning("Aviso", "Digite uma hotkey válida.")
            return
        try:
            content = render_ahk(hotkey)
            with open(HOTKEY_FILE, "w", encoding="utf-8") as fh:
                fh.write(content)
            self.status_label.config(text=f"Hotkey gravada: {hotkey}")
            messagebox.showinfo("Salvo", "Hotkey salva com sucesso em format_hotkey.ahk")
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))


def main():
    app = HotkeyConfigApp()
    app.mainloop()


if __name__ == "__main__":
    main()
