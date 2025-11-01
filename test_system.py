#!/usr/bin/env python3
"""
Test script for the Article Recommendation System.
This script demonstrates the full workflow of the RL-based recommendation system.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def test_health():
    """Test health endpoint."""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def create_sample_data():
    """Create sample articles and users."""
    print_section("Creating Sample Data")
    
    # Create articles
    articles = [
        {
            "id": "art001",
            "title": "Introduction to Machine Learning",
            "content": "Machine learning is a subset of artificial intelligence...",
            "category": "technology",
            "tags": ["AI", "ML", "technology"],
            "author": "John Doe",
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "likes": 0
        },
        {
            "id": "art002",
            "title": "Deep Learning Fundamentals",
            "content": "Deep learning uses neural networks with multiple layers...",
            "category": "technology",
            "tags": ["AI", "deep-learning", "neural-networks"],
            "author": "Jane Smith",
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "likes": 0
        },
        {
            "id": "art003",
            "title": "Healthy Eating Habits",
            "content": "Maintaining a balanced diet is crucial for good health...",
            "category": "health",
            "tags": ["nutrition", "wellness", "lifestyle"],
            "author": "Dr. Health",
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "likes": 0
        },
        {
            "id": "art004",
            "title": "Travel Guide to Europe",
            "content": "Europe offers diverse cultures and beautiful destinations...",
            "category": "travel",
            "tags": ["travel", "Europe", "tourism"],
            "author": "Travel Expert",
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "likes": 0
        },
        {
            "id": "art005",
            "title": "Python Programming Best Practices",
            "content": "Writing clean and maintainable Python code requires...",
            "category": "technology",
            "tags": ["programming", "Python", "coding"],
            "author": "Code Master",
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "likes": 0
        }
    ]
    
    for article in articles:
        response = requests.post(f"{BASE_URL}/api/articles", json=article)
        if response.status_code == 200:
            print(f"✓ Created article: {article['title']}")
        else:
            print(f"✗ Failed to create article: {article['title']}")
    
    # Create users
    users = [
        {
            "id": "user001",
            "name": "Alice",
            "preferences": ["technology", "health"],
            "history": []
        },
        {
            "id": "user002",
            "name": "Bob",
            "preferences": ["travel", "finance"],
            "history": []
        }
    ]
    
    for user in users:
        response = requests.post(f"{BASE_URL}/api/users", json=user)
        if response.status_code == 200:
            print(f"✓ Created user: {user['name']}")
        else:
            print(f"✗ Failed to create user: {user['name']}")


def get_recommendations(user_id, num_recommendations=3):
    """Get article recommendations for a user."""
    print_section(f"Getting Recommendations for {user_id}")
    
    payload = {
        "user_id": user_id,
        "num_recommendations": num_recommendations
    }
    
    response = requests.post(f"{BASE_URL}/api/recommendations", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"User ID: {data['user_id']}")
        print(f"Number of recommendations: {len(data['articles'])}")
        print("\nRecommended Articles:")
        for i, (article, score) in enumerate(zip(data['articles'], data['scores']), 1):
            print(f"  {i}. {article['title']}")
            print(f"     Category: {article['category']}")
            print(f"     Score: {score:.3f}")
            print(f"     Tags: {', '.join(article['tags'])}")
        return data
    else:
        print(f"Error: {response.status_code}")
        return None


def submit_feedback(user_id, article_id, interaction_type, duration=None):
    """Submit feedback on an article."""
    payload = {
        "user_id": user_id,
        "article_id": article_id,
        "interaction_type": interaction_type
    }
    if duration:
        payload["duration"] = duration
    
    response = requests.post(f"{BASE_URL}/api/feedback", json=payload)
    
    if response.status_code == 200:
        print(f"✓ Feedback recorded: {interaction_type} for article {article_id}")
    else:
        print(f"✗ Failed to record feedback")


def simulate_user_interactions():
    """Simulate user interactions to train the RL agent."""
    print_section("Simulating User Interactions")
    
    # User 1 (Alice) - likes technology and health
    print("\n--- Alice's interactions ---")
    submit_feedback("user001", "art001", "like")
    submit_feedback("user001", "art002", "view", duration=120.5)
    submit_feedback("user001", "art003", "like")
    submit_feedback("user001", "art004", "skip")
    
    # User 2 (Bob) - likes travel
    print("\n--- Bob's interactions ---")
    submit_feedback("user002", "art004", "like")
    submit_feedback("user002", "art001", "view", duration=45.0)
    submit_feedback("user002", "art005", "skip")


def get_stats():
    """Get system statistics."""
    print_section("System Statistics")
    
    response = requests.get(f"{BASE_URL}/api/stats")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"Number of articles: {stats['num_articles']}")
        print(f"Number of users: {stats['num_users']}")
        print(f"Number of interactions: {stats['num_interactions']}")
        print(f"Q-table size: {stats['q_table_size']}")
        print(f"Epsilon (exploration rate): {stats['epsilon']}")
        print(f"Learning rate: {stats['learning_rate']}")
    else:
        print(f"Error: {response.status_code}")


def main():
    """Main test function."""
    print_section("Article Recommendation System - Test Suite")
    
    # Wait for server to be ready
    print("\nWaiting for server to start...")
    time.sleep(2)
    
    # Test health
    if not test_health():
        print("❌ Server is not healthy!")
        return
    
    # Create sample data
    create_sample_data()
    
    # Get initial recommendations (before training)
    print("\n" + "🔹" * 30)
    print(" INITIAL RECOMMENDATIONS (Before Training)")
    print("🔹" * 30)
    get_recommendations("user001", num_recommendations=3)
    get_recommendations("user002", num_recommendations=3)
    
    # Simulate interactions to train the agent
    simulate_user_interactions()
    
    # Get recommendations after training
    print("\n" + "🔹" * 30)
    print(" UPDATED RECOMMENDATIONS (After Training)")
    print("🔹" * 30)
    get_recommendations("user001", num_recommendations=3)
    get_recommendations("user002", num_recommendations=3)
    
    # Get system statistics
    get_stats()
    
    print("\n" + "=" * 60)
    print(" ✅ TEST SUITE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nAPI Documentation: {BASE_URL}/docs")
    print(f"Alternative Docs: {BASE_URL}/redoc")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Make sure the server is running.")
        print("   Start the server with: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
