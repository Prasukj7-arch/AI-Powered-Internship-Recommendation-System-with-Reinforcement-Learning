"""
Integrated Recommendation System with Automatic Fallback
Combines OpenRouter API with ChromaDB + Ollama backup system
"""

from rag_internship_recommender import InternshipRecommender
from simple_backup_recommender import SimpleBackupRecommender
from config import get_api_key, is_api_configured
import warnings
warnings.filterwarnings('ignore')

class IntegratedRecommender:
    def __init__(self, csv_file_path: str):
        """
        Initialize the Integrated Recommender with automatic fallback
        
        Args:
            csv_file_path: Path to the CSV file containing internship data
        """
        self.csv_file_path = csv_file_path
        self.primary_recommender = None
        self.backup_recommender = None
        self.setup_recommenders()
        
    def setup_recommenders(self):
        """Setup both primary and backup recommenders"""
        print("🔧 Setting up Integrated Recommendation System...")
        
        # Setup primary recommender (OpenRouter API)
        try:
            if is_api_configured():
                api_key = get_api_key()
                self.primary_recommender = InternshipRecommender(self.csv_file_path, api_key)
                print("✅ Primary recommender (OpenRouter API) ready")
            else:
                print("⚠️ Primary recommender not available - API key not configured")
        except Exception as e:
            print(f"⚠️ Primary recommender setup failed: {e}")
        
        # Setup backup recommender (TF-IDF only)
        try:
            self.backup_recommender = SimpleBackupRecommender(self.csv_file_path)
            print("✅ Backup recommender (TF-IDF) ready")
        except Exception as e:
            print(f"⚠️ Backup recommender setup failed: {e}")
            self.backup_recommender = None
        
        if not self.primary_recommender and not self.backup_recommender:
            raise Exception("❌ No recommendation system available!")
    
    def recommend_internships(self, resume_data: dict, num_recommendations: int = 5) -> dict:
        """
        Get internship recommendations with automatic fallback
        
        Args:
            resume_data: Dictionary containing candidate information
            num_recommendations: Number of recommendations to return
        
        Returns:
            Dictionary containing recommendations and metadata
        """
        print("🔍 Starting integrated recommendation process...")
        
        # Try primary recommender first
        if self.primary_recommender:
            try:
                print("🔄 Attempting primary recommendation (OpenRouter API)...")
                result = self.primary_recommender.recommend_internships(resume_data, num_recommendations)
                result['method'] = 'primary'
                result['fallback_used'] = False
                print("✅ Primary recommendation successful")
                return result
            except Exception as e:
                print(f"⚠️ Primary recommendation failed: {e}")
                print("🔄 Falling back to backup system...")
        
        # Fallback to backup recommender
        if self.backup_recommender:
            try:
                print("🔄 Using backup recommendation (TF-IDF)...")
                recommendations = self.backup_recommender.get_recommendations(resume_data, num_recommendations)
                
                result = {
                    "candidate_profile": self.backup_recommender.create_candidate_profile_text(resume_data),
                    "total_internships_analyzed": len(self.backup_recommender.df),
                    "recommendations": recommendations,
                    "method": 'backup',
                    "fallback_used": True,
                    "timestamp": pd.Timestamp.now().isoformat()
                }
                print("✅ Backup recommendation successful")
                return result
            except Exception as e:
                print(f"❌ Backup recommendation failed: {e}")
        
        # If both fail, return minimal fallback
        print("⚠️ All recommendation systems failed, using emergency fallback")
        try:
            # Emergency fallback: return first few internships with basic info
            emergency_recommendations = []
            for i in range(min(3, num_recommendations)):
                emergency_recommendations.append({
                    "rank": i + 1,
                    "company": f"Company {i+1}",
                    "title": f"Internship {i+1}",
                    "match_score": 70,
                    "reasoning": "Basic recommendation due to system limitations",
                    "skills_to_highlight": []
                })
            
            return {
                "candidate_profile": str(resume_data),
                "total_internships_analyzed": 0,
                "recommendations": emergency_recommendations,
                "method": 'emergency_fallback',
                "fallback_used": True,
                "timestamp": pd.Timestamp.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Even emergency fallback failed: {e}")
            raise Exception("❌ All recommendation systems failed completely!")
    
    def display_recommendations(self, result: dict):
        """Display recommendations with method indicator"""
        print("\n" + "="*80)
        print("🎯 INTERNSHIP RECOMMENDATIONS")
        if result['method'] == 'primary':
            print("🤖 Generated by: OpenRouter API (Mistral-7B)")
        else:
            print("🔄 Generated by: TF-IDF (Backup System)")
        print("="*80)
        
        print(f"\n📊 Analysis Summary:")
        print(f"   • Total internships analyzed: {result['total_internships_analyzed']}")
        print(f"   • Recommendations provided: {len(result['recommendations'])}")
        print(f"   • Method used: {result['method']}")
        print(f"   • Fallback used: {result['fallback_used']}")
        
        print(f"\n👤 Candidate Profile:")
        print(result['candidate_profile'])
        
        print(f"\n🏆 TOP RECOMMENDATIONS:")
        print("-" * 80)
        
        for rec in result['recommendations']:
            print(f"\n#{rec['rank']} - {rec['company']} - {rec['title']}")
            print(f"   Match Score: {rec['match_score']}%")
            print(f"   Reasoning: {rec['reasoning']}")
            
            if rec['skills_to_highlight']:
                print(f"   Skills to Highlight: {', '.join(rec['skills_to_highlight'])}")
            
            print("-" * 40)
    
    def get_system_status(self) -> dict:
        """Get status of both recommendation systems"""
        status = {
            "primary_available": self.primary_recommender is not None,
            "backup_available": self.backup_recommender is not None,
            "api_configured": is_api_configured()
        }
        
        if self.backup_recommender:
            try:
                # Check if it's the simple backup (TF-IDF) or advanced backup (ChromaDB)
                if hasattr(self.backup_recommender, 'collection'):
                    status["backup_chromadb_ready"] = self.backup_recommender.collection is not None
                    status["backup_chunks_count"] = self.backup_recommender.collection.count() if self.backup_recommender.collection else 0
                else:
                    # Simple backup (TF-IDF) - always ready
                    status["backup_chromadb_ready"] = True
                    status["backup_chunks_count"] = len(self.backup_recommender.df) if hasattr(self.backup_recommender, 'df') else 0
            except:
                status["backup_chromadb_ready"] = False
                status["backup_chunks_count"] = 0
        else:
            status["backup_chromadb_ready"] = False
            status["backup_chunks_count"] = 0
            
        return status

def main():
    """Main function to test the integrated system"""
    print("🚀 Testing Integrated Recommendation System")
    print("="*60)
    
    try:
        # Initialize integrated recommender
        recommender = IntegratedRecommender("internships_all_streams_edited.csv")
        
        # Check system status
        status = recommender.get_system_status()
        print(f"\n📊 System Status:")
        print(f"   • Primary (OpenRouter API): {'✅' if status['primary_available'] else '❌'}")
        print(f"   • Backup (ChromaDB + Ollama): {'✅' if status['backup_available'] else '❌'}")
        print(f"   • API Configured: {'✅' if status['api_configured'] else '❌'}")
        if status['backup_available']:
            print(f"   • ChromaDB Ready: {'✅' if status['backup_chromadb_ready'] else '❌'}")
            print(f"   • ChromaDB Chunks: {status['backup_chunks_count']}")
        
        # Sample candidate data
        sample_resume = {
            "name": "Priya Sharma",
            "education": "B.Tech Computer Science Engineering, 2024 - 8.5 CGPA",
            "skills": "Python, Machine Learning, TensorFlow, Data Analysis, SQL, Tableau, Web Development, JavaScript, React, Communication, Teamwork",
            "experience": "2 months data science internship at TechCorp, 1 year coding experience with personal projects, 6 months freelance web development",
            "interests": "Artificial Intelligence, Machine Learning, Data Science, Software Development, Fintech, Healthcare Technology",
            "location_preference": "Bangalore, Pune, Delhi, Mumbai, Hyderabad",
            "career_goals": "Become a senior data scientist in a leading tech company, work on AI/ML products that impact millions of users",
            "certifications": "Google Data Analytics Certificate, AWS Cloud Practitioner",
            "projects": "Built ML model for stock prediction, Developed e-commerce website, Created data visualization dashboard"
        }
        
        # Get recommendations
        result = recommender.recommend_internships(sample_resume, num_recommendations=5)
        recommender.display_recommendations(result)
        
    except Exception as e:
        print(f"❌ Error during integrated recommendation: {e}")

if __name__ == "__main__":
    main()
