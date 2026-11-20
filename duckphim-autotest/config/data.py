"""Dữ liệu kiểm thử dùng chung cho test API và test UI (Bảng 6 trong báo cáo).
Khai báo tập trung ở đây: dữ liệu trên web đổi thì chỉ sửa 1 file này."""

# --- Từ khóa có kết quả ---
KEYWORD_DORAEMON = "doraemon"
KEYWORD_CONAN = "conan"
# thường, HOA, tiếng Việt có dấu
KEYWORDS_FOUND = ["doraemon", "DORAEMON", "conan", "người nhện"]

# --- Từ khóa không dấu (web chưa hỗ trợ) ---
KEYWORD_NO_DIACRITICS = "nguoi nhen"

# --- Từ khóa không có kết quả ---
KEYWORD_NOT_FOUND = "zzzxxqqq"

# --- Từ khóa bất thường: chuỗi dạng SQL, thẻ HTML, ký tự đặc biệt, chuỗi 300 ký tự ---
KEYWORDS_ABNORMAL = ["' OR 1=1 --", "<script>", "%", "a" * 300]
KEYWORD_PARENTHESIS = "Conan (Lồng"      # dấu ngoặc đơn (TC-17)
KEYWORD_HTML = "<b>xyzq</b>"             # thẻ HTML (TC-18)

# --- Các trường mà 1 phim trong kết quả tìm kiếm bắt buộc phải có ---
MOVIE_FIELDS = ["id", "title", "posterUrl", "type", "country", "viewCount"]
MOVIE_TYPES = ("Phim Lẻ", "Phim Bộ")

# --- Phim mẫu. Nếu phim này bị xóa khỏi web thì đổi id và tên khác ---
MOVIE_ID = 360
MOVIE_TITLE = "Mị Ảnh Thần Bộ"

# --- Các trang chính (TC-10) và đường dẫn không hợp lệ (TC-11) ---
MAIN_PAGES = [
    "Movies",
    "Movies/PhimLe",
    "Movies/PhimBo",
    "Movies/AdvancedSearch",
    "Movies/Category/1",
    f"Movies/Details/{MOVIE_ID}",
    "Account/Login",
    "Account/Register",
]
INVALID_PATHS = ["Movies/Details/999999", "Movies/Details/abc", "trang-khong-ton-tai"]

# --- Ngưỡng phi chức năng: API tìm kiếm phải trả lời trong 3 giây (TC-09) ---
MAX_RESPONSE_SECONDS = 3
# --- Lọc phim trong Kho phim (TC-19, TC-20). Ghi đúng chữ hiển thị trong ô chọn ---
FILTER_CATEGORY = "Hoạt hình"
FILTER_TYPE = "Phim lẻ"
# TC-19 mở trang chi tiết của vài phim đầu để kiểm tra thể loại (kiểm tra lấy mẫu)
FILTER_SAMPLE_SIZE = 3