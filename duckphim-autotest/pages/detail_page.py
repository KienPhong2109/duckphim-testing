from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class DetailPage(BasePage):
    """Trang chi tiết phim (/Movies/Details/{id}). Kế thừa BasePage."""

    MOVIE_TITLE = (By.CSS_SELECTOR, "h1.movie-title-huge")
    GENRE_LINKS = (By.CSS_SELECTOR, "main a[href*='/Movies/Category/']")
    DESCRIPTION = (By.ID, "movieDescContent")
    TOGGLE_DESC_BUTTON = (By.ID, "btnToggleDesc")

    def load(self, movie_id):
        self.open(f"Movies/Details/{movie_id}")
        self.wait_loaded()

    def wait_loaded(self):
        self.wait.until(EC.url_contains("/Movies/Details/"))
        self.find(self.MOVIE_TITLE)

    def movie_title(self):
        return self.find(self.MOVIE_TITLE).text

    def genres(self):
        return [link.get_attribute("textContent").strip() for link in self.find_all(self.GENRE_LINKS)]

    def is_description_collapsed(self):
        return "desc-collapsed" in self.find(self.DESCRIPTION).get_attribute("class")

    def toggle_description(self):
        self.click(self.TOGGLE_DESC_BUTTON)

    def toggle_button_text(self):
        return self.find(self.TOGGLE_DESC_BUTTON).text.strip()