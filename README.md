# Agent-Recomment - Hệ thống gợi ý bài viết dựa trên học tăng cường

Hệ thống ứng dụng học tăng cường (Reinforcement Learning) để gợi ý và sắp xếp bài viết cho người dùng, được xây dựng bằng FastAPI và Python.

## Tính năng

- 🤖 **Học tăng cường (Q-Learning)**: Sử dụng thuật toán Q-Learning để học từ tương tác người dùng và cải thiện gợi ý theo thời gian
- 🎯 **Gợi ý cá nhân hóa**: Gợi ý bài viết phù hợp với sở thích của từng người dùng
- 📊 **Sắp xếp thông minh**: Sắp xếp bài viết dựa trên Q-values được học
- 🔄 **Học liên tục**: Hệ thống học và cải thiện từ mỗi tương tác người dùng
- ⚡ **API nhanh**: Xây dựng trên FastAPI với hiệu suất cao
- 📈 **Theo dõi thống kê**: Endpoints để theo dõi hiệu suất hệ thống

## Cấu trúc dự án

```
agent-recomment/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Cấu hình ứng dụng
│   ├── models/
│   │   ├── __init__.py
│   │   └── rl_agent.py        # RL Agent (Q-Learning)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── recommendation_service.py  # Business logic
│   ├── __init__.py
│   └── main.py                # FastAPI application
├── data/
│   └── init_data.py           # Dữ liệu mẫu
├── models/                     # Lưu trữ RL model
├── .gitignore
├── requirements.txt
└── README.md
```

## Cài đặt

### Yêu cầu
- Python 3.8+
- pip

### Các bước cài đặt

1. Clone repository:
```bash
git clone https://github.com/np2023v2/agent-recomment.git
cd agent-recomment
```

2. Tạo môi trường ảo (khuyến nghị):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

## Sử dụng

### 1. Khởi động server

```bash
python -m uvicorn app.main:app --reload
```

Server sẽ chạy tại: `http://localhost:8000`

### 2. Khởi tạo dữ liệu mẫu

Trong terminal khác:
```bash
python data/init_data.py
```

### 3. Truy cập API Documentation

Mở trình duyệt và truy cập:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Articles (Bài viết)

- `POST /api/articles` - Tạo bài viết mới
- `GET /api/articles` - Lấy tất cả bài viết
- `GET /api/articles/{article_id}` - Lấy bài viết theo ID

### Users (Người dùng)

- `POST /api/users` - Tạo người dùng mới
- `GET /api/users/{user_id}` - Lấy thông tin người dùng
- `GET /api/users/{user_id}/history` - Lấy lịch sử xem bài viết

### Recommendations (Gợi ý)

- `POST /api/recommendations` - Lấy gợi ý bài viết cho người dùng
  ```json
  {
    "user_id": "user001",
    "num_recommendations": 5
  }
  ```

### Feedback (Phản hồi)

- `POST /api/feedback` - Gửi phản hồi về bài viết
  ```json
  {
    "user_id": "user001",
    "article_id": "art001",
    "interaction_type": "like",
    "duration": 120.5
  }
  ```
  
  Các loại tương tác:
  - `view`: Xem bài viết
  - `like`: Thích bài viết
  - `share`: Chia sẻ bài viết
  - `skip`: Bỏ qua bài viết

### System (Hệ thống)

- `GET /api/stats` - Lấy thống kê hệ thống
- `POST /api/model/save` - Lưu model RL
- `GET /health` - Kiểm tra sức khỏe hệ thống

## Cách thức hoạt động của RL Agent

### Q-Learning Algorithm

Hệ thống sử dụng Q-Learning, một thuật toán Reinforcement Learning:

1. **Q-Table**: Lưu trữ giá trị Q cho mỗi cặp (user, article)
2. **Epsilon-Greedy**: Cân bằng giữa exploration (khám phá) và exploitation (khai thác)
3. **Reward System**:
   - Skip: -0.5 (phạt khi bỏ qua)
   - View: 0.3 + duration bonus (thưởng khi xem)
   - Like: 0.7 (thưởng cao khi thích)
   - Share: 1.0 (thưởng tối đa khi chia sẻ)

4. **Q-Value Update**:
   ```
   Q(s,a) = Q(s,a) + α * (reward + γ * max(Q(s',a')) - Q(s,a))
   ```
   - α (learning_rate): Tốc độ học
   - γ (discount_factor): Giá trị tương lai

### Quy trình gợi ý

1. User yêu cầu gợi ý
2. Hệ thống lấy các bài viết chưa xem
3. RL Agent chọn bài viết dựa trên Q-values
4. Trả về danh sách bài viết được xếp hạng
5. User tương tác với bài viết
6. Hệ thống cập nhật Q-values dựa trên feedback

## Ví dụ sử dụng

### 1. Lấy gợi ý bài viết

```bash
curl -X POST "http://localhost:8000/api/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user001",
    "num_recommendations": 5
  }'
```

### 2. Gửi feedback

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

### 3. Xem thống kê

```bash
curl "http://localhost:8000/api/stats"
```

## Cấu hình

Chỉnh sửa `app/core/config.py` để thay đổi:

- `epsilon`: Tỷ lệ exploration (mặc định: 0.1)
- `learning_rate`: Tốc độ học (mặc định: 0.01)
- `discount_factor`: Hệ số chiết khấu (mặc định: 0.9)
- `max_recommendations`: Số gợi ý tối đa (mặc định: 10)

## Phát triển

### Chạy tests (nếu có)
```bash
pytest
```

### Code formatting
```bash
black app/
```

### Type checking
```bash
mypy app/
```

## Công nghệ sử dụng

- **FastAPI**: Web framework hiện đại, nhanh
- **Pydantic**: Data validation
- **NumPy**: Tính toán số học
- **Uvicorn**: ASGI server
- **Python 3.8+**: Ngôn ngữ lập trình

## Tính năng tương lai

- [ ] Persistent storage với database (PostgreSQL/MongoDB)
- [ ] Deep Q-Learning với neural networks
- [ ] Multi-armed bandit algorithms
- [ ] A/B testing framework
- [ ] Real-time analytics dashboard
- [ ] User clustering và collaborative filtering
- [ ] Content-based filtering
- [ ] Hybrid recommendation system

## License

MIT License

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.

## Liên hệ

- Repository: https://github.com/np2023v2/agent-recomment
- Issues: https://github.com/np2023v2/agent-recomment/issues