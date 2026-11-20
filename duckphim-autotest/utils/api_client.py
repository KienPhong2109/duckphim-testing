import requests

from config.settings import BASE_URL, TIMEOUT
from utils.logger import step


class ApiClient:
    """Lớp cha: gói thư viện requests lại để mọi lớp API dùng chung một cách gọi."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        # Session giữ kết nối + cookie giữa các request (sau này đăng nhập sẽ cần cookie)
        self.session = requests.Session()

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"

        # Ghi lại request sắp gửi. Các dòng này chỉ hiện khi test FAIL hoặc chạy kèm -s
        step(f"Gửi {method} {url} | tham số: {kwargs.get('params', {})}")

        response = self.session.request(method, url, timeout=TIMEOUT, **kwargs)

        # Ghi lại phản hồi: mã trạng thái, thời gian, 200 ký tự đầu của nội dung
        step(f"Nhận về mã {response.status_code} sau {response.elapsed.total_seconds():.2f} giây")
        step(f"Nội dung trả về: {response.text[:200]}")
        return response

    # **kwargs = "nhận thêm bao nhiêu tham số tùy chọn cũng được" (params, headers,
    # allow_redirects...) rồi chuyển nguyên xuống requests
    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)