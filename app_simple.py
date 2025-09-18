"""
Simplified Flask Backend for PM Internship Recommendation System
Works with minimal dependencies for Python 3.13
"""

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
import os

app = Flask(__name__, static_folder='twin-digital-copy-main/twin-digital-copy-main/dist')
CORS(app)

# Load CSV data
try:
    df = pd.read_csv("internships_all_streams_edited.csv")
    print(f"✅ Loaded {len(df)} internships from CSV")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    df = pd.DataFrame()

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
    """Check system status"""
    return jsonify({
        'primary_available': False,
        'backup_available': True,
        'api_configured': False,
        'message': 'Running in simplified mode'
    })

@app.route('/api/internships')
def get_internships():
    """Get all internships with optional filtering"""
    try:
        if df.empty:
            return jsonify({'internships': [], 'total': 0, 'filters': {}})
        
        # Get query parameters for filtering
        state = request.args.get('state')
        district = request.args.get('district')
        sector = request.args.get('sector')
        field = request.args.get('field')
        search = request.args.get('search', '')
        
        # Apply filters
        filtered_df = df.copy()
        if state:
            filtered_df = filtered_df[filtered_df['Internship State'].str.contains(state, case=False, na=False)]
        if district:
            filtered_df = filtered_df[filtered_df['Internship District'].str.contains(district, case=False, na=False)]
        if sector:
            filtered_df = filtered_df[filtered_df['Area/Field'].str.contains(sector, case=False, na=False)]
        if field:
            filtered_df = filtered_df[filtered_df['Tag'].str.contains(field, case=False, na=False)]
        if search:
            search_cols = ['Company', 'Internship Title', 'Area/Field', 'Tag']
            mask = filtered_df[search_cols].apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            filtered_df = filtered_df[mask]
        
        # Convert to list of dictionaries
        internships = []
        for idx, row in filtered_df.iterrows():
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
    """API endpoint for recommendations (simplified)"""
    try:
        # Get candidate data from request
        candidate_data = request.json
        
        # Validate required fields
        required_fields = ['name', 'education', 'skills']
        for field in required_fields:
            if not candidate_data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Simple keyword-based matching
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
            "method": 'backup',
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
    print("🚀 Starting PM Internship Recommendation System (Simplified)")
    print("=" * 60)
    print("📱 Frontend: http://localhost:5000")
    print("🔧 API: http://localhost:5000/api/")
    print("💡 Running in simplified mode (no AI features)")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
