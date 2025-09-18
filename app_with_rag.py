"""
Enhanced Flask Backend with RAG Integration for PM Internship Recommendation System
Integrates the existing RAG recommendation system with the React frontend
"""

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Import your existing recommendation systems
try:
    from integrated_recommender import IntegratedRecommender
    from simple_backup_recommender import SimpleBackupRecommender
    from config import get_api_key, is_api_configured
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ RAG modules not available: {e}")
    RAG_AVAILABLE = False

app = Flask(__name__, static_folder='twin-digital-copy-main/twin-digital-copy-main/dist')
CORS(app)

# Initialize the recommender (will be loaded when first request comes)
recommender = None
backup_recommender = None

def get_recommender():
    """Lazy initialization of integrated recommender"""
    global recommender, backup_recommender
    
    if not RAG_AVAILABLE:
        return None, None
    
    if recommender is None:
        try:
            recommender = IntegratedRecommender("internships_all_streams_edited.csv")
            print("✅ RAG recommender initialized successfully")
        except Exception as e:
            print(f"⚠️ RAG recommender failed to initialize: {e}")
            recommender = None
    
    if backup_recommender is None:
        try:
            backup_recommender = SimpleBackupRecommender("internships_all_streams_edited.csv")
            print("✅ Backup recommender initialized successfully")
        except Exception as e:
            print(f"⚠️ Backup recommender failed to initialize: {e}")
            backup_recommender = None
    
    return recommender, backup_recommender

@app.route('/')
def serve_react_app():
    """Serve the React app"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files from React build"""
    return send_from_directory(app.static_folder, path)

# API Routes
@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'PM Internship Recommender API is running'})

@app.route('/api/system-status')
def system_status():
    """Check system status including RAG availability"""
    try:
        rag_rec, backup_rec = get_recommender()
        
        status = {
            'primary_available': rag_rec is not None and rag_rec.primary_recommender is not None,
            'backup_available': backup_rec is not None,
            'api_configured': is_api_configured() if RAG_AVAILABLE else False,
            'rag_available': RAG_AVAILABLE,
            'message': 'RAG system available' if RAG_AVAILABLE else 'RAG system not available'
        }
        
        if backup_rec:
            try:
                status["backup_chromadb_ready"] = hasattr(backup_rec, 'collection') and backup_rec.collection is not None
                status["backup_chunks_count"] = len(backup_rec.df) if hasattr(backup_rec, 'df') else 0
            except:
                status["backup_chromadb_ready"] = False
                status["backup_chunks_count"] = 0
        
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'primary_available': False,
            'backup_available': False,
            'api_configured': False,
            'rag_available': RAG_AVAILABLE,
            'error': str(e)
        })

@app.route('/api/internships')
def get_internships():
    """Get all internships with optional filtering"""
    try:
        # Load CSV data
        df = pd.read_csv("internships_all_streams_edited.csv")
        
        # Get query parameters for filtering
        state = request.args.get('state')
        district = request.args.get('district')
        sector = request.args.get('sector')
        field = request.args.get('field')
        search = request.args.get('search', '')
        
        # Apply filters
        if state:
            df = df[df['Internship State'].str.contains(state, case=False, na=False)]
        if district:
            df = df[df['Internship District'].str.contains(district, case=False, na=False)]
        if sector:
            df = df[df['Area/Field'].str.contains(sector, case=False, na=False)]
        if field:
            df = df[df['Tag'].str.contains(field, case=False, na=False)]
        if search:
            search_cols = ['Company', 'Internship Title', 'Area/Field', 'Tag']
            mask = df[search_cols].apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            df = df[mask]
        
        # Convert to list of dictionaries
        internships = []
        for idx, row in df.iterrows():
            internship = {
                'id': idx,
                'company': row.get('Company', ''),
                'internshipId': row.get('Internship ID', ''),
                'title': row.get('Internship Title', ''),
                'areaField': row.get('Area/Field', ''),
                'state': row.get('Internship State', ''),
                'district': row.get('Internship District', ''),
                'benefits': row.get('Benefits', ''),
                'candidatesApplied': row.get('Candidates Applied', 0),
                'tag': row.get('Tag', ''),
                'recommendation': None
            }
            internships.append(internship)
        
        return jsonify({
            'internships': internships,
            'total': len(internships),
            'filters': {
                'state': state,
                'district': district,
                'sector': sector,
                'field': field,
                'search': search
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API endpoint for recommendations using RAG system"""
    try:
        # Get candidate data from request
        candidate_data = request.json
        
        # Validate required fields
        required_fields = ['name', 'education', 'skills']
        for field in required_fields:
            if not candidate_data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get recommenders
        rag_rec, backup_rec = get_recommender()
        
        # Try RAG recommender first
        if rag_rec:
            try:
                print("🔄 Using RAG recommendation system...")
                result = rag_rec.recommend_internships(candidate_data, num_recommendations=5)
                print("✅ RAG recommendations generated successfully")
                return jsonify(result)
            except Exception as e:
                print(f"⚠️ RAG recommendation failed: {e}")
                print("🔄 Falling back to backup system...")
        
        # Fallback to backup recommender
        if backup_rec:
            try:
                print("🔄 Using backup recommendation system...")
                recommendations = backup_rec.get_recommendations(candidate_data, num_recommendations=5)
                
                result = {
                    "candidate_profile": backup_rec.create_candidate_profile_text(candidate_data),
                    "total_internships_analyzed": len(backup_rec.df),
                    "recommendations": recommendations,
                    "method": 'backup',
                    "fallback_used": True,
                    "timestamp": pd.Timestamp.now().isoformat()
                }
                print("✅ Backup recommendations generated successfully")
                return jsonify(result)
            except Exception as e:
                print(f"❌ Backup recommendation failed: {e}")
        
        # Final fallback - simple keyword matching
        print("🔄 Using simple keyword matching...")
        return get_simple_recommendations(candidate_data)
        
    except Exception as e:
        print(f"❌ Recommendation error: {e}")
        return jsonify({'error': str(e)}), 500

def get_simple_recommendations(candidate_data):
    """Simple keyword-based recommendations as final fallback"""
    try:
        df = pd.read_csv("internships_all_streams_edited.csv")
        skills = candidate_data.get('skills', '').lower()
        recommendations = []
        
        # Find internships that match skills
        for idx, row in df.iterrows():
            if len(recommendations) >= 5:
                break
                
            # Simple matching based on area/field and skills
            area_field = str(row.get('Area/Field', '')).lower()
            company = str(row.get('Company', '')).lower()
            
            # Calculate a simple match score
            match_score = 0
            if any(skill in area_field for skill in ['tech', 'engineering', 'software', 'data', 'ai', 'ml']):
                match_score += 30
            if any(skill in skills for skill in ['python', 'java', 'javascript', 'react', 'node']):
                match_score += 40
            if any(skill in skills for skill in ['data', 'analysis', 'machine learning', 'ai']):
                match_score += 30
            
            if match_score > 0:
                recommendations.append({
                    'rank': len(recommendations) + 1,
                    'company': row.get('Company', ''),
                    'title': row.get('Internship Title', ''),
                    'match_score': min(match_score, 95),
                    'reasoning': f"Matches your skills in {candidate_data.get('skills', '')}",
                    'skills_to_highlight': [skill for skill in skills.split(',') if skill.strip()]
                })
        
        result = {
            "candidate_profile": f"Name: {candidate_data.get('name')}, Education: {candidate_data.get('education')}, Skills: {candidate_data.get('skills')}",
            "total_internships_analyzed": len(df),
            "recommendations": recommendations,
            "method": 'simple',
            "fallback_used": True,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/apply', methods=['POST'])
def apply_internship():
    """Apply for an internship"""
    try:
        data = request.json
        internship_id = data.get('internship_id')
        user_id = data.get('user_id')
        
        if not internship_id or not user_id:
            return jsonify({'error': 'Missing internship_id or user_id'}), 400
        
        return jsonify({
            'success': True,
            'message': f'Application submitted for internship {internship_id}',
            'application_id': f'APP-{internship_id}-{user_id}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/profile', methods=['GET', 'POST'])
def user_profile():
    """Get or update user profile"""
    if request.method == 'GET':
        return jsonify({
            'id': 51423,
            'name': 'PORNADULLA USHA',
            'age': 19,
            'education': 'B.Tech in Mechatronics',
            'location': 'Tirupati, ANDHRA PRADESH',
            'profile_completion': 100,
            'skills': ['Python', 'Machine Learning', 'Data Analysis'],
            'interests': ['AI/ML', 'Data Science', 'Software Development'],
            'experience': '2 months data science internship'
        })
    
    elif request.method == 'POST':
        data = request.json
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'profile': data
        })

if __name__ == '__main__':
    print("🚀 Starting PM Internship Recommendation System with RAG")
    print("=" * 60)
    print("📱 Frontend: http://localhost:5000")
    print("🔧 API: http://localhost:5000/api/")
    print("🤖 RAG System: Available" if RAG_AVAILABLE else "⚠️ RAG System: Not Available")
    print("=" * 60)
    
    # Test RAG system initialization
    if RAG_AVAILABLE:
        try:
            rag_rec, backup_rec = get_recommender()
            if rag_rec:
                print("✅ RAG recommender ready")
            if backup_rec:
                print("✅ Backup recommender ready")
        except Exception as e:
            print(f"⚠️ RAG initialization warning: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
