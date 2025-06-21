def check_callback_data_length(data: str):
    byte_length = len(data.encode("utf-8"))
    print(f"String: {data} | Bytes: {byte_length}")

    if byte_length > 64:
        raise ValueError("callback_data exceeds 64 bytes!")
    return data


# Example test cases
check_callback_data_length("buy_123")  # ✅ 8 bytes (safe)
check_callback_data_length("Привет")  # ✅ 12 bytes (safe)
check_callback_data_length("Hello 😊")  # ❌ 10 characters but 11 bytes (safe)
check_callback_data_length("🚀🔥💥💯")  # ❌ 4 emojis but 16 bytes each (too long!)

rana = "THISISNOTEID"

check_callback_data_length(rana)
