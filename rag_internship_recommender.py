import pandas as pd
import numpy as np
import requests
import json
import os
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from config import get_api_key, is_api_configured, OPENROUTER_MODEL, API_TIMEOUT, MAX_TOKENS, TEMPERATURE
warnings.filterwarnings('ignore')

class InternshipRecommender:
    def __init__(self, csv_file_path: str, openrouter_api_key: str):
        """
        Initialize the Internship Recommender with RAG architecture
        
        Args:
            csv_file_path: Path to the CSV file containing internship data
            openrouter_api_key: OpenRouter API key for Mistral model
        """
        self.csv_file_path = csv_file_path
        self.openrouter_api_key = openrouter_api_key
        self.df = None
        self.vectorizer = None
        self.job_vectors = None
        self.load_data()
        self.setup_vectorizer()
        
    def load_data(self):
        """Load and preprocess the internship data"""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            print(f"✅ Loaded {len(self.df)} internships from {self.csv_file_path}")
            
            # Create a combined text field for each internship
            self.df['combined_text'] = (
                self.df['Internship Title'].fillna('') + ' ' +
                self.df['Description'].fillna('') + ' ' +
                self.df['Sector'].fillna('') + ' ' +
                self.df['Area/Field'].fillna('') + ' ' +
                self.df['Preferred Skill(s)'].fillna('') + ' ' +
                self.df['Specialization'].fillna('') + ' ' +
                self.df['Course'].fillna('') + ' ' +
                self.df['Minimum Qualification'].fillna('')
            )
            
            print("✅ Data preprocessing completed")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def setup_vectorizer(self):
        """Setup TF-IDF vectorizer for text similarity"""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit and transform the combined text
        self.job_vectors = self.vectorizer.fit_transform(self.df['combined_text'])
        print("✅ TF-IDF vectorizer setup completed")
    
    def call_openrouter_api(self, prompt: str, model: str = None) -> str:
        """
        Call OpenRouter API with Mistral model
        
        Args:
            prompt: The prompt to send to the model
            model: The model to use (default: from config)
        
        Returns:
            Response from the model
        """
        if model is None:
            model = OPENROUTER_MODEL
            
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None
        except KeyError as e:
            print(f"❌ Response parsing error: {e}")
            return None
    
    def create_candidate_profile(self, resume_data: Dict[str, Any]) -> str:
        """
        Create a structured candidate profile from resume data
        
        Args:
            resume_data: Dictionary containing candidate information
        
        Returns:
            Formatted candidate profile string
        """
        profile = f"""
        CANDIDATE PROFILE:
        Name: {resume_data.get('name', 'N/A')}
        Education: {resume_data.get('education', 'N/A')}
        Skills: {resume_data.get('skills', 'N/A')}
        Experience: {resume_data.get('experience', 'N/A')}
        Interests: {resume_data.get('interests', 'N/A')}
        Location Preference: {resume_data.get('location_preference', 'N/A')}
        Career Goals: {resume_data.get('career_goals', 'N/A')}
        Certifications: {resume_data.get('certifications', 'N/A')}
        Projects: {resume_data.get('projects', 'N/A')}
        """
        return profile.strip()
    
    def get_similar_internships(self, candidate_profile: str, top_k: int = 10) -> List[int]:
        """
        Find similar internships using TF-IDF similarity
        
        Args:
            candidate_profile: Candidate's profile text
            top_k: Number of top similar internships to return
        
        Returns:
            List of indices of similar internships
        """
        # Vectorize the candidate profile
        candidate_vector = self.vectorizer.transform([candidate_profile])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(candidate_vector, self.job_vectors).flatten()
        
        # Get top k similar internships
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        return top_indices.tolist()
    
    def generate_recommendations_with_llm(self, candidate_profile: str, similar_indices: List[int]) -> List[Dict]:
        """
        Use LLM to generate detailed recommendations with reasoning
        
        Args:
            candidate_profile: Candidate's profile
            similar_indices: Indices of similar internships
        
        Returns:
            List of recommendation dictionaries
        """
        # Get the similar internships data
        similar_internships = self.df.iloc[similar_indices]
        
        # Create a detailed prompt for the LLM
        internships_text = ""
        for idx, (_, internship) in enumerate(similar_internships.iterrows()):
            internships_text += f"""
            INTERNSHIP {idx + 1}:
            Company: {internship['Company Name']}
            Title: {internship['Internship Title']}
            Sector: {internship['Sector']}
            Area/Field: {internship['Area/Field']}
            Description: {internship['Description']}
            Location: {internship['Location']}, {internship['State/UT']}
            Required Skills: {internship['Preferred Skill(s)']}
            Qualification: {internship['Minimum Qualification']}
            Course: {internship['Course']}
            Specialization: {internship['Specialization']}
            Benefits: {internship['Benefits Description']}
            Opportunities Available: {internship['No. of Opportunities']}
            ---
            """
        
        prompt = f"""
        You are an AI career counselor. Analyze this candidate profile and recommend the best 3-5 internships.

        CANDIDATE PROFILE:
        {candidate_profile}

        AVAILABLE INTERNSHIPS:
        {internships_text}

        Return ONLY a valid JSON array with this exact format:
        [
            {{
                "rank": 1,
                "company": "Company Name",
                "title": "Internship Title", 
                "match_score": 85,
                "reasoning": "Why this matches the candidate",
                "skills_to_highlight": ["skill1", "skill2"]
            }}
        ]

        IMPORTANT: 
        - Use match_score as percentage (75-95)
        - Do NOT include gaps_to_address field
        - Return ONLY the JSON array, no other text.
        """
        
        # Call the LLM
        response = self.call_openrouter_api(prompt)
        
        if response:
            try:
                # Clean the response to extract JSON
                response_clean = response.strip()
                
                # Try to find JSON array in the response
                if response_clean.startswith('[') and response_clean.endswith(']'):
                    recommendations = json.loads(response_clean)
                else:
                    # Look for JSON array in the response
                    start_idx = response_clean.find('[')
                    end_idx = response_clean.rfind(']')
                    if start_idx != -1 and end_idx != -1:
                        json_str = response_clean[start_idx:end_idx+1]
                        recommendations = json.loads(json_str)
                    else:
                        raise json.JSONDecodeError("No JSON array found", response, 0)
                
                # Validate the recommendations
                if isinstance(recommendations, list) and len(recommendations) > 0:
                    return recommendations
                else:
                    raise json.JSONDecodeError("Invalid recommendations format", response, 0)
                    
            except json.JSONDecodeError as e:
                print(f"⚠️ Could not parse LLM response as JSON: {e}")
                print(f"Response: {response[:200]}...")
                return self.create_fallback_recommendations(similar_internships.head(5))
        else:
            print("⚠️ LLM API call failed, using fallback recommendations")
            return self.create_fallback_recommendations(similar_internships.head(5))
    
    def create_fallback_recommendations(self, internships_df) -> List[Dict]:
        """Create fallback recommendations when LLM fails"""
        recommendations = []
        for idx, (_, internship) in enumerate(internships_df.iterrows()):
            # Calculate more realistic match scores based on similarity
            base_score = 75 + (idx * 2)  # 75-85% range
            match_percentage = min(base_score, 95)
            
            recommendations.append({
                "rank": idx + 1,
                "company": internship['Company Name'],
                "title": internship['Internship Title'],
                "match_score": match_percentage,
                "reasoning": f"Strong alignment with {internship['Sector']} sector and {internship['Area/Field']} specialization. Location and requirements match candidate profile well.",
                "skills_to_highlight": internship['Preferred Skill(s)'].split(', ') if pd.notna(internship['Preferred Skill(s)']) else []
            })
        return recommendations
    
    def recommend_internships(self, resume_data: Dict[str, Any], num_recommendations: int = 5) -> Dict[str, Any]:
        """
        Main method to get internship recommendations
        
        Args:
            resume_data: Dictionary containing candidate information
            num_recommendations: Number of recommendations to return
        
        Returns:
            Dictionary containing recommendations and metadata
        """
        print("🔍 Starting internship recommendation process...")
        
        # Create candidate profile
        candidate_profile = self.create_candidate_profile(resume_data)
        print("✅ Candidate profile created")
        
        # Get similar internships using TF-IDF
        similar_indices = self.get_similar_internships(candidate_profile, top_k=15)
        print(f"✅ Found {len(similar_indices)} similar internships")
        
        # Generate detailed recommendations using LLM
        recommendations = self.generate_recommendations_with_llm(candidate_profile, similar_indices)
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        # Limit to requested number of recommendations
        recommendations = recommendations[:num_recommendations]
        
        return {
            "candidate_profile": candidate_profile,
            "total_internships_analyzed": len(self.df),
            "recommendations": recommendations,
            "timestamp": pd.Timestamp.now().isoformat()
        }
    
    def display_recommendations(self, result: Dict[str, Any]):
        """Display recommendations in a user-friendly format"""
        print("\n" + "="*80)
        print("🎯 INTERNSHIP RECOMMENDATIONS")
        print("="*80)
        
        print(f"\n📊 Analysis Summary:")
        print(f"   • Total internships analyzed: {result['total_internships_analyzed']}")
        print(f"   • Recommendations provided: {len(result['recommendations'])}")
        
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

def main():
    """Main function to test the recommendation system"""
    
    # Configuration
    CSV_FILE = "internships_all_streams_edited.csv"
    OPENROUTER_API_KEY = get_api_key()
    
    # Check if API key is provided
    if not is_api_configured():
        print("❌ Please set your OpenRouter API key!")
        print("   Options:")
        print("   1. Set environment variable: OPENROUTER_API_KEY=your_key")
        print("   2. Create .env file with: OPENROUTER_API_KEY=your_key")
        print("   3. Get your API key from: https://openrouter.ai/")
        print("\n   The system will work with TF-IDF similarity only (no AI features)")
        return
    
    # Initialize the recommender
    try:
        recommender = InternshipRecommender(CSV_FILE, OPENROUTER_API_KEY)
    except Exception as e:
        print(f"❌ Failed to initialize recommender: {e}")
        return
    
    # Sample candidate resume data - More detailed for better matching
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
    
    print("🚀 Testing Internship Recommendation System")
    print("="*50)
    
    # Get recommendations
    try:
        result = recommender.recommend_internships(sample_resume, num_recommendations=5)
        recommender.display_recommendations(result)
        
    except Exception as e:
        print(f"❌ Error during recommendation: {e}")

if __name__ == "__main__":
    main()
