# User and Item Profile Recommendations

Tập tin Python này chứa các hàm để tạo/lưu hồ sơ người dùng và mặt hàng và nhận gợi ý cho người dùng dựa trên độ tương tự cosin.

## Requirements

pip install -r requirements.txt

## Sử dụng

Các bước để sử dụng mô hình gợi ý

### Tạo và Lưu Ma Trận TF-IDF (chạy một lần/mỗi khi update dữ liệu phim)

Sử dụng hàm create_and_save_tfidf_matrix_v1(documents, filename) để tạo và lưu ma trận TF-IDF(với cái tf-idf vectorizer).

![ad](https://github.com/nhat2520/Letfnix/assets/161301206/05b2be77-5326-415e-91d5-a54f5f7d69de)

### Tạo và Lưu Hồ Sơ Người Dùng và Ma Trận Tương Đồng (chạy mỗi khi có người dùng mới)

Sử dụng hàm create_and_save_user_profile(user_id, tfidf_matrix_filename) để tạo và lưu hồ sơ người dùng dựa trên ma trận TF-IDF.
Sử dụng hàm calculate_and_save_similarity_matrix(user_id, tfidf_matrix_filename) để tính toán và lưu ma trận tương đồng cosine cho một hồ sơ người dùng.

![ad](https://github.com/nhat2520/Letfnix/assets/161301206/fde61eba-e55a-4e51-abf6-036d7b48542e)

### Tạo Recommendation Cho Người Dùng (chạy khi cần recommendation)

Sử dụng hàm get_recommendations(user_id, n_rec) để nhận n_rec số gợi ý hàng đầu cho một người dùng dựa trên ma trận tương đồng cosine.

![ad](https://github.com/nhat2520/Letfnix/assets/161301206/d145d5cb-c399-41e8-bcdb-16a2eeefc818)


### Cập Nhật Hồ Sơ Người Dùng và Ma Trận Tương Đồng (chạy khi người dùng tương tác với trang web)

Sử dụng hàm update_user_and_similarity_matrix(user_id, movie_idx, action, tfidf_matrix_filename) để cập nhật hồ sơ người dùng và ma trận tương đồng cosine dựa trên các hành động của người dùng.
Chuyển ID người dùng (user_id), chỉ số phim (movie_idx), hành động ('view' hoặc 'buy'), và tên tệp của ma trận TF-IDF đã lưu (tfidf_matrix_filename).

Để biết thêm chi tiết, tham khảo các docstrings trong tập tin Python.
