from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import step


class EcosystemPage(BasePage):
    """Trang giới thiệu DuckEntertainment (/), có khu "Chọn Trải Nghiệm Của Bạn"
    để vào web phim hoặc web nhạc. Sau khi đăng nhập, web đưa người dùng về đây."""

    # Khu chọn trải nghiệm, và thẻ dẫn vào web phim DuckPhim
    SECTION = (By.ID, "ecosystem")
    DUCKPHIM_CARD = (By.CSS_SELECTOR, "#ecosystem a.cinema-card[href='/Movies']")

    # Trình duyệt có đang ở trang này không
    def is_open(self):
        # Chờ trang tải xong hẳn rồi mới xét đây là trang nào
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        step(f"Trang hiện tại: {self.driver.current_url}")
        return len(self.driver.find_elements(*self.SECTION)) > 0

    # Bấm thẻ "DuckPhim" để vào web phim
    def enter_duckphim(self):
        self.click(self.DUCKPHIM_CARD)
        self.wait.until(EC.url_contains("/Movies"))