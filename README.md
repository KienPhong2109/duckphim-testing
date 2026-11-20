# DuckPhim Testing

Dự án kiểm thử website xem phim **DuckPhim** (http://duckphim-24.runasp.net), gồm:

- **Automation test bằng Python**: test API với `requests`, test giao diện với `Selenium`, chạy bằng `pytest`.
- **Test case** viết tay (Excel).
- **Danh sách lỗi** (bug list) tìm được trong quá trình kiểm thử.
- **Ảnh chụp màn hình** làm bằng chứng cho các test không đạt.

## Cấu trúc thư mục

```
duckphim-testing/
├── duckphim-autotest/        # Code automation test (Python)
│   ├── api/                  # Lớp gọi API của DuckPhim (MoviesApi)
│   ├── config/               # Cấu hình (URL, timeout, tài khoản) và dữ liệu kiểm thử
│   ├── pages/                # Page Object: mỗi trang web là một lớp, kế thừa BasePage
│   ├── tests/
│   │   ├── api/              # TC-01 → TC-13: test API
│   │   └── ui/               # TC-14 → TC-27: test giao diện
│   ├── utils/                # ApiClient, ghi log từng bước, thu thập bằng chứng
│   ├── conftest.py           # Fixture dùng chung, tự chụp màn hình khi test fail
│   ├── pytest.ini
│   └── requirements.txt
├── test-cases/               # DuckPhim_TestCase.xlsx
├── bug-reports/              # Duckphim_BugList.xlsx
└── screenshots/              # Ảnh bằng chứng các test không đạt
```

## Phạm vi kiểm thử

27 test case, mỗi hàm test được gắn mã TC trong tên (ví dụ `test_tc14_...`):

| Nhóm | Mã TC | Nội dung |
|---|---|---|
| API – Tìm kiếm | TC-01 → TC-09 | Tìm phim theo tên, có dấu/không dấu, ký tự đặc biệt, từ khóa không tồn tại |
| API – Trang & đăng nhập | TC-10 → TC-13 | Các trang chính phản hồi đúng, kiểm tra luồng xác thực |
| UI – Tìm kiếm | TC-14 → TC-18 | Hộp tìm kiếm, gợi ý, kết quả tìm trực tiếp (live search) |
| UI – Lọc phim | TC-19, TC-20 | Lọc theo thể loại, loại phim (lẻ/bộ) ở Kho phim |
| UI – Chi tiết phim | TC-21, TC-22 | Thông tin phim, nút "Xem thêm / Thu gọn" mô tả |
| UI – Yêu thích | TC-23 | Bấm yêu thích khi chưa đăng nhập |
| UI – Đăng nhập | TC-24 → TC-27 | Bỏ trống, sai mật khẩu, hiện/ẩn mật khẩu, đăng nhập đúng |

## Kết quả

**23/27 test case đạt, 4 không đạt.**

| Mã TC | Kết quả | Ghi chú |
|---|---|---|
| TC-05 | Không đạt | Tìm phim không dấu không ra kết quả (đề xuất cải tiến) |
| TC-17 | Không đạt | BUG-02: gõ từ khóa có dấu ngoặc `(` thì live search báo "Lỗi mất kết nối tới API máy chủ!" |
| TC-18 | Không đạt | BUG-03: từ khóa chứa thẻ HTML (`<b>...</b>`) bị hiển thị thành HTML thật thay vì chữ thường |
| TC-23 | Không đạt | BUG-01: bấm yêu thích khi chưa đăng nhập thì không có thông báo, không chuyển sang trang đăng nhập |

Chi tiết từng lỗi xem trong `bug-reports/Duckphim_BugList.xlsx`, ảnh chụp trong `screenshots/`.

## Cài đặt và chạy

Yêu cầu: Python 3.10+ và Google Chrome.

```bash
cd duckphim-autotest

# Tạo môi trường ảo và cài thư viện
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Tạo file `.env` trong `duckphim-autotest/` để chạy các test cần đăng nhập (không có file này thì các test đó được bỏ qua):

```
TEST_USERNAME=ten_tai_khoan_test
TEST_PASSWORD=mat_khau_test
# BASE_URL=http://duckphim-24.runasp.net   (tùy chọn, mặc định là web thật)
```

> File `.env` đã nằm trong `.gitignore`, không bao giờ đẩy lên GitHub.

### Các lệnh chạy test

```bash
pytest                       # chạy tất cả
pytest -m api                # chỉ test API
pytest -m ui                 # chỉ test giao diện
pytest -m smoke              # test nhanh để biết web còn hoạt động
pytest -k tc14               # chạy riêng một test case
pytest --html=reports/report.html --self-contained-html   # xuất báo cáo HTML
```

Khi một test không đạt:

- **Test giao diện**: tự chụp màn hình ngay lúc fail.
- **Test API**: tự mở Chrome, thao tác lại kịch bản trên giao diện rồi chụp màn hình.

Ảnh được lưu vào `duckphim-autotest/reports/screenshots/` và được dọn sạch ở mỗi lần chạy mới.

## Công nghệ

- Python, pytest, pytest-html
- requests (test API)
- Selenium WebDriver + Page Object Model (test giao diện)
- python-dotenv (đọc tài khoản test từ `.env`)

## Tác giả

**Chung Kiến Phong** ([@KienPhong2109](https://github.com/KienPhong2109)): tester, viết test case, automation test và báo cáo lỗi cho DuckPhim.
