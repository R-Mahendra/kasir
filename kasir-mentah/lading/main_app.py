from lading import start_loading   # pastikan file bernama lading.py
import tkinter as tk

def main():
    start_loading()   # blok sampai splash selesai
    # sekarang buat aplikasi utama
    root = tk.Tk()
    root.title("Hexsploit POS")
    root.geometry("1024x720")
    root.configure(bg="#0c4a6e")
    tk.Label(root, text="App utama", bg="#0c4a6e", fg="white").pack()
    root.mainloop()

if __name__ == "__main__":
    main()
