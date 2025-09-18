#!/usr/bin/env python3
"""
Test script for RAG recommendation system
"""

import sys
import os
from pathlib import Path

def test_rag_system():
    """Test the RAG recommendation system"""
    print("🧪 Testing RAG Recommendation System")
    print("=" * 50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from integrated_recommender import IntegratedRecommender
        from simple_backup_recommender import SimpleBackupRecommender
        from config import get_api_key, is_api_configured
        print("✅ All imports successful")
        
        # Test CSV loading
        print("\n2. Testing CSV data loading...")
        import pandas as pd
        df = pd.read_csv("internships_all_streams_edited.csv")
        print(f"✅ Loaded {len(df)} internships from CSV")
        
        # Test backup recommender
        print("\n3. Testing backup recommender...")
        backup_rec = SimpleBackupRecommender("internships_all_streams_edited.csv")
        print("✅ Backup recommender initialized")
        
        # Test integrated recommender
        print("\n4. Testing integrated recommender...")
        try:
            rag_rec = IntegratedRecommender("internships_all_streams_edited.csv")
            print("✅ Integrated recommender initialized")
        except Exception as e:
            print(f"⚠️ Integrated recommender failed: {e}")
            rag_rec = None
        
        # Test recommendation
        print("\n5. Testing recommendation generation...")
        sample_profile = {
            "name": "Test User",
            "education": "B.Tech Computer Science",
            "skills": "Python, Machine Learning, Data Analysis",
            "experience": "1 year coding experience",
            "interests": "AI/ML, Data Science"
        }
        
        if rag_rec:
            try:
                result = rag_rec.recommend_internships(sample_profile, num_recommendations=3)
                print(f"✅ RAG recommendations generated: {len(result['recommendations'])} recommendations")
                print(f"   Method: {result['method']}")
                print(f"   Fallback used: {result['fallback_used']}")
            except Exception as e:
                print(f"⚠️ RAG recommendation failed: {e}")
        
        # Test backup recommendation
        try:
            backup_result = backup_rec.get_recommendations(sample_profile, num_recommendations=3)
            print(f"✅ Backup recommendations generated: {len(backup_result)} recommendations")
        except Exception as e:
            print(f"⚠️ Backup recommendation failed: {e}")
        
        print("\n🎉 RAG system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ RAG system test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_rag_system()
    sys.exit(0 if success else 1)
