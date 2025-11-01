from typing import Dict, List, Optional
from app.schemas.schemas import Article, User, UserInteraction
from app.models.rl_agent import RLAgent
from app.core.config import settings
from datetime import datetime


class RecommendationService:
    """Service for managing article recommendations."""
    
    def __init__(self):
        """Initialize the recommendation service."""
        # Initialize RL agent
        self.agent = RLAgent(
            epsilon=settings.epsilon,
            learning_rate=settings.learning_rate,
            discount_factor=settings.discount_factor
        )
        
        # In-memory storage (in production, use a database)
        self.articles: Dict[str, Article] = {}
        self.users: Dict[str, User] = {}
        self.interactions: List[UserInteraction] = []
        
        # Load existing model if available
        self.agent.load_model('models/rl_agent.pkl')
    
    def add_article(self, article: Article) -> Article:
        """Add a new article."""
        self.articles[article.id] = article
        return article
    
    def get_article(self, article_id: str) -> Optional[Article]:
        """Get an article by ID."""
        return self.articles.get(article_id)
    
    def get_all_articles(self) -> List[Article]:
        """Get all articles."""
        return list(self.articles.values())
    
    def add_user(self, user: User) -> User:
        """Add a new user."""
        self.users[user.id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)
    
    def get_candidate_articles(self, user_id: str) -> List[str]:
        """
        Get candidate articles for a user.
        Filters out articles the user has already viewed.
        """
        user = self.get_user(user_id)
        if not user:
            # If user not found, return all articles
            return list(self.articles.keys())
        
        # Filter out already viewed articles
        viewed_articles = set(user.history)
        candidate_articles = [
            article_id for article_id in self.articles.keys()
            if article_id not in viewed_articles
        ]
        
        # If user has viewed all articles, reset and show all
        if not candidate_articles:
            candidate_articles = list(self.articles.keys())
        
        return candidate_articles
    
    def get_recommendations(
        self,
        user_id: str,
        num_recommendations: int = 5
    ) -> tuple[List[Article], List[float]]:
        """
        Get article recommendations for a user.
        
        Args:
            user_id: User ID
            num_recommendations: Number of articles to recommend
            
        Returns:
            Tuple of (articles, scores)
        """
        # Ensure user exists
        if user_id not in self.users:
            # Create a default user if not exists
            self.add_user(User(id=user_id, name=f"User {user_id}"))
        
        # Get candidate articles
        candidate_articles = self.get_candidate_articles(user_id)
        
        if not candidate_articles:
            return [], []
        
        # Use RL agent to select articles
        num_recommendations = min(
            num_recommendations,
            settings.max_recommendations,
            len(candidate_articles)
        )
        
        selected = self.agent.select_articles(
            user_id,
            candidate_articles,
            num_recommendations
        )
        
        # Get article objects
        articles = []
        scores = []
        for article_id, score in selected:
            article = self.get_article(article_id)
            if article:
                articles.append(article)
                scores.append(score)
        
        return articles, scores
    
    def record_interaction(
        self,
        user_id: str,
        article_id: str,
        interaction_type: str,
        duration: Optional[float] = None
    ):
        """
        Record a user interaction and update the RL agent.
        
        Args:
            user_id: User ID
            article_id: Article ID
            interaction_type: Type of interaction ('view', 'like', 'share', 'skip')
            duration: Time spent on article (seconds)
        """
        # Create interaction record
        interaction = UserInteraction(
            user_id=user_id,
            article_id=article_id,
            interaction_type=interaction_type,
            duration=duration,
            timestamp=datetime.now()
        )
        self.interactions.append(interaction)
        
        # Update user history
        user = self.get_user(user_id)
        if user and article_id not in user.history:
            user.history.append(article_id)
        
        # Update article metrics
        article = self.get_article(article_id)
        if article:
            if interaction_type == 'view':
                article.views += 1
            elif interaction_type == 'like':
                article.likes += 1
        
        # Get next candidate articles for Q-learning
        candidate_articles = self.get_candidate_articles(user_id)
        
        # Update RL agent
        self.agent.learn_from_interaction(
            user_id,
            article_id,
            interaction_type,
            duration,
            candidate_articles
        )
        
        # Periodically save the model
        if len(self.interactions) % 10 == 0:
            self.save_model()
    
    def save_model(self):
        """Save the RL agent model."""
        self.agent.save_model('models/rl_agent.pkl')
    
    def get_user_history(self, user_id: str) -> List[Article]:
        """Get articles viewed by a user."""
        user = self.get_user(user_id)
        if not user:
            return []
        
        articles = []
        for article_id in user.history:
            article = self.get_article(article_id)
            if article:
                articles.append(article)
        
        return articles


# Global service instance
recommendation_service = RecommendationService()
