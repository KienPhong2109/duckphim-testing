import os

from dotenv import load_dotenv

# Đọc file .env ở thư mục gốc (nếu có) và nạp nội dung vào biến môi trường
load_dotenv()

# Web cần test: DuckPhim. Đọc từ biến môi trường BASE_URL nếu có (để sau này đổi
# sang bản local/staging mà không sửa code), không có thì dùng web thật.
BASE_URL = os.getenv("BASE_URL", "http://duckphim-24.runasp.net")

# Hosting miễn phí đôi khi "ngủ", lần gọi đầu chậm -> cho chờ tối đa 15 giây
TIMEOUT = 15

# Tài khoản kiểm thử: lấy từ file .env, KHÔNG ghi thẳng vào code
TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")