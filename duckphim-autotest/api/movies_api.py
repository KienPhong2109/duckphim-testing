from utils.api_client import ApiClient


class MoviesApi(ApiClient):
    """Lớp con kế thừa ApiClient: mỗi hàm = 1 endpoint của DuckPhim."""

    # API tìm kiếm mà ô search trên web đang gọi -> trả về JSON (list phim)
    def search(self, keyword):
        # params= tự ghép thành ?keyword=... và tự mã hóa tiếng Việt, dấu cách
        return self.get("Movies/SearchApi", params={"keyword": keyword})

    # Mở 1 trang HTML bất kỳ (trang chủ, phim lẻ, chi tiết...) để kiểm status code
    def open_page(self, path):
        return self.get(path)

    # Bấm "Yêu thích" khi CHƯA đăng nhập
    def toggle_favorite(self, movie_id, ajax=False):
        # ajax=True: gửi kèm header mà trình duyệt gửi khi gọi bằng JavaScript
        headers = {"X-Requested-With": "XMLHttpRequest"} if ajax else {}
        # allow_redirects=False: KHÔNG tự đi theo chuyển hướng,
        # để test thấy đúng mã 302 mà server trả về
        return self.post(
            "Account/ToggleFavorite",
            params={"movieId": movie_id},
            headers=headers,
            allow_redirects=False,
        )