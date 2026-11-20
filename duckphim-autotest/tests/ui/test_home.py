import pytest

from pages.home_page import HomePage

pytestmark = pytest.mark.ui


# Smoke test: trang chủ mở được và đúng tiêu đề
@pytest.mark.smoke
def test_home_page_title(driver):
    home = HomePage(driver)
    home.load()

    assert "DUCKPHIM" in home.title