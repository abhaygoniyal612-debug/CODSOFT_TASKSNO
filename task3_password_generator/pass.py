"""
Konoha Password Forge
----------------------
A Naruto-themed password generator built with Python's Tkinter.

Run with:  python naruto_password_generator.py
(Tkinter ships with standard Python installs, so no extra packages needed.)
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import string
import secrets

# ---------------------------------------------------------------------------
# Theme colors — inspired by Naruto's outfit, the Konoha leaf, and Sharingan
# ---------------------------------------------------------------------------
BG_DARK = "#1a1410"        # near-black, like night in the Hidden Leaf
ORANGE = "#FF7800"         # Naruto's jumpsuit orange
ORANGE_DARK = "#CC5F00"
LEAF_GREEN = "#3C7A3C"     # Konoha leaf green
SHARINGAN_RED = "#C8102E"
CREAM = "#F5E6C8"          # scroll parchment color
WHITE = "#FFF7EC"

PASSWORD_CHARS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digits": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{};:,.<>?/",
}


def pick_font(preferred, fallback="Arial"):
    """Return a font family name if it's installed, else fall back."""
    available = set(tkfont.families())
    return preferred if preferred in available else fallback


def generate_password(length, use_lower, use_upper, use_digits, use_symbols):
    pool = ""
    guaranteed = []
    if use_lower:
        pool += PASSWORD_CHARS["lower"]
        guaranteed.append(secrets.choice(PASSWORD_CHARS["lower"]))
    if use_upper:
        pool += PASSWORD_CHARS["upper"]
        guaranteed.append(secrets.choice(PASSWORD_CHARS["upper"]))
    if use_digits:
        pool += PASSWORD_CHARS["digits"]
        guaranteed.append(secrets.choice(PASSWORD_CHARS["digits"]))
    if use_symbols:
        pool += PASSWORD_CHARS["symbols"]
        guaranteed.append(secrets.choice(PASSWORD_CHARS["symbols"]))

    if not pool:
        raise ValueError("Select at least one character type, believe it!")
    if length < len(guaranteed):
        raise ValueError(f"Length must be at least {len(guaranteed)} for the selected options.")

    remaining = [secrets.choice(pool) for _ in range(length - len(guaranteed))]
    result = guaranteed + remaining
    # shuffle securely so guaranteed chars aren't always at the front
    for i in range(len(result) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        result[i], result[j] = result[j], result[i]
    return "".join(result)


class KonohaPasswordForge(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🍥 Konoha Password Forge")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)

        title_font_name = pick_font("Impact", "Arial Black")
        header_font = tkfont.Font(family=title_font_name, size=22, weight="bold")
        label_font = tkfont.Font(family=pick_font("Verdana"), size=11, weight="bold")
        entry_font = tkfont.Font(family="Consolas", size=14, weight="bold")
        button_font = tkfont.Font(family=pick_font("Verdana"), size=12, weight="bold")

        container = tk.Frame(self, bg=BG_DARK, padx=24, pady=20)
        container.pack()

        # --- Header, styled like the Konoha headband ---
        header = tk.Label(
            container, text="🍥 KONOHA PASSWORD FORGE 🍥",
            font=header_font, fg=ORANGE, bg=BG_DARK
        )
        header.pack(pady=(0, 4))

        subtitle = tk.Label(
            container, text="Believe it! Forge a password worthy of the Hokage.",
            font=(pick_font("Verdana"), 10, "italic"), fg=LEAF_GREEN, bg=BG_DARK
        )
        subtitle.pack(pady=(0, 16))

        # --- Length input ---
        length_frame = tk.Frame(container, bg=BG_DARK)
        length_frame.pack(fill="x", pady=6)
        tk.Label(length_frame, text="Password Length:", font=label_font,
                 fg=WHITE, bg=BG_DARK).pack(side="left")
        self.length_var = tk.IntVar(value=12)
        length_spin = tk.Spinbox(
            length_frame, from_=4, to=64, textvariable=self.length_var,
            width=5, font=label_font, bg=CREAM, fg=BG_DARK,
            buttonbackground=ORANGE, relief="flat", justify="center"
        )
        length_spin.pack(side="right")

        # --- Complexity checkboxes ---
        options_frame = tk.LabelFrame(
            container, text=" Jutsu Ingredients ", font=label_font,
            fg=SHARINGAN_RED, bg=BG_DARK, bd=2, labelanchor="n"
        )
        options_frame.pack(fill="x", pady=12)

        self.use_lower = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        checks = [
            ("Lowercase (a-z)", self.use_lower),
            ("Uppercase (A-Z)", self.use_upper),
            ("Numbers (0-9)", self.use_digits),
            ("Symbols (!@#$...)", self.use_symbols),
        ]
        for text, var in checks:
            cb = tk.Checkbutton(
                options_frame, text=text, variable=var, font=label_font,
                fg=WHITE, bg=BG_DARK, selectcolor=BG_DARK,
                activebackground=BG_DARK, activeforeground=ORANGE,
                anchor="w"
            )
            cb.pack(fill="x", padx=10, pady=2)

        # --- Generate button ---
        generate_btn = tk.Button(
            container, text="🔥 Summon Password! 🔥", font=button_font,
            bg=ORANGE, fg=BG_DARK, activebackground=ORANGE_DARK,
            activeforeground=WHITE, relief="flat", padx=10, pady=8,
            command=self.on_generate, cursor="hand2"
        )
        generate_btn.pack(fill="x", pady=(10, 14))

        # --- Result display, styled like a scroll ---
        result_frame = tk.Frame(container, bg=CREAM, bd=3, relief="ridge")
        result_frame.pack(fill="x")
        self.result_var = tk.StringVar(value="Your password will appear here")
        result_label = tk.Entry(
            result_frame, textvariable=self.result_var, font=entry_font,
            fg=BG_DARK, bg=CREAM, justify="center", relief="flat",
            state="readonly", readonlybackground=CREAM
        )
        result_label.pack(fill="x", padx=8, pady=10)

        copy_btn = tk.Button(
            container, text="📋 Copy to Clipboard", font=(pick_font("Verdana"), 10, "bold"),
            bg=LEAF_GREEN, fg=WHITE, relief="flat", padx=6, pady=4,
            command=self.on_copy, cursor="hand2"
        )
        copy_btn.pack(pady=(10, 0))

        footer = tk.Label(
            container, text="Made in the Hidden Leaf Village 🍃",
            font=(pick_font("Verdana"), 8), fg=ORANGE_DARK, bg=BG_DARK
        )
        footer.pack(pady=(16, 0))

    def on_generate(self):
        try:
            password = generate_password(
                self.length_var.get(),
                self.use_lower.get(),
                self.use_upper.get(),
                self.use_digits.get(),
                self.use_symbols.get(),
            )
            self.result_var.set(password)
        except ValueError as e:
            messagebox.showerror("Jutsu Failed!", str(e))

    def on_copy(self):
        password = self.result_var.get()
        if not password or password == "Your password will appear here":
            messagebox.showwarning("Nothing to copy", "Generate a password first!")
            return
        self.clipboard_clear()
        self.clipboard_append(password)
        messagebox.showinfo("Copied!", "Password copied to clipboard, believe it!")


if __name__ == "__main__":
    app = KonohaPasswordForge()
    app.mainloop()