import time


def step(message):
    """In 1 bước thao tác. pytest chỉ hiện các dòng này KHI TEST FAIL
    (hoặc khi chạy kèm cờ -s), nên lúc pass terminal vẫn gọn."""
    print(f"   [{time.strftime('%H:%M:%S')}] {message}")