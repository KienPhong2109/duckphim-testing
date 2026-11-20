import pytest
from selenium.webdriver.support import expected_conditions as EC

from config import data
from pages.home_page import HomePage

pytestmark = pytest.mark.ui


# TC-14: gõ "conan" vào ô tìm kiếm -> hiện danh sách gợi ý có tiêu đề chứa "conan"
@pytest.mark.smoke
def test_tc14_live_search_shows_matching_movies(driver):
    home = HomePage(driver)
    home.load()

    home.type_keyword(data.KEYWORD_CONAN)

    titles = home.live_result_titles()
    assert len(titles) > 0
    for title in titles:
        assert data.KEYWORD_CONAN in title.lower()


# TC-15: gõ từ khóa không có phim -> hiện thông báo không tìm thấy
def test_tc15_live_search_not_found_shows_message(driver):
    home = HomePage(driver)
    home.load()

    home.type_keyword(data.KEYWORD_NOT_FOUND)

    message = home.live_message()
    assert "không tìm thấy" in message
    assert data.KEYWORD_NOT_FOUND in message


# TC-16: gõ "conan" rồi nhấn Enter -> chuyển đến trang kết quả, có phim phù hợp
def test_tc16_search_by_enter_goes_to_result_page(driver):
    home = HomePage(driver)
    home.load()

    home.search(data.KEYWORD_CONAN)

    # Nhấn Enter -> URL đổi thành /Movies?searchString=conan
    home.wait.until(EC.url_contains("searchString="))
    titles = home.result_titles()
    assert len(titles) > 0
    for title in titles:
        assert data.KEYWORD_CONAN in title.lower()

# TC-17 (đoán lỗi): từ khóa có dấu ngoặc đơn -> vẫn hiện kết quả phù hợp, không báo lỗi
def test_tc17_live_search_with_parenthesis(driver):
    home = HomePage(driver)
    home.load()

    home.type_keyword(data.KEYWORD_PARENTHESIS)

    message = home.live_message()
    assert "Lỗi mất kết nối" not in message, f"Khung gợi ý báo lỗi: '{message}'"

    titles = home.live_result_titles()
    assert len(titles) > 0
    for title in titles:
        assert data.KEYWORD_PARENTHESIS.lower() in title.lower()


# TC-18 (đoán lỗi): từ khóa là thẻ HTML -> phải hiển thị như văn bản thường, không bị in đậm
def test_tc18_live_search_html_keyword_shown_as_text(driver):
    home = HomePage(driver)
    home.load()

    home.type_keyword(data.KEYWORD_HTML)

    message = home.live_message()
    # Nếu web chèn thẳng từ khóa vào trang, trình duyệt sẽ hiểu <b> là thẻ in đậm thật
    assert home.live_bold_tag_count() == 0, "Từ khóa bị trình duyệt hiểu thành thẻ HTML (nguy cơ XSS)"
    # Hiển thị đúng thì người dùng phải nhìn thấy nguyên chuỗi mình đã gõ
    assert data.KEYWORD_HTML in message