import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
# ---------- DATA MENU ----------
menu_items = {
    "Nasi Goreng": 15000,
    "Mie Ayam": 12000,
    "Ayam Geprek": 18000,
    "Es Teh": 5000,
    "Kopi Hitam": 8000,
    "Jus Alpukat": 12000,
    "Sate Ayam": 18000,
    "Daging Babi": 40000,
    "Jus pare": 12000,
}


# ---------- FUNCTION ----------
def hitung_total():
    subtotal = 0
    for item, var in qty_vars.items():
        jumlah = var.get()
        if jumlah > 0:
            subtotal += jumlah * menu_items[item]

    pajak = subtotal * 0.1
    diskon = subtotal * 0.05 if member_var.get() else 0
    total = subtotal + pajak - diskon
    

    lbl_subtotal_val.config(text=f"Rp {subtotal:,}") # type: ignore
    lbl_pajak_val.config(text=f"Rp {pajak:,}") # type: ignore
    lbl_diskon_val.config(text=f"Rp {diskon:,}") # type: ignore
    lbl_total_val.config(text=f"Rp {total:,}") # type: ignore
    return total, subtotal, pajak, diskon


def proses_transaksi():
    total, subtotal, pajak, diskon = hitung_total()
    try:
        bayar = int(entry_bayar.get())
    except ValueError:
        messagebox.showerror("Error", "Nominal pembayaran tidak valid!")
        return

    if bayar < total:
        messagebox.showwarning("Kurang", "Uang tidak cukup!")
        return

    kembalian = bayar - total
    lbl_kembalian_val.config(text=f"Rp {kembalian:,}") # type: ignore
    tampilkan_struk(subtotal, pajak, diskon, total, bayar, kembalian)


def tampilkan_struk(subtotal, pajak, diskon, total, bayar, kembalian):
    waktu = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    struk = []
    struk.append("STRUK PEMBAYARAN")
    struk.append(f"Waktu: {waktu}")
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for item, var in qty_vars.items():
        jml = var.get()
        if jml > 0:
            harga = menu_items[item]
            struk.append(f"{item:<15} x{jml} = Rp {harga*jml:,}")
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    struk.append(f"Subtotal : Rp {subtotal:,}")
    struk.append(f"Pajak 10%: Rp {pajak:,}")
    struk.append(f"Diskon   : Rp {diskon:,}")
    struk.append(f"Total    : Rp {total:,}")
    struk.append(f"Bayar    : Rp {bayar:,}")
    struk.append(f"Kembalian: Rp {kembalian:,}")
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    struk.append("Terima kasih telah berbelanja!")

    struk_text.delete(1.0, tk.END)
    struk_text.insert(tk.END, "\n".join(struk))

    nama_file = f"struk_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}."
    with open(nama_file, "w", encoding="utf-8") as f:
        f.write("\n".join(struk))
    print(f"Struk tersimpan: {nama_file}")


def reset():
    for var in qty_vars.values():
        var.set(0)
    entry_bayar.delete(0, tk.END)
    lbl_subtotal_val.config(text="-") # type: ignore
    lbl_pajak_val.config(text="-") # type: ignore
    lbl_diskon_val.config(text="-") # type: ignore
    lbl_total_val.config(text="-") # type: ignore
    lbl_kembalian_val.config(text="-") # type: ignore
    struk_text.delete(1.0, tk.END)
    member_var.set(False)

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("🍽️ Aplikasi Kasir Restoran - Final Version")
root.geometry("650x750")
root.config(bg="#f9fafb")

title = tk.Label(
    root,
    text="Aplikasi Kasir Restoran",
    bg="#34495e",
    fg="white",
    font=("Segoe UI", 18, "bold"),
    pady=10,
)
title.pack(fill="x")

# ---------- MENU ----------
frame_menu = tk.LabelFrame(
    root,
    text="Pilih Menu dan Jumlah",
    font=("Segoe UI", 12, "bold"),
    bg="#f9fafb",
    padx=10,
    pady=10,
)
frame_menu.pack(fill="x", padx=15, pady=10)

qty_vars = {}
row = 0
for item, harga in menu_items.items():
    tk.Label(
        frame_menu, text=f"{item} (Rp {harga:,})", bg="#f9fafb", font=("Segoe UI", 10)
    ).grid(row=row, column=0, sticky="w", pady=5)
    qty_var = tk.IntVar()
    qty_vars[item] = qty_var
    spin = tk.Spinbox(
        frame_menu, from_=0, to=10, width=5, textvariable=qty_var, font=("Segoe UI", 10)
    )
    spin.grid(row=row, column=1, padx=10)
    row += 1

# ---------- OPSI TAMBAHAN ----------
member_var = tk.BooleanVar()
tk.Checkbutton(
    root,
    text="Member (Diskon 5%)",
    variable=member_var,
    bg="#f9fafb",
    font=("Segoe UI", 10, "italic"),
).pack(anchor="w", padx=30)

# ---------- HASIL PERHITUNGAN ----------
frame_total = tk.LabelFrame(
    root,
    text="Rincian Total",
    font=("Segoe UI", 12, "bold"),
    bg="#f9fafb",
    padx=10,
    pady=10,
)
frame_total.pack(fill="x", padx=15, pady=10)

labels = [
    ("Subtotal", "lbl_subtotal_val"),
    ("Pajak (10%)", "lbl_pajak_val"),
    ("Diskon", "lbl_diskon_val"),
    ("Total", "lbl_total_val"),
    ("Kembalian", "lbl_kembalian_val"),
]

for i, (text, varname) in enumerate(labels):
    tk.Label(
        frame_total, text=f"{text}:", bg="#f9fafb", font=("Segoe UI", 10, "bold")
    ).grid(row=i, column=0, sticky="w")
    lbl = tk.Label(frame_total, text="-", bg="#f9fafb", font=("Segoe UI", 10))
    lbl.grid(row=i, column=1, sticky="w")
    globals()[varname] = lbl





# ---------- PEMBAYARAN ----------
frame_bayar = tk.LabelFrame(
    root,
    text="Pembayaran",
    font=("Segoe UI", 12, "bold"),
    bg="#f9fafb",
    padx=10,
    pady=10,
)
frame_bayar.pack(fill="x", padx=15, pady=10)

tk.Label(
    frame_bayar, text="Uang Bayar (Rp):", bg="#f9fafb", font=("Segoe UI", 10)
).grid(row=0, column=0, sticky="w")
entry_bayar = tk.Entry(frame_bayar, font=("Segoe UI", 10))
entry_bayar.grid(row=0, column=1, padx=10)




# ---------- BUTTON ----------
frame_btn = tk.Frame(root, bg="#f9fafb", pady=10)
frame_btn.pack()
tk.Button(
    frame_btn,
    text="Hitung Total",
    command=hitung_total,
    bg="#27ae60",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    relief="groove",
).grid(row=0, column=0, padx=10)
tk.Button(
    frame_btn,
    text="Proses Transaksi",
    command=proses_transaksi,
    bg="#2980b9",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    relief="groove",
).grid(row=0, column=1, padx=10)
tk.Button(
    frame_btn,
    text="Reset",
    command=reset,
    bg="#c0392b",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    relief="groove",
).grid(row=0, column=2, padx=10)




# ---------- STRUK ----------
frame_struk = tk.LabelFrame(
    root,
    text="Struk Pembayaran",
    font=("Segoe UI", 12, "bold"),
    bg="#f9fafb",
    padx=10,
    pady=10,
)
frame_struk.pack(fill="both", expand=True, padx=15, pady=10)

struk_text = scrolledtext.ScrolledText(frame_struk, height=15, font=("Consolas", 10))
struk_text.pack(fill="both", expand=True)






# ---------- FOOTER ----------
tk.Label(
    root,
    text="© 2025 - Aplikasi Kasir Restoran | by Zhaenx",
    bg="#ecf0f1",
    font=("Segoe UI", 9, "italic"),
).pack(fill="x", pady=5)

root.mainloop()
