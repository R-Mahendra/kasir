import tkinter as tk
import datetime, os
from tkinter import messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
from loading import start_loading

# ---------- DATA MENU MAKANAN ----------

menuMakan = {
    "Nasi Goreng": 15000,
    "Mie Ayam": 12000,
    "Ayam Geprek": 18000,
    "Sate Ayam": 18000,
    "Daging Babi": 40000,
}

# ---------- DATA MENU MINUMAN ----------
menuMinum = {
    "Es Teh Manis": 8000,
    "Kopi Hitam": 8000,
    "Jus Alpukat": 10000,
    "Jus pare": 7000,
    "Es Kelapa Sawit": 5000,
}


# ---------- FUNGSI HITUNG TOTAL ----------
def hitungTotal():
    subtotal = 0

    # HITUNG JUMLAH MAKANAN YANG DIBELI

    for item, qty_vars in qty_vars_makan.items():
        jumlah = qty_vars.get()
        if jumlah > 0:
            subtotal += menuMakan[item] * jumlah

    # HITUNG JUMLAH MINUMAN YANG DIBELI
    for item, qty_vars in qty_vars_minum.items():
        jumlah = qty_vars.get()
        if jumlah > 0:
            subtotal += menuMinum[item] * jumlah

    # HITUNG PAJAK & DISKON
    pajak = subtotal * 0.1  # 10% PPN
    diskon = subtotal * 0.05 if member_var.get() else 0
    total = subtotal + pajak - diskon

    # TAMPILKAN HASIL HITUNG DI RINCIAN
    lbl_subtotal_val.config(text=f"Rp {subtotal:,.0f}")  # type: ignore
    lbl_pajak_val.config(text=f"Rp {pajak:,.0f}")  # type: ignore
    lbl_diskon_val.config(text=f"Rp {diskon:,.0f}")  # type: ignore
    lbl_total_val.config(text=f"Rp {total:,.0f}")  # type: ignore

    return total, subtotal, pajak, diskon


# ---------- FUNGSI TRANSAKSI ----------
def prosesTransaksi():
    total, subtotal, pajak, diskon = hitungTotal()
    try:
        bayar = int(entry_bayar.get())
    except ValueError:
        messagebox.showerror("Error Bro.!", "Nominal pembayaran tidak valid!")
        return

    if bayar < total:
        messagebox.showwarning("Kurang Bro.!", "Uang Lo ngga cukup!")
        return

    kembalian = bayar - total
    lbl_kembalian_val.config(text=f"Rp {kembalian:,.0f}")  # type: ignore
    tampilanStruk(subtotal, pajak, diskon, total, bayar, kembalian)


def animate_struk_loading():
    text = "💾 Mencetak Struk"
    for i in range(len(text) + 1):
        struk_text.delete(1.0, tk.END)
        struk_text.insert(tk.END, text[:i] + "...")
        struk_text.update()
        struk_text.after(250)


# ---------- FUNGSI UI STRUK ---------
def tampilanStruk(subtotal, pajak, diskon, total, bayar, kembalian):
    # btn_proses.config(state="disabled") 
    animate_struk_loading()
    # btn_proses.config(state="normal")

    # Ambil subtotal total
    namaPembeli = entry_nama.get()

    waktu = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    struk = []

    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nama_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    folder = "struk"
    os.makedirs(folder, exist_ok=True)

    # Buat isi struk
    struk = []
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    struk.append("         STRUK PEMBAYARAN RESTORAN        ")
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    struk.append(f"Tanggal : {waktu}")
    struk.append("")
    struk.append(f"Pesanan (a/n) : {namaPembeli}")
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # --- MAKANAN ---
    for item, qty_var in qty_vars_makan.items():
        jumlah = int(qty_var.get())
        if jumlah > 0:
            total_harga = menuMakan[item] * jumlah
            struk.append(f"{item:<20} x{jumlah:<2} Rp {total_harga:>10,}")

    # --- MINUMAN ---
    for item, qty_var in qty_vars_minum.items():
        jumlah = int(qty_var.get())
        if jumlah > 0:
            total_harga = menuMinum[item] * jumlah
            struk.append(f"{item:<20} x{jumlah:<2} Rp {total_harga:>10,}")

    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    struk.append(f"Subtotal     : Rp {subtotal:,.0f}")
    struk.append(f"Bayar        : Rp {bayar:,.0f}")
    struk.append(f"PPN (10%)    : Rp {pajak:,.0f}")
    struk.append(f"Diskon       : Rp {diskon:,.0f}")
    struk.append(f"Total        : Rp {total:,.0f}")
    struk.append(f"Kembalian    : Rp {kembalian:,.0f}")
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    struk.append("   Terima kasih telah berkunjung di")
    struk.append("         Restoran Zhaenx  ")
    struk.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Gabung jadi string utuh
    hasil_struk = "\n".join(struk)

    # --- TAMPIL DI SCROLLEDTEXT ---
    struk_text.config(state="normal")  # aktifkan biar bisa diubah
    struk_text.delete(1.0, tk.END)
    struk_text.insert(tk.END, hasil_struk)
    struk_text.config(state="disabled")  # kunci lagi biar gak bisa diketik

    # --- SIMPAN KE FILE ---
    file_path = os.path.join(folder, nama_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(hasil_struk)

    # Notifikasi ke user
    messagebox.showinfo("Struk Disimpan", f"Struk berhasil disimpan ke:\n{file_path}")


# ---------- FUNGSI CLEAR ----------
def clear():
    # Reset semua Spinbox makanan
    for item in qty_vars_makan.values():
        item.set(0)

    # Reset semua Spinbox minuman
    for item in qty_vars_minum.values():
        item.set(0)

    # Reset entry pembayaran
    entry_bayar.delete(0, tk.END)
    entry_nama.delete(0, tk.END)  # reset input nama juga

    # Reset label hasil perhitungan
    lbl_subtotal_val.config(text="-")  # type: ignore
    lbl_pajak_val.config(text="-")  # type: ignore
    lbl_diskon_val.config(text="-")  # type: ignore
    lbl_total_val.config(text="-")  # type: ignore
    lbl_kembalian_val.config(text="-")  # type: ignore

    # Reset struk
    struk_text.config(state="normal")
    struk_text.delete(1.0, tk.END)
    struk_text.config(state="disabled")

    # Reset member checkbox
    member_var.set(False)

start_loading()
# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("🍽️ Aplikasi Kasir Restoran - zhaenx Apps")
# root.geometry("700x860")
root.config(bg="#0c4a6e")
#root.overrideredirect(True)  # hilangkan title bar biar clean

# ---------- TEXT BERJALAN ----------
marquee_text = "🔥 Selamat Datang di Restoran Zhaenx — Promo Spesial Hari Ini: Diskon 10% untuk Semua Menu! 🔥"
marquee_label = tk.Label(
    root,
    text=marquee_text,
    bg="#34495e",
    fg="yellow",
    font=("Consolas", 14, "bold"),
    pady=5,
)
marquee_label.pack(fill="x")


def run_marquee():
    global marquee_text
    marquee_text = marquee_text[1:] + marquee_text[0]  # geser huruf ke kiri
    marquee_label.config(text=marquee_text)
    marquee_label.after(200, run_marquee)  # kecepatan gerak (ms)


run_marquee()


# ---------- FRAME UTAMA ----------
frame_menu = tk.LabelFrame(
    bg="#0c4a6e",
    padx=0,
    pady=0,
    highlightthickness=0,  # hilangin outline biru/abu default
    bd=0,  # hilangin border frame
)
frame_menu.pack(pady=5)
frame_menu.grid_columnconfigure(0, weight=1, uniform="equal")
frame_menu.grid_columnconfigure(1, weight=1, uniform="equal")

# ---------- FRAME MAKANAN ----------
frame_makan = tk.LabelFrame(
    frame_menu,
    text="🍛 Makanan",
    font=("Poppins", 28, "bold"),
    bg="#0c4a6e",
    padx=5,
    pady=5,
    labelanchor="n",
    fg="#c800de",
    bd=5,
)
frame_makan.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

qty_vars_makan = {}
for i, (item, harga) in enumerate(menuMakan.items()):
    tk.Label(
        frame_makan,
        text=f"{item} (Rp {harga:,})",
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 14),
    ).grid(row=i, column=0, sticky="w", pady=5)
    qty_var = tk.IntVar()
    qty_vars_makan[item] = qty_var
    tk.Spinbox(
        frame_makan,
        from_=0,
        to=100,
        width=5,
        textvariable=qty_var,
        font=("Poppins", 15, "bold"),
        bg="#0c4a6e",  # dark navy
        fg="#ffffff",  # white text
        insertbackground="#00ffff",  # warna kursor input (neon cyan)
        relief="flat",  # hilangin garis kotak default
        justify="center",  # teks di tengah
        highlightthickness=2,  # kasih garis luar glowing
        highlightbackground="#1e293b",  # warna normal
        highlightcolor="#00ffff",  # warna saat aktif
        borderwidth=0,  # tipis banget, biar modern
    ).grid(row=i, column=1, padx=5)


# ---------- FRAME MINUMAN ----------
frame_minum = tk.LabelFrame(
    frame_menu,
    text="🥤 Minuman",
    font=("Poppins", 28, "bold"),
    bg="#0c4a6e",
    padx=5,
    pady=5,
    labelanchor="n",
    fg="#c800de",
    bd=5,
)
frame_minum.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

qty_vars_minum = {}
for i, (item, harga) in enumerate(menuMinum.items()):
    tk.Label(
        frame_minum,
        text=f"{item} (Rp {harga:,})",
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 14),
    ).grid(row=i, column=0, sticky="w", pady=5)
    qty_var = tk.IntVar()
    qty_vars_minum[item] = qty_var
    tk.Spinbox(
        frame_minum,
        from_=0,
        to=100,
        width=5,
        textvariable=qty_var,
        font=("Poppins", 15, "bold"),
        bg="#0c4a6e",  # dark navy
        fg="#e2e8f0",  # white text
        insertbackground="#00ffff",  # warna kursor input (neon cyan)
        relief="flat",  # hilangin garis kotak default
        justify="center",  # teks di tengah
        highlightthickness=2,  # kasih garis luar glowing
        highlightbackground="#1e293b",  # warna normal
        highlightcolor="#00ffff",  # warna saat aktif
        borderwidth=0,  # tipis banget, biar modern
    ).grid(row=i, column=1, padx=5)

# ---------- OPSI TAMBAHAN ----------
member_var = tk.BooleanVar()

frame_opsi = tk.Frame(root, bg="#0c4a6e")
frame_opsi.pack(fill="x")

chk_member = tk.Checkbutton(
    frame_opsi,
    text="✨ Member (Diskon 5%)",
    variable=member_var,
    bg="#0c4a6e",  # background gelap biar nyatu sama tema
    fg="#ff00ff",  # teks neon cyan
    activebackground="#0c4a6e",
    activeforeground="#00ffff",  # warna teks saat hover
    selectcolor="#e2e8f0",  # warna belakang kotak checkbox (gelap lembut)
    font=("Poppins", 12, "bold", "italic"),
    cursor="hand2",  # ubah cursor jadi tangan biar interaktif
    relief="flat",
)
chk_member.pack(anchor="n", padx=35, pady=0)


# ---------- HASIL PERHITUNGAN ----------
frame_total = tk.LabelFrame(
    root,
    text="💰 Rincian Total",
    font=("Poppins", 14, "bold"),
    bg="#0c4a6e",
    fg="#ff00ff",
    bd=5,
)
frame_total.pack(fill="x", padx=20, pady=0)


# Biar dua kolom punya jarak seimbang
frame_total.columnconfigure(0, weight=1, minsize=150)
frame_total.columnconfigure(1, weight=1, minsize=200)

labels = [
    ("Subtotal         :", "lbl_subtotal_val"),
    ("PPN (10%)     :", "lbl_pajak_val"),
    ("Diskon            :", "lbl_diskon_val"),
    ("Total               :", "lbl_total_val"),
    ("Kembalian      :", "lbl_kembalian_val"),
]

for i, (text, varname) in enumerate(labels):
    # Label kiri
    tk.Label(
        frame_total,
        text=text,
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 11, "bold"),
        anchor="w",
        width=15,
    ).grid(row=i, column=0, sticky="w", pady=4, padx=10)

    # Label kanan (hasil)
    lbl = tk.Label(
        frame_total,
        text="-",
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 11, "bold"),
        anchor="e",
        width=20,
        relief="solid",
        bd=0,
        padx=10,
        pady=2,
    )
    lbl.grid(row=i, column=1, sticky="e", pady=4, padx=10)
    globals()[varname] = lbl


# ---------- PEMBAYARAN ----------
frame_bayar = tk.LabelFrame(
    root,
    text="Pembayaran",
    font=("Poppins", 14, "bold"),
    bg="#0c4a6e",
    fg="#c800de",
    bd=5,
)
frame_bayar.pack(fill="x", padx=55, pady=10)

# Label dan Entry
tk.Label(
    frame_bayar,
    text="Uang Bayar (Rp):",
    bg="#0c4a6e",
    fg="#e2e8f0",
    font=("Poppins", 12, "bold"),
).grid(row=0, column=0, sticky="w", pady=5)
entry_bayar = tk.Entry(
    frame_bayar,
    bg="#0c4a6e",
    fg="#e2e8f0",
    font=("Poppins", 14, "bold"),
    justify="center",  # teks di tengah
    highlightcolor="#00ffff",
    insertbackground="#c800de",
)
entry_bayar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

tk.Label(
    frame_bayar, text="Nama:", bg="#0c4a6e", fg="#e2e8f0", font=("Poppins", 12, "bold")
).grid(row=0, column=2, sticky="w", pady=5)
entry_nama = tk.Entry(
    frame_bayar,
    bg="#0c4a6e",
    fg="#e2e8f0",
    font=("Poppins", 14, "bold"),
    justify="center",  # teks di tengah
    highlightcolor="#00ffff",
    insertbackground="#c800de",
)
entry_nama.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

# Konfigurasi kolom agar responsif
frame_bayar.grid_columnconfigure(1, weight=1)
frame_bayar.grid_columnconfigure(3, weight=1)


# ---------- BUTTON ----------
frame_btn = tk.Frame(root, bg="#0c4a6e", pady=5)
frame_btn.pack(pady=5)
tk.Button(
    frame_btn,
    text="Hitung Total",
    command=hitungTotal,
    bg="#00AD48",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=15,
    relief="groove",
).grid(row=0, column=0, padx=10)
tk.Button(
    frame_btn,
    text="Proses Transaksi",
    command=prosesTransaksi,
    bg="#007fd4",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=15,
    relief="groove",
).grid(row=0, column=1, padx=10)
tk.Button(
    frame_btn,
    text="Clear Output",
    command=clear,
    bg="#d41500",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=15,
    relief="groove",
).grid(row=0, column=2, padx=10)


# ---------- STRUK ----------
frame_struk = tk.LabelFrame(
    root,
    text="🧾Struk Pembayaran",
    font=("Poppins", 18, "bold"),
    bg="#0c4a6e",
    fg="#c800de",
    labelanchor="n",
    bd=7,
)
frame_struk.pack(fill="x", expand=True, padx=5, pady=0)
struk_text = scrolledtext.ScrolledText(
    frame_struk, bg="#0c4a6e", font=("Consolas"), height=7, bd=0, fg="#e2e8f0"
)
struk_text.pack(fill="both", expand=False)

# ---------- FOOTER ----------
tk.Label(
    root,
    text="© 2025 - Aplikasi Kasir Restoran | by Zhaenx Develop",
    bg="#34495e",
    fg="#e2e8f0",
    font=("Poppins", 10, "italic", "bold"),
).pack(side="bottom", fill="x", pady=0)


# === SESUAIKAN UKURAN WINDOW UNTUK RATA-RATA LAPTOP ===
# Auto-scale ukuran utama (75% dari resolusi layar)
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
w, h = int(sw * 0.75), int(sh * 0.75)
x, y = (sw - w) // 2, (sh - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")



# === BATASI AGAR NGGAK BISA DI-RESIZE ===
root.resizable(True, True)
root.minsize(700, 860)  # <- biar minimal gak kekecilan

root.mainloop()
