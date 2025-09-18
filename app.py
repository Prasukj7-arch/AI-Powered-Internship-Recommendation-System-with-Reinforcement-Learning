"""
Integrated Flask Backend for PM Internship Recommendation System
Serves React frontend and provides API endpoints
"""

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from integrated_recommender import IntegratedRecommender
from config import get_api_key, is_api_configured
import json
import os
import pandas as pd

app = Flask(__name__, static_folder='twin-digital-copy-main/twin-digital-copy-main/dist')
CORS(app)

# Initialize the recommender (will be loaded when first request comes)
recommender = None

def get_recommender():
    """Lazy initialization of integrated recommender"""
    global recommender
    if recommender is None:
        recommender = IntegratedRecommender("internships_all_streams_edited.csv")
    return recommender

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
    """Check integrated system status"""
    try:
        rec = get_recommender()
        status = rec.get_system_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'primary_available': False,
            'backup_available': False,
            'api_configured': False,
            'error': str(e)
        })

@app.route('/api/internships')
def get_internships():
    """Get all internships with optional filtering"""
    try:
        rec = get_recommender()
        
        # Get query parameters for filtering
        state = request.args.get('state')
        district = request.args.get('district')
        sector = request.args.get('sector')
        field = request.args.get('field')
        search = request.args.get('search', '')
        
        # Load the CSV data
        df = pd.read_csv("internships_all_streams_edited.csv")
        
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
                'recommendation': None  # Will be set by recommendation API
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
    """API endpoint for recommendations"""
    try:
        # Get candidate data from request
        candidate_data = request.json
        
        # Validate required fields
        required_fields = ['name', 'education', 'skills']
        for field in required_fields:
            if not candidate_data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get recommender
        rec = get_recommender()
        
        # Get recommendations
        result = rec.recommend_internships(candidate_data, num_recommendations=5)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/<int:user_id>')
def get_user_recommendations(user_id):
    """Get recommendations for a specific user"""
    try:
        # This would typically fetch from a database
        # For now, return a placeholder
        return jsonify({
            'user_id': user_id,
            'recommendations': [],
            'message': 'User recommendations endpoint - implement with user data'
        })
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
        
        # Here you would typically save to database
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
        # Return sample profile data
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
        # Update profile
        data = request.json
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'profile': data
        })

if __name__ == '__main__':
    print("🚀 Starting PM Internship Recommendation System")
    print("="*60)
    print("📱 Frontend: http://localhost:5000")
    print("🔧 API: http://localhost:5000/api/")
    print("🔑 Set OPENROUTER_API_KEY environment variable for AI features")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
