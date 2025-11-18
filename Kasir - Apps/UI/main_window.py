import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from utils.dataload import loadMenu
from utils.hitung import hitung_total
from utils.clear import clear_total


def zhaenxUI(root):
    spinbox_makanan = []
    spinbox_minuman = []

    # =========================== FUNGSI HANDLE HITUNG
    def handle_hitung():
        hasil = hitung_total(spinbox_makanan, spinbox_minuman, member_diskon.get())

        lbl_subtotal_val.config(text=f"Rp {hasil['subtotal']:,}")  # type: ignore
        lbl_pajak_val.config(text=f"Rp {hasil['pajak']:,}")  # type: ignore
        lbl_diskon_val.config(text=f"Rp {hasil['diskon']:,}")  # type: ignore
        lbl_total_val.config(text=f"Rp {hasil['total']:,}")  # type: ignore

    # =========================== FUNGSI HANDLE HITUNG
    def handle_clear():
        clear_total(
            lbl_subtotal_val,  # type: ignore
            lbl_pajak_val,  # type: ignore
            lbl_diskon_val,  # type: ignore
            lbl_total_val,  # type: ignore
            lbl_kembalian_val,  # type: ignore
            spinbox_makanan,
            spinbox_minuman,
            frameInput_uang,
            frameInput_nama,
            member_diskon,
            struk_text,
        )

    # =========================== GUI SETUP
    root.title("🍽️ Aplikasi Kasir Restoran - zhaenx Apps")
    root.config(bg="#0c4a6e")

    # SESUAIKAN UKURAN WINDOW UNTUK RATA-RATA LAPTOP
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    w, h = int(sw * 0.52), int(sh * 0.70)
    x, y = (sw - w) // 2, (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    # BATASI AGAR NGGAK BISA DI-RESIZE
    root.resizable(True, True)

    # ANIMASI TEXT RUNNING
    marquee_text = "🔥 Selamat Datang di Restoran Zhaenx — Promo Spesial Hari Ini: Diskon 10% untuk Semua Menu! 🔥"
    marquee_label = tk.Label(
        root,
        text=marquee_text,
        bg="#34495e",
        fg="yellow",
        font=("Consolas", 12, "bold"),
        pady=4,
    )
    marquee_label.pack(fill="x")

    def run_marquee():
        nonlocal marquee_text  # biar bisa ubah variabel luar
        marquee_text = marquee_text[1:] + marquee_text[0]
        marquee_label.config(text=marquee_text)
        marquee_label.after(200, run_marquee)

    run_marquee()
    # ===========================================================================================================

    # =========================== LOAD Menu.json
    menu_items = loadMenu()
    makanan = menu_items["Makanan"]
    minuman = menu_items["Minum"]

    # =========================== FRAME LAYOUT MENU
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

    # =========================== FRAME LAYOUT MENU MAKANAN
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

    for i, item in enumerate(makanan):
        nama = item["nama"]
        harga = item["price"]

        tk.Label(
            frame_makan,
            text=f"{nama} (Rp {harga:,})",
            bg="#0c4a6e",
            fg="#e2e8f0",
            font=("Poppins", 12, "bold"),
            justify="center",
        ).grid(row=i, column=0, sticky="w", pady=5)

        spinBox = tk.Spinbox(
            frame_makan,
            from_=0,
            to=100,
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
        )
        spinBox.grid(row=i, column=1, padx=15)
        spinbox_makanan.append((item, spinBox))

    # =========================== FRAME LAYOUT MENU MINUMAN
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

    for i, item in enumerate(minuman):
        nama = item["nama"]
        harga = item["price"]

        tk.Label(
            frame_minum,
            text=f"{nama} (Rp {harga:,})",
            bg="#0c4a6e",
            fg="#e2e8f0",
            font=("Poppins", 12, "bold"),
            justify="center",
        ).grid(row=i, column=0, sticky="w", pady=5)

        spinBox = tk.Spinbox(
            frame_minum,
            from_=0,
            to=100,
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
        )
        spinBox.grid(row=i, column=1, padx=5)
        spinbox_minuman.append((item, spinBox))

    # =========================== FRAME DISKON
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

    # =========================== FRAME RINCIAN TOTAL HARGA
    frame_total = tk.LabelFrame(
        root,
        text="💰 Rincian Total",
        font=("Poppins", 14, "bold"),
        bg="#0c4a6e",
        fg="#ff00ff",
        bd=5,
    )
    frame_total.pack(fill="x", padx=20, pady=0)

    # BIAR ADA 2 KOLOM - JARAK SAMA RATA
    frame_total.columnconfigure(0, weight=1, minsize=150)
    frame_total.columnconfigure(1, weight=1, minsize=200)

    labels_data = [
        ("Subtotal         :", "lbl_subtotal_val"),
        ("PPN (10%)     :", "lbl_pajak_val"),
        ("Diskon            :", "lbl_diskon_val"),
        ("Total               :", "lbl_total_val"),
        ("Kembalian      :", "lbl_kembalian_val"),
    ]

    for i, (text, varname) in enumerate(labels_data):

        # Layout Kiri
        tk.Label(
            frame_total,
            text=text,
            bg="#0c4a6e",
            fg="#e2e8f0",
            font=("Poppins", 11, "bold"),
            anchor="w",
            width=15,
        ).grid(row=i, column=0, sticky="w", pady=4, padx=10)

        # Layout Kanan untuk hasil hitung
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

    # =========================== FRAME INPUT NAMA DAN UANG
    frame_input = tk.LabelFrame(
        root,
        text="Pembayaran",
        font=("Poppins", 14, "bold"),
        bg="#0c4a6e",
        fg="#c800de",
        bd=5,
    )
    frame_input.pack(fill="x", padx=55, pady=10)

    # FRAME INPUT UANG
    tk.Label(
        frame_input,
        text="Uang Bayar (Rp):",
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 12, "bold"),
    ).grid(row=0, column=0, sticky="w", pady=5)
    frameInput_uang = tk.Entry(
        frame_input,
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 14, "bold"),
        justify="center",  # teks di tengah
        highlightcolor="#00ffff",
        insertbackground="#c800de",
    )
    frameInput_uang.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # FRAME INPUT NAMA
    tk.Label(
        frame_input,
        text="Nama:",
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 12, "bold"),
    ).grid(row=0, column=2, sticky="w", pady=5)
    frameInput_nama = tk.Entry(
        frame_input,
        bg="#0c4a6e",
        fg="#e2e8f0",
        font=("Poppins", 14, "bold"),
        justify="center",  # teks di tengah
        highlightcolor="#00ffff",
        insertbackground="#c800de",
    )
    frameInput_nama.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

    # Konfigurasi kolom agar responsif
    frame_input.grid_columnconfigure(1, weight=1)
    frame_input.grid_columnconfigure(3, weight=1)

    # =========================== FRAME TOMBOL

    frame_Button = tk.Frame(root, bg="#0c4a6e", pady=5)
    frame_Button.pack(pady=5)
    tk.Button(
        frame_Button,
        text="Hitung Total",
        command=handle_hitung,
        bg="#00AD48",
        fg="white",
        font=("Poppins", 10, "bold"),
        padx=15,
        relief="groove",
    ).grid(row=0, column=0, padx=10)
    tk.Button(
        frame_Button,
        text="Proses Transaksi",
        # command=prosesTransaksi,
        bg="#007fd4",
        fg="white",
        font=("Poppins", 10, "bold"),
        padx=15,
        relief="groove",
    ).grid(row=0, column=1, padx=10)
    tk.Button(
        frame_Button,
        text="Clear",
        command=handle_clear,
        bg="#d41500",
        fg="white",
        font=("Poppins", 10, "bold"),
        padx=15,
        relief="groove",
    ).grid(row=0, column=2, padx=10)

    # =========================== FRAME STRUK
    frame_struk = tk.LabelFrame(
        root,
        text="🧾Struk Pembayaran",
        font=("Poppins", 14, "bold"),
        bg="#0c4a6e",
        fg="#c800de",
        labelanchor="n",
        bd=5,
    )
    frame_struk.pack(fill="x", expand=True, padx=5, pady=0)
    struk_text = scrolledtext.ScrolledText(
        frame_struk, bg="#0c4a6e", font=("Consolas"), height=7, bd=0, fg="#e2e8f0"
    )
    struk_text.pack(fill="both", expand=False)

    # =========================== FOOTER
    tk.Label(
        root,
        text="© 2025 - Aplikasi Kasir Restoran | by Zhaenx Develop",
        bg="#34495e",
        fg="#e2e8f0",
        font=("Poppins", 10, "italic", "bold"),
    ).pack(side="bottom", fill="x", pady=0)
