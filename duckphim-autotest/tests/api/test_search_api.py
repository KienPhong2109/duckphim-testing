import pytest

from config import data

# Gắn nhãn "api" cho TẤT CẢ test trong file
pytestmark = pytest.mark.api


# TC-01: từ khóa có trong hệ thống -> mã 200, dữ liệu JSON, có ít nhất 1 phim
@pytest.mark.smoke
def test_tc01_search_returns_results(movies_api):
    response = movies_api.search(data.KEYWORD_DORAEMON)

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]
    assert len(response.json()) > 0


# TC-02: mỗi phim trong kết quả phải có đủ các trường
def test_tc02_search_result_schema(movies_api):
    movies = movies_api.search(data.KEYWORD_CONAN).json()

    # Phải có phim thì vòng for bên dưới mới thật sự kiểm tra được gì đó
    assert len(movies) > 0, "Không có phim nào để kiểm tra cấu trúc"
    for movie in movies:
        for field in data.MOVIE_FIELDS:
            assert field in movie, f"Phim id={movie.get('id')} thiếu trường '{field}'"
        assert movie["type"] in data.MOVIE_TYPES
        assert movie["viewCount"] >= 0


# TC-03 (chữ HOA) và TC-04 (tiếng Việt có dấu), chạy kèm 2 từ khóa thường để đối chứng
# parametrize: 1 hàm chạy 4 lần, mỗi lần 1 từ khóa
@pytest.mark.parametrize("keyword", data.KEYWORDS_FOUND)
def test_tc03_tc04_search_titles_contain_keyword(movies_api, keyword):
    movies = movies_api.search(keyword).json()

    assert len(movies) > 0
    for movie in movies:
        # .lower() để so sánh không phân biệt hoa/thường
        assert keyword.lower() in movie["title"].lower()


# TC-05: tìm kiếm bằng tiếng Việt không dấu
def test_tc05_search_without_diacritics(movies_api, evidence):
    # Nếu test này fail -> tái hiện bằng cách gõ từ khóa này vào ô tìm kiếm
    evidence.search(data.KEYWORD_NO_DIACRITICS)

    movies = movies_api.search(data.KEYWORD_NO_DIACRITICS).json()
    assert len(movies) > 0, "Hệ thống chưa hỗ trợ tìm kiếm tiếng Việt không dấu!"


# TC-06: từ khóa không có kết quả -> mã 200, danh sách rỗng
def test_tc06_search_not_found_returns_empty_list(movies_api):
    response = movies_api.search(data.KEYWORD_NOT_FOUND)

    assert response.status_code == 200
    assert response.json() == []


# TC-07: từ khóa rỗng -> web vẫn trả về danh sách phim gợi ý
def test_tc07_search_empty_keyword_returns_suggestions(movies_api):
    assert len(movies_api.search("").json()) > 0


# TC-08: dữ liệu bất thường không được làm máy chủ lỗi 500 hay lộ hết dữ liệu
@pytest.mark.parametrize("keyword", data.KEYWORDS_ABNORMAL)
def test_tc08_search_abnormal_input_is_safe(movies_api, keyword):
    response = movies_api.search(keyword)

    assert response.status_code == 200
    assert response.json() == []


# TC-09 (phi chức năng): API tìm kiếm phải phản hồi dưới 3 giây
def test_tc09_search_response_time(movies_api):
    response = movies_api.search(data.KEYWORD_CONAN)
    assert response.elapsed.total_seconds() < data.MAX_RESPONSE_SECONDS