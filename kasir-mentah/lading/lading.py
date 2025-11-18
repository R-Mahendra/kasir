import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def start_loading():
    root = tk.Tk()
    root.overrideredirect(True)

    # === SETTING WINDOW ===
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    w, h = min(500, int(sw * 0.35)), min(300, int(sh * 0.35))
    x, y = (sw - w) // 2, (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    # === BACKGROUND GAMBAR ===
    try:
        img = Image.open("bg.png").resize((w, h))
        bg_img = ImageTk.PhotoImage(img)
        bg_label = tk.Label(root, image=bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # layer paling bawah
    except Exception as e:
        print(f"[!] Gagal load background: {e}")
        root.configure()

    # === PROGRESS BAR ===
    progress = ttk.Progressbar(
        root,
        orient="horizontal",
        length=int(w * 0.75),
        mode="determinate",
    )
    progress.pack(side="bottom", pady=0, fill="x")

    # === STATUS LABEL (tanpa background) ===
    label_status = tk.Label(
        root,
        text="Initializing...",
        font=("Consolas", 14, "bold"),
        foreground="#00b62d",
        bg="#e2e8f0",
        pady=3,
        padx=3,
    )
    label_status.pack(side="bottom", pady=5)

    # === FADE-IN ===
    alpha = 0.0

    def fade_in():
        nonlocal alpha
        alpha += 0.05
        if alpha >= 1.0:
            alpha = 1.0
            try:
                root.attributes("-alpha", 1.0)
            except Exception:
                pass
            root.after(60, step)
            return
        try:
            root.attributes("-alpha", alpha)
        except Exception:
            pass
        root.after(30, fade_in)

    # === FADE-OUT ===
    def fade_out(callback=None):
        nonlocal alpha
        alpha -= 0.05
        if alpha <= 0.0:
            alpha = 0.0
            try:
                root.attributes("-alpha", 0.0)
            except Exception:
                pass
            if callable(callback):
                callback()
            return
        try:
            root.attributes("-alpha", alpha)
        except Exception:
            pass
        root.after(30, lambda: fade_out(callback))

    # === PROGRESS BAR ANIMATION ===
    i = 0

    def step():
        nonlocal i
        if i <= 100:
            progress["value"] = i
            label_status.config(text=f"Loading... {i}%")
            i += 1
            root.after(40, step)
        else:
            fade_out(lambda: root.destroy())

    fade_in()
    root.mainloop()


if __name__ == "__main__":
    start_loading()
