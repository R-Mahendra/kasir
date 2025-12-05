def greedy():
    uang = int(input("Masukkan Uang : "))
    koinSaya = [10, 25, 30, 5, 1, 8]
    hasil = []

    if uang == 0:
        print("Error!")

    for koin in sorted(koinSaya, reverse=True):
        while uang >= koin:
            uang -= koin
            hasil.append(koin)
    if uang == 0:
        print(f"Koin yang dipakai : {hasil}\nTotal : {len(hasil)} Koin")
    else:
        print("Uang tidak bisa di pecah...!")

greedy()
