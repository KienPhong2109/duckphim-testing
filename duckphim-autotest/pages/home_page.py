from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.logger import step


class HomePage(BasePage):
    """Trang chủ DuckPhim (/Movies) và hộp tìm kiếm. Kế thừa BasePage."""

    PATH = "Movies"

    # --- Locator hộp tìm kiếm ---
    SEARCH_OPEN_BUTTON = (By.ID, "btnOpenSearchModal")   # nút "Tìm phim..." trên thanh menu
    SEARCH_INPUT = (By.ID, "aurumSearchInput")           # ô nhập trong hộp tìm kiếm
    LIVE_BOX = (By.ID, "searchResultsLive")              # khung hiện gợi ý khi đang gõ
    # Tên từng phim trong khung gợi ý (CSS selector: đi từ khung -> dòng phim -> tên)
    LIVE_RESULT_TITLES = (By.CSS_SELECTOR, "#searchResultsLive a.result-row .result-title")
    # Thẻ <b> (chữ in đậm) nằm trong khung gợi ý. Bình thường KHÔNG được có cái nào
    LIVE_BOLD_TAGS = (By.CSS_SELECTOR, "#searchResultsLive b")

    # --- Locator trang kết quả (sau khi nhấn Enter) ---
    RESULT_CARD_TITLES = (By.CSS_SELECTOR, "a.movie-card .poster-title")

    # --- Locator thẻ phim và nút yêu thích trên trang chủ ---
    MOVIE_CARDS = (By.CSS_SELECTOR, "a.movie-card")
    # Nút trái tim của phim ĐANG HIỆN trên băng chuyền lớn đầu trang.
    # Băng chuyền có nhiều phim xếp chồng, chỉ phim có class swiper-slide-active là bấm được
    HERO_FAVORITE_BUTTON = (By.CSS_SELECTOR, ".myHeroSwiper .swiper-slide-active .btn-favorite")

    # --- Locator thanh menu trên cùng ---
    NAVBAR = (By.CSS_SELECTOR, "nav.custom-navbar")
    LOGIN_LINKS = (By.CSS_SELECTOR, "a[href*='/Account/Login']")

    def load(self):
        self.open(self.PATH)
        # Chờ tiêu đề có chữ DUCKPHIM = trang đã tải xong
        self.wait.until(lambda d: "DUCKPHIM" in d.title)

    # ---------- Tìm kiếm ----------

    # Bấm nút "Tìm phim..." để bật hộp tìm kiếm, chờ ô nhập hiện ra
    def open_search(self):
        self.click(self.SEARCH_OPEN_BUTTON)
        self.find(self.SEARCH_INPUT)

    # Mở hộp tìm kiếm rồi gõ từ khóa, KHÔNG nhấn Enter -> web tự hiện gợi ý
    def type_keyword(self, keyword):
        self.open_search()
        self.type(self.SEARCH_INPUT, keyword)

    # Gõ từ khóa rồi nhấn Enter -> web chuyển sang trang kết quả
    def search(self, keyword):
        self.type_keyword(keyword)
        self.find(self.SEARCH_INPUT).send_keys(Keys.ENTER)

    # Danh sách tên phim đang hiện trong khung gợi ý
    def live_result_titles(self):
        return [element.text for element in self.find_all(self.LIVE_RESULT_TITLES)]

    # Dòng chữ trong khung gợi ý (dùng khi không có phim, ví dụ thông báo "không tìm thấy")
    def live_message(self):
        step("Chờ khung gợi ý hiện nội dung")
        # Lúc đang tải, khung chỉ có các ô xám không có chữ -> chờ tới khi có chữ
        self.wait.until(lambda d: d.find_element(*self.LIVE_BOX).text.strip() != "")
        return self.driver.find_element(*self.LIVE_BOX).text

    # Đếm số thẻ <b> trong khung gợi ý. find_elements (có s) không chờ,
    # không thấy thì trả về danh sách rỗng chứ không báo lỗi
    def live_bold_tag_count(self):
        return len(self.driver.find_elements(*self.LIVE_BOLD_TAGS))

    # Danh sách tên phim ở trang kết quả. Tên trên thẻ phim chỉ hiện khi rê chuột,
    # nên đọc từ thuộc tính title của thẻ thay vì đọc chữ hiển thị
    def result_titles(self):
        return [element.get_attribute("title") for element in self.find_all(self.RESULT_CARD_TITLES)]

    # ---------- Thẻ phim ----------

    # Tên của phim đầu tiên trên trang chủ (đọc từ thuộc tính title của thẻ)
    def first_movie_title(self):
        first_card = self.find_all(self.MOVIE_CARDS)[0]
        return first_card.find_element(By.CSS_SELECTOR, ".poster-title").get_attribute("title")

    # Bấm vào phim đầu tiên để mở trang chi tiết.
    # Hàng phim là băng chuyền: đôi khi cú bấm bị băng chuyền "nuốt" (nó tưởng đang kéo
    # hoặc đang trượt) -> chờ 5 giây, URL chưa đổi thì bấm lại, tối đa 3 lần
    def open_first_movie(self, attempts=3):
        for attempt in range(1, attempts + 1):
            self.click(self.MOVIE_CARDS)
            try:
                WebDriverWait(self.driver, 5).until(EC.url_contains("/Movies/Details/"))
                return
            except TimeoutException:
                step(f"Lần bấm thứ {attempt} chưa mở được trang chi tiết, bấm lại")
        raise AssertionError(f"Bấm {attempts} lần vào phim mà không mở được trang chi tiết")

    # ---------- Yêu thích ----------

    def click_favorite(self):
        self.click(self.HERO_FAVORITE_BUTTON)

    # Sau khi bấm yêu thích lúc CHƯA đăng nhập, web phải phản hồi bằng 1 trong 2 cách:
    # hiện hộp thông báo (alert), hoặc chuyển sang trang đăng nhập.
    # Trả về nội dung phản hồi; trả về None nếu chờ hết thời gian mà không có gì xảy ra
    def wait_login_prompt(self, seconds=5):
        step(f"Chờ tối đa {seconds} giây xem web có phản hồi không")

        # Cách 1: web hiện hộp thông báo của trình duyệt (alert)
        try:
            alert = WebDriverWait(self.driver, seconds).until(EC.alert_is_present())
            message = alert.text
            step(f"Web hiện hộp thông báo: '{message}'")
            alert.accept()          # bấm OK để đóng hộp thông báo
            return message
        except TimeoutException:
            pass                    # hết giờ mà không có alert -> xét tiếp cách 2

        # Cách 2: web chuyển thẳng sang trang đăng nhập
        if "/Account/Login" in self.driver.current_url:
            step("Web chuyển sang trang đăng nhập")
            return "Chuyển sang trang đăng nhập"

        step("Web không phản hồi gì")
        return None

    # ---------- Trạng thái đăng nhập ----------

    # Đã đăng nhập khi: thanh menu hiện tên tài khoản VÀ không còn link "Đăng nhập"
    def is_logged_in_as(self, username):
        navbar_text = self.find(self.NAVBAR).text.replace("\n", " | ")
        has_login_link = len(self.driver.find_elements(*self.LOGIN_LINKS)) > 0
        step(f"Thanh menu đang hiện: '{navbar_text}'. Còn link Đăng nhập: {has_login_link}")
        return username.lower() in navbar_text.lower() and not has_login_link
    