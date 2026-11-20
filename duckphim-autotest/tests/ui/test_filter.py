import pytest

from config import data
from pages.advanced_search_page import AdvancedSearchPage
from pages.detail_page import DetailPage

pytestmark = pytest.mark.ui


# TC-19: vào kho phim, chọn một thể loại, bấm lọc -> phim trả về thuộc thể loại đã chọn
def test_tc19_filter_by_category(driver):
    page = AdvancedSearchPage(driver)
    page.load()

    page.choose_category(data.FILTER_CATEGORY)
    page.apply_filter()

    # Ô chọn vẫn giữ thể loại vừa chọn, và có phim trả về
    assert page.selected_category() == data.FILTER_CATEGORY
    movie_ids = page.movie_ids()
    assert len(movie_ids) > 0

    # Thẻ phim chỉ hiện 2 thể loại đầu nên không đủ để kết luận.
    # Mở trang chi tiết của vài phim đầu để xem đủ danh sách thể loại
    detail = DetailPage(driver)
    for movie_id in movie_ids[:data.FILTER_SAMPLE_SIZE]:
        detail.load(movie_id)
        assert data.FILTER_CATEGORY in detail.genres(), (
            f"Phim '{detail.movie_title()}' (id={movie_id}) không thuộc thể loại {data.FILTER_CATEGORY}"
        )


# TC-20: vào kho phim, chọn loại "Phim lẻ", bấm lọc -> danh sách chỉ gồm phim lẻ
def test_tc20_filter_by_type(driver):
    page = AdvancedSearchPage(driver)
    page.load()

    page.choose_type(data.FILTER_TYPE)
    page.apply_filter()

    badges = page.type_badges()
    assert len(badges) > 0
    for badge in badges:
        # .lower() vì ô chọn ghi "Phim lẻ" còn nhãn trên thẻ ghi "Phim Lẻ"
        assert badge.lower() == data.FILTER_TYPE.lower()