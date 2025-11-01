#!/usr/bin/env python3
"""
Interactive demo script to showcase the RL learning process.
This script shows how the system learns and improves recommendations over time.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_server():
    """Check if server is running."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def setup_data():
    """Setup initial data."""
    print_header("Setting Up Data")
    
    # Articles from different categories
    articles = [
        {
            "id": "tech1", "title": "AI in 2024", "content": "AI trends...",
            "category": "technology", "tags": ["AI", "tech"], "author": "Tech Writer",
            "created_at": datetime.now().isoformat(), "views": 0, "likes": 0
        },
        {
            "id": "tech2", "title": "Python Tips", "content": "Python best practices...",
            "category": "technology", "tags": ["Python", "coding"], "author": "Dev Expert",
            "created_at": datetime.now().isoformat(), "views": 0, "likes": 0
        },
        {
            "id": "health1", "title": "Yoga Benefits", "content": "Health benefits...",
            "category": "health", "tags": ["yoga", "wellness"], "author": "Health Guru",
            "created_at": datetime.now().isoformat(), "views": 0, "likes": 0
        },
        {
            "id": "health2", "title": "Nutrition Guide", "content": "Healthy eating...",
            "category": "health", "tags": ["nutrition", "diet"], "author": "Nutritionist",
            "created_at": datetime.now().isoformat(), "views": 0, "likes": 0
        },
        {
            "id": "travel1", "title": "Travel Asia", "content": "Best destinations...",
            "category": "travel", "tags": ["travel", "Asia"], "author": "Traveler",
            "created_at": datetime.now().isoformat(), "views": 0, "likes": 0
        },
        {
            "id": "finance1", "title": "Invest Smart", "content": "Investment tips...",
            "category": "finance", "tags": ["finance", "investing"], "author": "Finance Pro",
            "created_at": datetime.now().isoformat(), "views": 0, "likes": 0
        },
    ]
    
    for article in articles:
        requests.post(f"{BASE_URL}/api/articles", json=article)
        print(f"  ✓ Added: {article['title']} [{article['category']}]")
    
    # Create users
    users = [
        {"id": "alice", "name": "Alice", "preferences": [], "history": []},
        {"id": "bob", "name": "Bob", "preferences": [], "history": []},
    ]
    
    for user in users:
        requests.post(f"{BASE_URL}/api/users", json=user)
        print(f"  ✓ Created user: {user['name']}")


def show_recommendations(user_id, iteration):
    """Show recommendations for a user."""
    payload = {"user_id": user_id, "num_recommendations": 3}
    response = requests.post(f"{BASE_URL}/api/recommendations", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n  Iteration {iteration} - Recommendations for {user_id}:")
        for i, (article, score) in enumerate(zip(data['articles'], data['scores']), 1):
            print(f"    {i}. {article['title']:30} [Score: {score:6.3f}] ({article['category']})")
        return data['articles']
    return []


def submit_feedback(user_id, article_id, interaction, duration=None):
    """Submit user feedback."""
    payload = {
        "user_id": user_id,
        "article_id": article_id,
        "interaction_type": interaction
    }
    if duration:
        payload["duration"] = duration
    
    requests.post(f"{BASE_URL}/api/feedback", json=payload)


def show_stats():
    """Show system statistics."""
    response = requests.get(f"{BASE_URL}/api/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"\n  📊 System Stats:")
        print(f"     - Q-table size: {stats['q_table_size']}")
        print(f"     - Total interactions: {stats['num_interactions']}")
        print(f"     - Exploration rate (ε): {stats['epsilon']}")


def run_demo():
    """Run the interactive demo."""
    print_header("🤖 RL-Based Article Recommendation System Demo")
    print("\nThis demo shows how the system learns from user interactions.")
    print("Watch how recommendations change as the RL agent learns!\n")
    
    if not check_server():
        print("❌ Error: Server not running!")
        print("   Start it with: python run.py")
        return
    
    print("✅ Server is running")
    time.sleep(1)
    
    # Setup
    setup_data()
    time.sleep(1)
    
    # Initial recommendations (random/exploration phase)
    print_header("📋 Phase 1: Initial Recommendations (Before Learning)")
    print("\nThe agent doesn't know user preferences yet, so recommendations")
    print("are based on exploration (random selection).")
    
    alice_recs = show_recommendations("alice", 1)
    bob_recs = show_recommendations("bob", 1)
    show_stats()
    
    time.sleep(2)
    
    # Simulate Alice liking tech articles
    print_header("👤 Phase 2: Alice's Interactions")
    print("\nAlice interacts with articles - she LIKES tech, SKIPS others:")
    
    print("\n  Alice's actions:")
    if alice_recs:
        for i, article in enumerate(alice_recs[:2]):
            category = article['category']
            if category == 'technology':
                print(f"    ✓ LIKED: {article['title']}")
                submit_feedback("alice", article['id'], "like")
            else:
                print(f"    ✗ SKIPPED: {article['title']}")
                submit_feedback("alice", article['id'], "skip")
            time.sleep(0.5)
    
    show_stats()
    time.sleep(2)
    
    # Simulate Bob liking travel and finance
    print_header("👤 Phase 3: Bob's Interactions")
    print("\nBob interacts with articles - he LIKES travel/finance, SKIPS tech:")
    
    print("\n  Bob's actions:")
    if bob_recs:
        for i, article in enumerate(bob_recs[:2]):
            category = article['category']
            if category in ['travel', 'finance']:
                print(f"    ✓ LIKED: {article['title']}")
                submit_feedback("bob", article['id'], "like")
            else:
                print(f"    ✗ SKIPPED: {article['title']}")
                submit_feedback("bob", article['id'], "skip")
            time.sleep(0.5)
    
    show_stats()
    time.sleep(2)
    
    # Show improved recommendations
    print_header("🎯 Phase 4: Improved Recommendations (After Learning)")
    print("\nNow the agent has learned user preferences!")
    print("Notice how recommendations are more personalized:")
    
    show_recommendations("alice", 2)
    show_recommendations("bob", 2)
    show_stats()
    
    # More interactions to strengthen learning
    time.sleep(2)
    print_header("🔄 Phase 5: More Learning")
    print("\nMore interactions to strengthen the learning...")
    
    # Alice likes more tech
    print("\n  Alice views more tech articles:")
    submit_feedback("alice", "tech2", "view", duration=150.0)
    print("    ✓ VIEWED: Python Tips (150 seconds)")
    
    # Bob likes travel
    print("\n  Bob shares a travel article:")
    submit_feedback("bob", "travel1", "share")
    print("    ✓ SHARED: Travel Asia")
    
    show_stats()
    time.sleep(2)
    
    # Final recommendations
    print_header("🌟 Phase 6: Final Recommendations (Well-Trained)")
    print("\nWith more data, the system provides better recommendations:")
    
    show_recommendations("alice", 3)
    show_recommendations("bob", 3)
    show_stats()
    
    # Summary
    print_header("✅ Demo Complete!")
    print("\n📚 Key Takeaways:")
    print("  1. The system starts with random/exploratory recommendations")
    print("  2. As users interact (like/view/skip), the RL agent learns")
    print("  3. Q-values are updated based on rewards from interactions")
    print("  4. Recommendations become personalized over time")
    print("  5. The more interactions, the better the recommendations")
    print("\n💡 The system uses Q-Learning with epsilon-greedy exploration")
    print("   to balance between trying new content and recommending")
    print("   content that users have liked in the past.")
    print("\n🔗 API Documentation: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
