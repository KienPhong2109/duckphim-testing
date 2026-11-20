import time

from pages.home_page import HomePage
from utils.logger import step


class Evidence:
    """Ghi lại kịch bản thao tác tay tương ứng với một test API.
    Khi test fail, replay() làm lại kịch bản đó trên trình duyệt
    để chụp được màn hình thật đưa vào Jira."""

    def __init__(self):
        self.keyword = None
        self.path = None

    # Kịch bản 1: gõ từ khóa vào ô tìm kiếm trên trang chủ
    def search(self, keyword):
        self.keyword = keyword

    # Kịch bản 2: mở thẳng một đường dẫn (dùng cho test trang lỗi 404)
    def open_page(self, path):
        self.path = path

    def is_empty(self):
        return self.keyword is None and self.path is None

    def replay(self, driver):
        if self.path is not None:
            step(f"Tái hiện: mở trang {self.path}")
            HomePage(driver).open(self.path)
            time.sleep(2)
            return

        step(f"Tái hiện: gõ '{self.keyword}' vào ô tìm kiếm")
        home = HomePage(driver)
        home.load()
        home.open_search()
        home.type(HomePage.SEARCH_INPUT, self.keyword)
        # Chờ web gọi API và vẽ xong kết quả rồi mới chụp.
        # Ở đây dùng sleep được vì chỉ đang chụp ảnh, không phải kiểm tra điều kiện gì
        time.sleep(3)