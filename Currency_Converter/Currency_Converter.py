import requests
import tkinter as tk
from tkinter import ttk, messagebox

# --- Colors & Fonts ---
BG = "#0f1f0f"
CARD = "#162716"
GREEN_DARK = "#1a3a1a"
GOLD = "#c9a84c"
GOLD_LIGHT = "#e8c97a"
TEXT = "#f0f0f0"
MUTED = "#7a9a7a"
FONT_TITLE = ("Times New Roman", 22, "bold")
FONT_LABEL = ("Times New Roman", 10)
FONT_INPUT = ("Times New Roman", 13)
FONT_RESULT = ("Times New Roman", 15, "bold")
FONT_BTN = ("Times New Roman", 12, "bold")


def currency_converter(amount, from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('result') == 'error':
            return None, data.get('error-type', 'Unknown error')
        conversion_rate = data['rates'][to_currency]
        converted_amount = round(amount * conversion_rate)
        return converted_amount, None
    except requests.exceptions.RequestException as e:
        return None, str(e)
    except KeyError:
        return None, f"Currency code not found"


def convert():
    from_cur = from_var.get().strip().upper()
    to_cur = to_var.get().strip().upper()
    amount_str = amount_entry.get().strip()

    if not amount_str or not from_cur or not to_cur:
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return

    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Please enter a valid number.")
        return

    result_label.config(text="Converting...", foreground=MUTED)
    root.update()

    result, error = currency_converter(amount, from_cur, to_cur)

    if error:
        result_label.config(text=f"Error: {error}", foreground="#e05555")
    else:
        result_label.config(
            text=f"{amount:,.0f} {from_cur}  =  {result:,} {to_cur}",
            foreground=GOLD_LIGHT
        )


# --- Root Window ---
root = tk.Tk()
root.title("Currency Converter")
root.geometry("800x700")
root.resizable(False, False)
root.configure(bg=BG)

# --- Title Bar ---
title_frame = tk.Frame(root, bg=GOLD, height=4)
title_frame.pack(fill="x")

tk.Label(root, text="💱 Currency Converter", font=FONT_TITLE,
         bg=BG, fg=GOLD).pack(pady=(22, 4))
tk.Label(root, text="Powered by open.er-api.com", font=("Times New Roman", 8),
         bg=BG, fg=MUTED).pack(pady=(0, 18))

# --- Card Frame ---
card = tk.Frame(root, bg=CARD, padx=30, pady=24,
                highlightbackground=GREEN_DARK, highlightthickness=1)
card.pack(padx=30, fill="x")

# Amount
tk.Label(card, text="AMOUNT", font=FONT_LABEL, bg=CARD, fg=MUTED).grid(
    row=0, column=0, sticky="w", pady=(0, 4))
amount_entry = tk.Entry(card, font=FONT_INPUT, bg=GREEN_DARK, fg=TEXT,
                        insertbackground=GOLD, relief="flat",
                        highlightbackground=GOLD, highlightthickness=1, width=18)
amount_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14), ipady=6)

# From / To
tk.Label(card, text="FROM", font=FONT_LABEL, bg=CARD, fg=MUTED).grid(
    row=2, column=0, sticky="w")
tk.Label(card, text="TO", font=FONT_LABEL, bg=CARD, fg=MUTED).grid(
    row=2, column=1, sticky="w", padx=(12, 0))

from_var = tk.StringVar(value="USD")
to_var = tk.StringVar(value="EUR")

from_entry = tk.Entry(card, textvariable=from_var, font=FONT_INPUT,
                      bg=GREEN_DARK, fg=TEXT, insertbackground=GOLD,
                      relief="flat", highlightbackground=GOLD,
                      highlightthickness=1, width=8)
from_entry.grid(row=3, column=0, sticky="w", ipady=6, pady=(4, 0))

to_entry = tk.Entry(card, textvariable=to_var, font=FONT_INPUT,
                    bg=GREEN_DARK, fg=TEXT, insertbackground=GOLD,
                    relief="flat", highlightbackground=GOLD,
                    highlightthickness=1, width=8)
to_entry.grid(row=3, column=1, sticky="w", padx=(12, 0), ipady=6, pady=(4, 0))

card.columnconfigure(0, weight=1)
card.columnconfigure(1, weight=1)

# --- Convert Button ---
btn = tk.Button(root, text="CONVERT", font=FONT_BTN,
                bg=GOLD, fg="#0f1f0f", activebackground=GOLD_LIGHT,
                activeforeground="#0f1f0f", relief="flat",
                cursor="hand2", command=convert, padx=20, pady=8)
btn.pack(pady=20)

# Bind Enter key
root.bind("<Return>", lambda e: convert())

# --- Result ---
result_label = tk.Label(root, text="—", font=FONT_RESULT,
                        bg=BG, fg=MUTED, wraplength=400)
result_label.pack()

root.mainloop()