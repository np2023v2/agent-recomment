from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.schemas import (
    Article,
    User,
    RecommendationRequest,
    RecommendationResponse,
    FeedbackRequest
)
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.post("/articles", response_model=Article)
async def create_article(article: Article):
    """Create a new article."""
    return recommendation_service.add_article(article)


@router.get("/articles", response_model=List[Article])
async def get_articles():
    """Get all articles."""
    return recommendation_service.get_all_articles()


@router.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: str):
    """Get a specific article."""
    article = recommendation_service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/users", response_model=User)
async def create_user(user: User):
    """Create a new user."""
    return recommendation_service.add_user(user)


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a specific user."""
    user = recommendation_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}/history", response_model=List[Article])
async def get_user_history(user_id: str):
    """Get articles viewed by a user."""
    return recommendation_service.get_user_history(user_id)


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get article recommendations for a user using RL-based ranking.
    
    The system uses reinforcement learning to learn user preferences
    and rank articles accordingly.
    """
    articles, scores = recommendation_service.get_recommendations(
        request.user_id,
        request.num_recommendations
    )
    
    return RecommendationResponse(
        user_id=request.user_id,
        articles=articles,
        scores=scores
    )


@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit feedback on a recommended article.
    
    This helps the RL agent learn and improve recommendations.
    Interaction types:
    - 'view': User viewed the article
    - 'like': User liked the article
    - 'share': User shared the article
    - 'skip': User skipped/ignored the article
    """
    recommendation_service.record_interaction(
        feedback.user_id,
        feedback.article_id,
        feedback.interaction_type,
        feedback.duration
    )
    
    return {
        "status": "success",
        "message": "Feedback recorded successfully"
    }


@router.post("/model/save")
async def save_model():
    """Manually save the RL model."""
    recommendation_service.save_model()
    return {
        "status": "success",
        "message": "Model saved successfully"
    }


@router.get("/stats")
async def get_stats():
    """Get system statistics."""
    num_articles = len(recommendation_service.articles)
    num_users = len(recommendation_service.users)
    num_interactions = len(recommendation_service.interactions)
    q_table_size = len(recommendation_service.agent.q_table)
    
    return {
        "num_articles": num_articles,
        "num_users": num_users,
        "num_interactions": num_interactions,
        "q_table_size": q_table_size,
        "epsilon": recommendation_service.agent.epsilon,
        "learning_rate": recommendation_service.agent.learning_rate
    }
