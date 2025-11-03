import sys
sys.path.append('/home/runner/work/agent-recomment/agent-recomment')

from app.schemas.schemas import Article, User
from app.services.recommendation_service import recommendation_service
from datetime import datetime

# Sample articles
articles = [
    Article(
        id="art001",
        title="Introduction to Machine Learning",
        content="Machine learning is a subset of artificial intelligence...",
        category="technology",
        tags=["AI", "ML", "technology"],
        author="John Doe",
        created_at=datetime.now()
    ),
    Article(
        id="art002",
        title="Deep Learning Fundamentals",
        content="Deep learning uses neural networks with multiple layers...",
        category="technology",
        tags=["AI", "deep-learning", "neural-networks"],
        author="Jane Smith",
        created_at=datetime.now()
    ),
    Article(
        id="art003",
        title="Healthy Eating Habits",
        content="Maintaining a balanced diet is crucial for good health...",
        category="health",
        tags=["nutrition", "wellness", "lifestyle"],
        author="Dr. Health",
        created_at=datetime.now()
    ),
    Article(
        id="art004",
        title="Travel Guide to Europe",
        content="Europe offers diverse cultures and beautiful destinations...",
        category="travel",
        tags=["travel", "Europe", "tourism"],
        author="Travel Expert",
        created_at=datetime.now()
    ),
    Article(
        id="art005",
        title="Python Programming Best Practices",
        content="Writing clean and maintainable Python code requires...",
        category="technology",
        tags=["programming", "Python", "coding"],
        author="Code Master",
        created_at=datetime.now()
    ),
    Article(
        id="art006",
        title="Investment Strategies for Beginners",
        content="Starting your investment journey can be overwhelming...",
        category="finance",
        tags=["finance", "investment", "money"],
        author="Finance Guru",
        created_at=datetime.now()
    ),
    Article(
        id="art007",
        title="Yoga for Stress Relief",
        content="Yoga is an ancient practice that helps reduce stress...",
        category="health",
        tags=["yoga", "wellness", "stress-relief"],
        author="Yoga Instructor",
        created_at=datetime.now()
    ),
    Article(
        id="art008",
        title="Climate Change and Its Impact",
        content="Climate change is one of the most pressing issues...",
        category="environment",
        tags=["climate", "environment", "sustainability"],
        author="Environmental Scientist",
        created_at=datetime.now()
    ),
]

# Sample users
users = [
    User(
        id="user001",
        name="Alice",
        preferences=["technology", "health"],
        history=[]
    ),
    User(
        id="user002",
        name="Bob",
        preferences=["travel", "finance"],
        history=[]
    ),
    User(
        id="user003",
        name="Charlie",
        preferences=["technology", "environment"],
        history=[]
    ),
]


def initialize_data():
    """Initialize the system with sample data."""
    print("Initializing sample data...")
    
    # Add articles
    for article in articles:
        recommendation_service.add_article(article)
        print(f"Added article: {article.title}")
    
    # Add users
    for user in users:
        recommendation_service.add_user(user)
        print(f"Added user: {user.name}")
    
    print("\nData initialization complete!")
    print(f"Total articles: {len(recommendation_service.articles)}")
    print(f"Total users: {len(recommendation_service.users)}")


if __name__ == "__main__":
    initialize_data()
