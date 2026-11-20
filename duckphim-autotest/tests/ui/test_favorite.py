import pytest

from pages.home_page import HomePage

pytestmark = pytest.mark.ui


# TC-23: bấm nút yêu thích trên trang chủ khi chưa đăng nhập
# -> web phải hiện thông báo yêu cầu đăng nhập hoặc chuyển đến trang đăng nhập
def test_tc23_favorite_without_login_asks_to_login(driver):
    home = HomePage(driver)
    home.load()

    home.click_favorite()

    reaction = home.wait_login_prompt()
    assert reaction is not None, (
        "Bấm yêu thích khi chưa đăng nhập: web không hiện thông báo "
        "và cũng không chuyển sang trang đăng nhập"
    )