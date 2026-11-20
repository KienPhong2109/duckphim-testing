from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api.movies_api import MoviesApi
from config.settings import BASE_URL
from utils.evidence import Evidence

SCREENSHOT_DIR = Path("reports/screenshots")


# --- Các hàm dùng chung ---

def _chrome_options():
    """Cấu hình Chrome dùng cho cả test giao diện lẫn lúc chụp ảnh tái hiện."""
    options = Options()
    # DuckPhim chỉ chạy http -> cho phép web này để Chrome không hiện cảnh báo HTTPS
    options.add_argument(f"--unsafely-treat-insecure-origin-as-secure={BASE_URL}")
    options.add_argument("--disable-features=HttpsFirstBalancedModeAutoEnable")
    options.add_experimental_option("prefs", {
        "https_only_mode_enabled": False,
        # Tắt trình quản lý mật khẩu của Chrome: không hỏi lưu mật khẩu, không hiện
        # hộp "Change your password" (mật khẩu đã bị lộ) che mất trang khi test đăng nhập
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--start-maximized")
    return options


def _save_screenshot(driver, test_name):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)     # chưa có folder thì tự tạo
    name = f"{test_name}_{datetime.now():%H%M%S}.png"
    driver.save_screenshot(str(SCREENSHOT_DIR / name))
    print(f"   Ảnh chụp lỗi: reports/screenshots/{name}")


# --- Hook của pytest ---

# Sau mỗi test, lưu kết quả vào chính test đó để các fixture biết pass hay fail
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"report_{outcome.get_result().when}", outcome.get_result())


# Chạy 1 lần trước test đầu tiên: dọn ảnh của lần chạy trước
def pytest_sessionstart(session):
    if SCREENSHOT_DIR.exists():
        for file in SCREENSHOT_DIR.glob("*.png"):
            file.unlink()


# --- Fixture ---

@pytest.fixture(scope="session")
def movies_api():
    return MoviesApi()


# Test giao diện: Chrome đang mở sẵn, fail thì chụp luôn
@pytest.fixture
def driver(request):
    driver = webdriver.Chrome(options=_chrome_options())
    yield driver

    report = getattr(request.node, "report_call", None)
    if report is not None and report.failed:
        _save_screenshot(driver, request.node.name)

    driver.quit()


# Test API: fail thì MỞ Chrome, thao tác lại kịch bản rồi mới chụp
@pytest.fixture
def evidence(request):
    ev = Evidence()
    yield ev

    report = getattr(request.node, "report_call", None)
    if report is None or not report.failed or ev.is_empty():
        return

    print("   Test fail -> mở trình duyệt tái hiện lại để chụp màn hình...")
    driver = webdriver.Chrome(options=_chrome_options())
    try:
        ev.replay(driver)
        _save_screenshot(driver, request.node.name)
    finally:
        driver.quit()      # finally: lỗi gì cũng phải đóng Chrome