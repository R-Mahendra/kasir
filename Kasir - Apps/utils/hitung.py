def hitung_total(makanan, minuman, is_member=False):
    subtotal = 0

    # Loop makanan
    for item, sb in makanan:
        qty = int(sb.get())
        subtotal += item["price"] * qty

    # Loop minuman
    for item, sb in minuman:
        qty = int(sb.get())
        subtotal += item["price"] * qty

    pajak = int(subtotal * 0.10)
    diskon = int(subtotal * 0.05) if is_member else 0
    total = subtotal + pajak - diskon

    return {
        "subtotal": subtotal,
        "pajak": pajak,
        "diskon": diskon,
        "total": total,
    }
