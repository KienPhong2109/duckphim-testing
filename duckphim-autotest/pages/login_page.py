from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.logger import step


class LoginPage(BasePage):
    """Trang đăng nhập (/Account/Login). Kế thừa BasePage."""

    PATH = "Account/Login"

    # Ô tài khoản không có id -> định vị theo name, giới hạn trong form đăng nhập
    USERNAME_INPUT = (By.CSS_SELECTOR, "#login-form input[name='username']")
    PASSWORD_INPUT = (By.ID, "password-input")
    TOGGLE_PASSWORD_BUTTON = (By.ID, "togglePasswordBtn")      # nút con mắt ẩn/hiện mật khẩu
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#login-form button[type='submit']")
    # Link "Đăng nhập" trên thanh menu: còn link này nghĩa là CHƯA đăng nhập
    LOGIN_LINKS = (By.CSS_SELECTOR, "a[href*='/Account/Login']")
    BODY = (By.TAG_NAME, "body")

    def load(self):
        self.open(self.PATH)
        self.find(self.USERNAME_INPUT)
        # Ghi lại các dòng chữ lúc trang vừa mở, để sau đó biết dòng nào MỚI xuất hiện
        self._initial_lines = self._visible_lines()

    # ---------- Thao tác ----------

    def type_password(self, password):
        self.type(self.PASSWORD_INPUT, password, secret=True)

    def submit(self):
        self.click(self.SUBMIT_BUTTON)

    # Nhập tài khoản, mật khẩu rồi bấm Đăng nhập
    def login(self, username, password):
        old_page = self.driver.find_element(By.TAG_NAME, "html")
        self.type(self.USERNAME_INPUT, username)
        self.type_password(password)
        self.submit()
        # Form gửi đi thì trình duyệt tải trang mới (dù đăng nhập đúng hay sai)
        # -> chờ trang cũ biến mất rồi mới kiểm tra tiếp
        step("Chờ web xử lý đăng nhập và tải trang mới")
        self.wait.until(EC.staleness_of(old_page))

    def toggle_password(self):
        self.click(self.TOGGLE_PASSWORD_BUTTON)

    # ---------- Đọc trạng thái ----------

    def is_on_login_page(self):
        return "/Account/Login" in self.driver.current_url

    # Đăng nhập thành công khi: đã rời trang đăng nhập VÀ thanh menu không còn link "Đăng nhập"
    def is_logged_in(self):
        if self.is_on_login_page():
            return False
        self.find(self.BODY)
        return len(self.driver.find_elements(*self.LOGIN_LINKS)) == 0

    # Kiểu của ô mật khẩu: "password" = đang ẩn (hiện dấu chấm), "text" = đang hiện chữ
    def password_field_type(self):
        return self.find(self.PASSWORD_INPUT).get_attribute("type")

    # Lời nhắc của trình duyệt khi ô bắt buộc còn trống. Chuỗi rỗng = ô hợp lệ
    def username_validation_message(self):
        return self.find(self.USERNAME_INPUT).get_attribute("validationMessage")

    # Các dòng chữ MỚI xuất hiện so với lúc trang vừa mở (ví dụ thông báo sai mật khẩu).
    # Chờ tối đa vài giây; không có gì mới thì trả về danh sách rỗng
    def new_messages(self, seconds=5):
        try:
            WebDriverWait(self.driver, seconds).until(lambda d: len(self._new_lines()) > 0)
        except TimeoutException:
            pass
        messages = self._new_lines()
        step(f"Dòng chữ mới xuất hiện trên trang: {messages}")
        return messages

    # ---------- Hàm phụ (tên bắt đầu bằng _ = chỉ dùng bên trong lớp) ----------

    def _visible_lines(self):
        text = self.driver.find_element(*self.BODY).text
        return [line.strip() for line in text.splitlines() if line.strip()]

    def _new_lines(self):
        return [line for line in self._visible_lines() if line not in self._initial_lines]