# Quick Start Guide

## Bắt đầu nhanh với hệ thống gợi ý bài viết

### 1. Cài đặt

```bash
# Clone repository
git clone https://github.com/np2023v2/agent-recomment.git
cd agent-recomment

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Chạy server

```bash
python -m uvicorn app.main:app --reload
```

Server sẽ chạy tại: http://localhost:8000

### 3. Thử nghiệm hệ thống

Trong terminal khác, chạy:

```bash
python test_system.py
```

### 4. Truy cập API Documentation

Mở trình duyệt và truy cập:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

### 5. Ví dụ sử dụng API

#### Tạo bài viết mới

```bash
curl -X POST "http://localhost:8000/api/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "art001",
    "title": "My Article",
    "content": "Article content here...",
    "category": "technology",
    "tags": ["tech", "AI"],
    "author": "Author Name",
    "created_at": "2024-01-01T00:00:00",
    "views": 0,
    "likes": 0
  }'
```

#### Tạo người dùng

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user001",
    "name": "John Doe",
    "preferences": ["technology", "health"],
    "history": []
  }'
```

#### Lấy gợi ý bài viết

```bash
curl -X POST "http://localhost:8000/api/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user001",
    "num_recommendations": 5
  }'
```

#### Gửi feedback

```bash
curl -X POST "http://localhost:8000/api/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user001",
    "article_id": "art001",
    "interaction_type": "like",
    "duration": 120.5
  }'
```

### 6. Hiểu về hệ thống

Hệ thống sử dụng **Q-Learning** (Reinforcement Learning) để học từ tương tác người dùng:

1. **Ban đầu**: Gợi ý ngẫu nhiên hoặc dựa trên exploration
2. **Sau tương tác**: Hệ thống học giá trị Q cho mỗi cặp (user, article)
3. **Cải thiện**: Càng nhiều tương tác, gợi ý càng chính xác

**Loại tương tác và reward:**
- `skip`: -0.5 (phạt)
- `view`: 0.3 + duration bonus
- `like`: 0.7
- `share`: 1.0 (tốt nhất)

### 7. Xem thống kê

```bash
curl http://localhost:8000/api/stats
```

Kết quả sẽ hiển thị:
- Số lượng bài viết
- Số lượng người dùng
- Số lượng tương tác
- Kích thước Q-table
- Tham số RL (epsilon, learning rate)

### Lưu ý

- Model RL tự động lưu sau mỗi 10 tương tác
- Có thể lưu thủ công: `POST /api/model/save`
- Dữ liệu lưu trong bộ nhớ (trong production nên dùng database)
