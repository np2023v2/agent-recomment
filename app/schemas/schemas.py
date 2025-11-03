from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Article(BaseModel):
    """Article model."""
    
    id: str
    title: str
    content: str
    category: str
    tags: List[str] = Field(default_factory=list)
    author: str
    created_at: datetime = Field(default_factory=datetime.now)
    views: int = 0
    likes: int = 0


class User(BaseModel):
    """User model."""
    
    id: str
    name: str
    preferences: List[str] = Field(default_factory=list)  # Preferred categories
    history: List[str] = Field(default_factory=list)  # Article IDs viewed


class UserInteraction(BaseModel):
    """User interaction with an article."""
    
    user_id: str
    article_id: str
    interaction_type: str  # 'view', 'like', 'share', 'skip'
    timestamp: datetime = Field(default_factory=datetime.now)
    duration: Optional[float] = None  # Time spent on article in seconds


class RecommendationRequest(BaseModel):
    """Request for article recommendations."""
    
    user_id: str
    num_recommendations: int = 5
    

class RecommendationResponse(BaseModel):
    """Response with recommended articles."""
    
    user_id: str
    articles: List[Article]
    scores: List[float]  # Confidence scores for each recommendation


class FeedbackRequest(BaseModel):
    """Feedback on a recommendation."""
    
    user_id: str
    article_id: str
    interaction_type: str  # 'view', 'like', 'share', 'skip'
    duration: Optional[float] = None
