import pytest

from config import data
from pages.detail_page import DetailPage
from pages.home_page import HomePage

pytestmark = pytest.mark.ui


# TC-21: bấm vào một phim trên trang chủ -> mở trang chi tiết, tiêu đề khớp với phim đã bấm
@pytest.mark.smoke
def test_tc21_open_movie_from_home(driver):
    home = HomePage(driver)
    home.load()
    # Ghi lại tên phim TRƯỚC khi bấm để lát nữa so sánh
    expected_title = home.first_movie_title()

    home.open_first_movie()

    detail = DetailPage(driver)
    detail.wait_loaded()
    assert detail.movie_title().strip().lower() == expected_title.strip().lower()


# TC-22: bấm nút "Xem thêm" ở phần mô tả -> phần mô tả được mở rộng
def test_tc22_expand_description(driver):
    detail = DetailPage(driver)
    detail.load(data.MOVIE_ID)

    # Lúc mới vào, mô tả đang thu gọn
    assert detail.is_description_collapsed()

    detail.toggle_description()

    # Sau khi bấm: hết thu gọn, và nút đổi chữ thành "Thu gọn"
    assert not detail.is_description_collapsed()
    assert "thu gọn" in detail.toggle_button_text().lower()