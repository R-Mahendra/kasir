def clear_total(
    lbl_subtotal,
    lbl_pajak,
    lbl_diskon,
    lbl_total,
    lbl_kembalian,
    spinbox_makanan,
    spinbox_minuman,
    frameInput_uang,
    frameInput_nama,
    member_diskon,
    struk_text,
):
    """Reset total pembayaran + form + spinbox"""

    # Reset label total
    lbl_subtotal.config(text="-")
    lbl_pajak.config(text="-")
    lbl_diskon.config(text="-")
    lbl_total.config(text="-")
    lbl_kembalian.config(text="-")

    # Reset semua spinbox makanan & minuman
    for _, spin in spinbox_makanan + spinbox_minuman:
        spin.delete(0, "end")
        spin.insert(0, 0)

    # Reset input uang & nama
    frameInput_uang.delete(0, "end")
    frameInput_nama.delete(0, "end")

    # Reset checkbox member
    member_diskon.set(False)

    # Reset struk
    struk_text.delete("1.0", "end")

    return True
