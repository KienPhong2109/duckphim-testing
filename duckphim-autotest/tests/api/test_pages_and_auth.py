import pytest

from config import data

pytestmark = pytest.mark.api


# TC-10: 8 trang chính của website đều phải mở được (mã 200)
# parametrize: 1 hàm chạy 8 lần, mỗi lần 1 trang -> trang nào hỏng thì biết ngay trang đó
@pytest.mark.smoke
@pytest.mark.parametrize("path", data.MAIN_PAGES)
def test_tc10_main_page_is_available(movies_api, path, evidence):
    # Fail -> mở thẳng trang này trên trình duyệt để chụp màn hình
    evidence.open_page(path)

    assert movies_api.open_page(path).status_code == 200


# TC-11: phân vùng không hợp lệ (id không tồn tại, id không phải số, đường dẫn sai)
# đều phải trả về mã 404
@pytest.mark.parametrize("path", data.INVALID_PATHS)
def test_tc11_invalid_page_returns_404(movies_api, path, evidence):
    evidence.open_page(path)

    assert movies_api.open_page(path).status_code == 404


# TC-12: bấm yêu thích khi CHƯA đăng nhập -> server chuyển hướng về trang đăng nhập
def test_tc12_favorite_without_login_redirects_to_login(movies_api):
    response = movies_api.toggle_favorite(data.MOVIE_ID)

    # 302 = server bảo "đi chỗ khác", header Location cho biết đi đâu
    assert response.status_code == 302
    assert "/Account/Login" in response.headers["Location"]


# TC-13: cũng thao tác đó nhưng gọi kiểu AJAX (như JavaScript của web đang gọi)
# -> server phải trả 401 (chưa xác thực) thay vì chuyển trang
def test_tc13_favorite_ajax_without_login_returns_401(movies_api):
    response = movies_api.toggle_favorite(data.MOVIE_ID, ajax=True)

    assert response.status_code == 401