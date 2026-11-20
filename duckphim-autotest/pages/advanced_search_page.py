from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from utils.logger import step


class AdvancedSearchPage(BasePage):
    """Trang Kho phim - lọc nâng cao (/Movies/AdvancedSearch). Kế thừa BasePage."""

    PATH = "Movies/AdvancedSearch"

    # Các ô trong form lọc không có id -> định vị theo thuộc tính name
    CATEGORY_SELECT = (By.CSS_SELECTOR, "select[name='categoryId']")
    TYPE_SELECT = (By.CSS_SELECTOR, "select[name='type']")
    FILTER_BUTTON = (By.CSS_SELECTOR, "button.btn-specular-filter")

    # Thẻ phim trong kết quả và nhãn loại phim ("Phim Lẻ"/"Phim Bộ") trên thẻ
    MOVIE_CARDS = (By.CSS_SELECTOR, "a.movie-card")
    TYPE_BADGES = (By.CSS_SELECTOR, "a.movie-card .badge-type")

    def load(self):
        self.open(self.PATH)
        self.find(self.FILTER_BUTTON)

    # Select là lớp của Selenium chuyên thao tác với ô chọn <select>
    def choose_category(self, name):
        step(f"Chọn thể loại '{name}'")
        Select(self.find(self.CATEGORY_SELECT)).select_by_visible_text(name)

    def choose_type(self, name):
        step(f"Chọn loại phim '{name}'")
        Select(self.find(self.TYPE_SELECT)).select_by_visible_text(name)

    # Bấm nút lọc. Form gửi bằng GET nên điều kiện lọc hiện lên URL
    # (...?keyword=&categoryId=7&country=&type=) -> chờ URL đổi là biết trang kết quả đã về
    def apply_filter(self):
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.url_contains("categoryId="))

    # Thể loại đang được chọn trong ô chọn
    def selected_category(self):
        return Select(self.find(self.CATEGORY_SELECT)).first_selected_option.text.strip()

    # Mã của các phim trong kết quả, lấy từ link /Movies/Details/{mã}
    def movie_ids(self):
        links = [card.get_attribute("href") for card in self.find_all(self.MOVIE_CARDS)]
        return [link.split("/")[-1] for link in links]

    # Nhãn loại phim trên từng thẻ phim
    def type_badges(self):
        return [badge.get_attribute("textContent").strip() for badge in self.find_all(self.TYPE_BADGES)]