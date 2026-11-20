import pytest

from config import settings
from pages.ecosystem_page import EcosystemPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui

# skipif: chưa khai báo tài khoản trong .env thì BỎ QUA test (kèm lời nhắc) thay vì báo lỗi khó hiểu
needs_account = pytest.mark.skipif(
    not settings.TEST_USERNAME or not settings.TEST_PASSWORD,
    reason="Chưa khai báo TEST_USERNAME / TEST_PASSWORD trong file .env",
)


# TC-24: nhập đúng tài khoản và mật khẩu, bấm Đăng nhập -> đăng nhập thành công
@needs_account
@pytest.mark.smoke
def test_tc24_login_with_valid_account(driver):
    login = LoginPage(driver)
    login.load()

    login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)

    assert not login.is_on_login_page(), (
        f"Vẫn ở trang đăng nhập. Thông báo trên trang: {login.new_messages()}"
    )

    # Đăng nhập xong web đưa về trang chọn hệ sinh thái -> bấm thẻ DuckPhim như người dùng thật.
    # Nếu sau này web đưa thẳng về chỗ khác thì mở trang phim trực tiếp
    ecosystem = EcosystemPage(driver)
    home = HomePage(driver)
    if ecosystem.is_open():
        ecosystem.enter_duckphim()
    else:
        home.load()

    # Ở web phim, thanh menu phải hiện tên tài khoản thay cho nút "Đăng nhập"
    assert home.is_logged_in_as(settings.TEST_USERNAME)


# TC-25: đúng tài khoản, sai mật khẩu -> hiện thông báo lỗi, vẫn ở trang đăng nhập
@needs_account
def test_tc25_login_with_wrong_password(driver):
    login = LoginPage(driver)
    login.load()

    login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD + "_sai")

    assert login.is_on_login_page()
    assert len(login.new_messages()) > 0, "Sai mật khẩu nhưng không thấy thông báo lỗi nào"


# TC-26: bỏ trống tài khoản và mật khẩu, bấm Đăng nhập -> không đăng nhập được, yêu cầu nhập
def test_tc26_login_with_empty_fields(driver):
    login = LoginPage(driver)
    login.load()

    login.submit()

    assert login.is_on_login_page()
    # Ô tài khoản có thuộc tính required: trình duyệt chặn không cho gửi form
    # và đưa ra lời nhắc ở ô còn trống
    assert login.username_validation_message() != ""


# TC-27: nhập mật khẩu, bấm nút con mắt -> hiện dạng văn bản; bấm lại thì ẩn
def test_tc27_show_and_hide_password(driver):
    login = LoginPage(driver)
    login.load()
    login.type_password("chuoi-bat-ky")       # không cần là mật khẩu thật

    assert login.password_field_type() == "password"     # mặc định đang ẩn

    login.toggle_password()
    assert login.password_field_type() == "text"         # bấm lần 1 -> hiện chữ

    login.toggle_password()
    assert login.password_field_type() == "password"     # bấm lần 2 -> ẩn lại