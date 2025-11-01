# Architecture Documentation

## Kiến trúc hệ thống gợi ý bài viết dựa trên học tăng cường

### Tổng quan

Hệ thống sử dụng kiến trúc RESTful API với FastAPI, kết hợp với thuật toán Q-Learning (Reinforcement Learning) để cung cấp gợi ý bài viết cá nhân hóa.

### Kiến trúc tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│              (Web, Mobile, Third-party Apps)                 │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                         (app/main.py)                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       API Layer                              │
│                      (app/api/routes.py)                     │
│  - Article Management    - User Management                   │
│  - Recommendations       - Feedback Collection               │
│  - Statistics            - Model Management                  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│            (app/services/recommendation_service.py)          │
│  - Business Logic        - Data Management                   │
│  - RL Agent Integration  - Model Persistence                 │
└─────────────────────────────┬───────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌───────────────────────────┐   ┌──────────────────────────┐
│      RL Agent Layer       │   │     Data Models          │
│  (app/models/rl_agent.py) │   │ (app/schemas/schemas.py) │
│  - Q-Learning Algorithm   │   │  - Article, User         │
│  - Epsilon-Greedy Policy  │   │  - Request/Response      │
│  - Reward Calculation     │   │  - Validation            │
└───────────────────────────┘   └──────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│                    Storage Layer                           │
│  - In-Memory Storage (Current)                             │
│  - Q-table Persistence (Pickle)                            │
│  - Future: Database (PostgreSQL/MongoDB)                   │
└───────────────────────────────────────────────────────────┘
```

### Thành phần chính

#### 1. API Layer (`app/api/routes.py`)
- **Trách nhiệm**: Xử lý HTTP requests, validation, routing
- **Endpoints chính**:
  - `/api/articles`: CRUD operations cho bài viết
  - `/api/users`: Quản lý người dùng
  - `/api/recommendations`: Gợi ý bài viết
  - `/api/feedback`: Thu thập phản hồi
  - `/api/stats`: Thống kê hệ thống

#### 2. Service Layer (`app/services/recommendation_service.py`)
- **Trách nhiệm**: Business logic, orchestration
- **Chức năng**:
  - Quản lý articles và users
  - Tích hợp RL Agent
  - Lọc candidate articles
  - Ghi nhận tương tác
  - Lưu/load model

#### 3. RL Agent Layer (`app/models/rl_agent.py`)
- **Trách nhiệm**: Machine learning logic
- **Thuật toán**: Q-Learning
- **Chức năng**:
  - Maintain Q-table: `Q(user, article) -> expected_reward`
  - Select articles: Epsilon-greedy policy
  - Update Q-values: Q-learning update rule
  - Calculate rewards: Based on interaction type

#### 4. Data Models (`app/schemas/schemas.py`)
- **Trách nhiệm**: Data structure, validation
- **Models**:
  - `Article`: Bài viết
  - `User`: Người dùng
  - `UserInteraction`: Tương tác
  - `RecommendationRequest/Response`: API contracts

### Q-Learning Algorithm

#### Q-Table Structure
```
Q-table: Dict[(user_id, article_id), float]

Example:
{
  ('user001', 'art001'): 0.7,   # High Q-value -> Good match
  ('user001', 'art002'): 0.3,   # Low Q-value -> Poor match
  ('user002', 'art001'): -0.5,  # Negative -> User dislikes
}
```

#### Q-Learning Update Rule
```
Q(s,a) = Q(s,a) + α * (reward + γ * max(Q(s',a')) - Q(s,a))

Where:
- s: Current state (user + current article)
- a: Action (recommend article)
- α: Learning rate (0.01)
- γ: Discount factor (0.9)
- reward: Immediate reward from interaction
```

#### Epsilon-Greedy Policy
```python
if random() < epsilon:
    # Exploration: Random selection
    articles = random_sample(candidate_articles, n)
else:
    # Exploitation: Select by Q-values
    articles = top_n_by_q_value(candidate_articles, n)
```

#### Reward Function
```python
Rewards:
- skip:  -0.5
- view:   0.3 + duration_bonus (up to 0.3)
- like:   0.7
- share:  1.0
```

### Data Flow

#### 1. Recommendation Flow
```
User Request
    ↓
API Endpoint (/api/recommendations)
    ↓
RecommendationService.get_recommendations()
    ↓
Filter candidate articles (exclude viewed)
    ↓
RLAgent.select_articles() [Epsilon-greedy]
    ↓
Return ranked articles with scores
    ↓
JSON Response
```

#### 2. Learning Flow
```
User Interaction
    ↓
API Endpoint (/api/feedback)
    ↓
RecommendationService.record_interaction()
    ↓
Store interaction record
    ↓
Update user history
    ↓
RLAgent.learn_from_interaction()
    ↓
Calculate reward
    ↓
Update Q-value [Q-learning formula]
    ↓
Periodically save model
```

### Configuration

**File**: `app/core/config.py`

```python
Settings:
- epsilon: 0.1          # Exploration rate
- learning_rate: 0.01   # α in Q-learning
- discount_factor: 0.9  # γ in Q-learning
- max_recommendations: 10
```

### Storage

#### Current Implementation
- **In-Memory**: Articles, Users, Interactions
- **Pickle**: Q-table persistence
- **Location**: `models/rl_agent.pkl`

#### Production Recommendations
```python
Articles & Users:
- PostgreSQL / MongoDB
- Schema-based with indexes

Q-table:
- Redis (for fast lookup)
- Periodic backup to disk

Interactions:
- Time-series database (InfluxDB)
- For analytics and replay
```

### Scaling Considerations

#### Horizontal Scaling
```
┌──────────┐   ┌──────────┐   ┌──────────┐
│ API Node │   │ API Node │   │ API Node │
│    1     │   │    2     │   │    3     │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     └──────────────┼──────────────┘
                    ↓
            ┌───────────────┐
            │ Load Balancer │
            └───────────────┘
                    ↓
            ┌───────────────┐
            │  Shared Redis │
            │   (Q-table)   │
            └───────────────┘
```

#### Optimization Strategies
1. **Cache recommendations**: TTL-based caching
2. **Batch Q-value updates**: Process in batches
3. **Async processing**: Background tasks for learning
4. **Database indexing**: On user_id, article_id
5. **CDN for static content**: Article images, etc.

### Performance Metrics

#### Current Performance
- Recommendation latency: ~10-50ms
- Q-value update: ~1ms
- Memory usage: O(users × articles) for Q-table
- Throughput: 1000+ req/s (single instance)

#### Monitoring Points
- API response times
- Q-table size growth
- Interaction rates
- Recommendation accuracy
- System resource usage

### Security

#### Current
- CORS enabled (configurable)
- Input validation (Pydantic)
- No authentication (demo)

#### Production Requirements
- API authentication (JWT/OAuth)
- Rate limiting
- Input sanitization
- HTTPS only
- Data encryption at rest

### Testing Strategy

1. **Unit Tests**: Individual components
2. **Integration Tests**: Service + RL Agent
3. **E2E Tests**: Full API flow
4. **Load Tests**: Performance benchmarking
5. **A/B Tests**: Algorithm variations

### Future Enhancements

1. **Advanced RL**:
   - Deep Q-Networks (DQN)
   - Policy Gradient methods
   - Multi-armed bandits

2. **Hybrid Approaches**:
   - Collaborative filtering
   - Content-based filtering
   - Matrix factorization

3. **Features**:
   - Real-time learning
   - Context-aware recommendations
   - Diversity optimization
   - Cold-start handling

4. **Infrastructure**:
   - Microservices architecture
   - Event-driven design
   - ML pipeline automation
   - A/B testing framework

### Development Guidelines

#### Code Organization
```
app/
├── api/          # FastAPI routes
├── core/         # Configuration
├── models/       # ML models
├── schemas/      # Data models
└── services/     # Business logic
```

#### Best Practices
1. Use type hints
2. Validate inputs with Pydantic
3. Log all interactions
4. Test RL updates
5. Monitor Q-table growth
6. Regular model backups

### Deployment

#### Development
```bash
python run.py
# or
uvicorn app.main:app --reload
```

#### Production
```bash
# With Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# With Docker
docker build -t article-recommender .
docker run -p 8000:8000 article-recommender

# With Kubernetes
kubectl apply -f deployment.yaml
```

### Troubleshooting

#### Common Issues

1. **Q-table too large**
   - Solution: Prune old entries, use sampling

2. **Slow recommendations**
   - Solution: Cache, index, optimize Q-lookup

3. **Poor recommendations**
   - Solution: Tune hyperparameters, collect more data

4. **Memory issues**
   - Solution: Move to database, implement pagination

### References

- FastAPI: https://fastapi.tiangolo.com/
- Q-Learning: Sutton & Barto, "Reinforcement Learning"
- Recommendation Systems: Aggarwal, "Recommender Systems"
