import tkinter as tk
from tkinter import messagebox, scrolledtext


def zhaenxUI():
    # === GUI SETUP ===
    root = tk.Tk()
    root.title("🍽️ Aplikasi Kasir Restoran - zhaenx Apps")
    root.config(bg="#0c4a6e")

    # === SESUAIKAN UKURAN WINDOW UNTUK RATA-RATA LAPTOP ===
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    w, h = int(sw * 0.52), int(sh * 0.70)
    x, y = (sw - w) // 2, (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    # === BATASI AGAR NGGAK BISA DI-RESIZE ===
    root.resizable(True, True)

    # === ANIMASI TEXT RUNNING ===
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
        nonlocal marquee_text  # biar bisa ubah variabel luar
        marquee_text = marquee_text[1:] + marquee_text[0]
        marquee_label.config(text=marquee_text)
        marquee_label.after(200, run_marquee)

    run_marquee()

    # === DATA MENU ===
    menuMakan = {
        "Nasi Goreng": 15000,
        "Mie Ayam": 12000,
        "Ayam Geprek": 18000,
        "Sate Ayam": 18000,
        "Daging Babi": 40000,
        "Sop Tunggir": 20000,
    }
    menuMinum = {
        "Es Teh Manis": 8000,
        "Kopi Hitam": 8000,
        "Jus Alpukat": 10000,
        "Jus Pare": 7000,
        "Es Kelapa Sawit": 5000,
        "Jus Rumput": 10000,
    }
    qty_vars_makan, qty_vars_minum = {}, {}

    # === FRAME MENU ===
    frame_menu = tk.LabelFrame(
        bg="#0c4a6e",
        padx=0,
        pady=0,
        highlightthickness=0,
        bd=0,
    )
    frame_menu.pack(pady=5)
    frame_menu.grid_columnconfigure(0, weight=1, uniform="equal")
    frame_menu.grid_columnconfigure(1, weight=1, uniform="equal")

    # === FRAME MENU MAKANAN===
    frame_makan = tk.LabelFrame(
        frame_menu,
        text="🍛 Makanan",
        font=("Poppins", 14, "bold"),
        bg="#0c4a6e",
        padx=5,
        pady=5,
        labelanchor="n",
        fg="#c800de",
        bd=5,
    )
    frame_makan.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    for i, (item, harga) in enumerate(menuMakan.items()):
        tk.Label(
            frame_makan,
            text=f"{item} (Rp {harga:,})",
            bg="#0c4a6e",
            fg="#e2e8f0",
            font=("Poppins", 12, "bold"),
            justify="center",
        ).grid(row=i, column=0, sticky="w", pady=5)
        qty_var = tk.IntVar()
        qty_vars_makan[item] = qty_var
        tk.Spinbox(
            frame_makan,
            from_=0,
            to=100,
            textvariable=qty_var,
            font=("Poppins", 14, "bold"),
            bg="#0c4a6e",  # dark navy
            fg="#ffffff",  # white text
            insertbackground="#00ffff",  # warna kursor input (neon cyan)
            relief="flat",  # hilangin garis kotak default
            justify="center",  # teks di tengah
            highlightthickness=2,  # kasih garis luar glowing
            highlightbackground="#1e293b",  # warna normal
            highlightcolor="#00ffff",  # warna saat aktif
            borderwidth=0,  # tipis banget, biar modern
        ).grid(row=i, column=1, padx=15)

    # === FRAME MENU MINUMAN===
    frame_minum = tk.LabelFrame(
        frame_menu,
        text="🥤 Minuman",
        font=("Poppins", 14, "bold"),
        bg="#0c4a6e",
        padx=5,
        pady=5,
        labelanchor="n",
        fg="#c800de",
        bd=5,
    )
    frame_minum.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    for i, (item, harga) in enumerate(menuMinum.items()):
        tk.Label(
            frame_minum,
            text=f"{item} (Rp {harga:,})",
            bg="#0c4a6e",
            fg="#e2e8f0",
            font=("Poppins", 12, "bold"),
            justify="center",
        ).grid(row=i, column=0, sticky="w", pady=5)
        qty_var = tk.IntVar()
        qty_vars_minum[item] = qty_var
        tk.Spinbox(
            frame_minum,
            from_=0,
            to=100,
            textvariable=qty_var,
            font=("Poppins", 14, "bold"),
            bg="#0c4a6e",
            fg="#ffffff",
            insertbackground="#00ffff",
            relief="flat",
            justify="center",
            highlightthickness=2,
            highlightbackground="#1e293b",
            highlightcolor="#00ffff",
            borderwidth=0,
        ).grid(row=i, column=1, padx=5)

    # === MEMBER CHECKBOX DISKON===
    member_diskon = tk.BooleanVar()
    frame_diskon = tk.Frame(root, bg="#0c4a6e")
    frame_diskon.pack(fill="x")
    chk_member = tk.Checkbutton(
        frame_diskon,
        text="✨ Member (Diskon 5%)",
        variable=member_diskon,
        bg="#0c4a6e",  # background gelap biar nyatu sama tema
        fg="#ff00ff",  # teks neon cyan
        activebackground="#0c4a6e",
        activeforeground="#00ffff",  # warna teks saat hover
        selectcolor="#e2e8f0",  # warna belakang kotak checkbox (gelap lembut)
        font=("Poppins", 12, "bold", "italic"),
        cursor="hand2",  # ubah cursor jadi tangan biar interaktif
        relief="flat",
    )
    chk_member.pack(fill="x")

    # === HASIL PERHITUNGAN ===
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

    # === FRAME NAMA & PEMBAYARAN # ===
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
        frame_bayar,
        text="Nama:",
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 12, "bold"),
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

    # === BUTTON ===
    frame_btn = tk.Frame(root, bg="#0c4a6e", pady=5)
    frame_btn.pack(pady=5)
    tk.Button(
        frame_btn,
        text="Hitung Total",
        # command=hitungTotal,
        bg="#00AD48",
        fg="white",
        font=("Poppins", 12, "bold"),
        padx=15,
        relief="groove",
    ).grid(row=0, column=0, padx=10)
    tk.Button(
        frame_btn,
        text="Proses Transaksi",
        # command=prosesTransaksi,
        bg="#007fd4",
        fg="white",
        font=("Poppins", 12, "bold"),
        padx=15,
        relief="groove",
    ).grid(row=0, column=1, padx=10)
    tk.Button(
        frame_btn,
        text="Clear Output",
        # command=clear,
        bg="#d41500",
        fg="white",
        font=("Poppins", 12, "bold"),
        padx=15,
        relief="groove",
    ).grid(row=0, column=2, padx=10)

    # === FOOTER ===
    tk.Label(
        root,
        text="© 2025 - Aplikasi Kasir Restoran | by Zhaenx Develop",
        bg="#34495e",
        fg="#e2e8f0",
        font=("Poppins", 10, "italic", "bold"),
    ).pack(side="bottom", fill="x", pady=0)

    root.mainloop()


zhaenxUI()
