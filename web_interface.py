"""
Simple web interface for the RAG Internship Recommendation System
Run this to get a web-based interface for testing
"""

from flask import Flask, render_template_string, request, jsonify
from rag_internship_recommender import InternshipRecommender
from config import get_api_key, is_api_configured
import json
import os

app = Flask(__name__)

# Initialize the recommender (will be loaded when first request comes)
recommender = None

def get_recommender():
    """Lazy initialization of recommender"""
    global recommender
    if recommender is None:
        api_key = get_api_key() or "dummy_key"
        recommender = InternshipRecommender("internships_all_streams_edited.csv", api_key)
    return recommender

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG Internship Recommendation System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        textarea {
            height: 80px;
            resize: vertical;
        }
        .form-row {
            display: flex;
            gap: 20px;
        }
        .form-row .form-group {
            flex: 1;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #2980b9;
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 5px;
        }
        .recommendation {
            background: white;
            margin: 15px 0;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .recommendation h3 {
            color: #2c3e50;
            margin-top: 0;
        }
        .match-score {
            display: inline-block;
            background: #27ae60;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }
        .reasoning {
            margin: 10px 0;
            font-style: italic;
            color: #7f8c8d;
        }
        .skills, .gaps {
            margin: 10px 0;
        }
        .skills strong, .gaps strong {
            color: #e74c3c;
        }
        .loading {
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
        }
        .error {
            background-color: #e74c3c;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .api-key-section {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 RAG Internship Recommendation System</h1>
        
        <div class="api-key-section" id="api-status">
            <strong>🔍 API Status:</strong> 
            <span id="api-status-text">Checking...</span>
            <br><small>If API is not connected, system will work with TF-IDF similarity only.</small>
        </div>
        
        <form id="recommendationForm">
            <div class="form-row">
                <div class="form-group">
                    <label for="name">Full Name *</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="education">Education *</label>
                    <input type="text" id="education" name="education" placeholder="e.g., B.Tech Computer Science, 2024" required>
                </div>
            </div>
            
            <div class="form-group">
                <label for="skills">Skills *</label>
                <textarea id="skills" name="skills" placeholder="e.g., Python, Machine Learning, Data Analysis, Web Development" required></textarea>
            </div>
            
            <div class="form-group">
                <label for="experience">Experience</label>
                <textarea id="experience" name="experience" placeholder="e.g., 2 months internship in data science, 1 year coding experience"></textarea>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="interests">Interests</label>
                    <input type="text" id="interests" name="interests" placeholder="e.g., AI/ML, Data Science, Software Development">
                </div>
                <div class="form-group">
                    <label for="location">Location Preference</label>
                    <input type="text" id="location" name="location" placeholder="e.g., Bangalore, Pune, Delhi">
                </div>
            </div>
            
            <div class="form-group">
                <label for="goals">Career Goals</label>
                <textarea id="goals" name="goals" placeholder="e.g., Become a data scientist in a tech company"></textarea>
            </div>
            
            <button type="submit">🔍 Get Recommendations</button>
        </form>
        
        <div id="results" class="results" style="display: none;">
            <h2>🏆 Recommendations</h2>
            <div id="recommendations"></div>
        </div>
    </div>

    <script>
        // Check API status on page load
        async function checkApiStatus() {
            try {
                const response = await fetch('/api-status');
                const data = await response.json();
                const statusElement = document.getElementById('api-status-text');
                const statusDiv = document.getElementById('api-status');
                
                if (data.configured) {
                    statusElement.textContent = `✅ ${data.message}`;
                    statusDiv.style.backgroundColor = '#d5f4e6';
                    statusDiv.style.borderLeftColor = '#27ae60';
                } else {
                    statusElement.textContent = `❌ ${data.message}`;
                    statusDiv.style.backgroundColor = '#fdf2f2';
                    statusDiv.style.borderLeftColor = '#e74c3c';
                }
            } catch (error) {
                document.getElementById('api-status-text').textContent = '❌ Error checking API status';
            }
        }
        
        // Check API status when page loads
        checkApiStatus();
        
        document.getElementById('recommendationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const candidateData = Object.fromEntries(formData.entries());
            
            // Show loading
            const resultsDiv = document.getElementById('results');
            const recommendationsDiv = document.getElementById('recommendations');
            resultsDiv.style.display = 'block';
            recommendationsDiv.innerHTML = '<div class="loading">🔄 Analyzing your profile and finding best matches...</div>';
            
            try {
                const response = await fetch('/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(candidateData)
                });
                
                const result = await response.json();
                
                if (result.error) {
                    recommendationsDiv.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                    return;
                }
                
                // Display recommendations
                let html = `
                    <div style="margin-bottom: 20px; padding: 15px; background: #d5f4e6; border-radius: 5px;">
                        <strong>📊 Analysis Summary:</strong><br>
                        • Total internships analyzed: ${result.total_internships_analyzed}<br>
                        • Recommendations provided: ${result.recommendations.length}
                    </div>
                `;
                
                result.recommendations.forEach(rec => {
                    html += `
                        <div class="recommendation">
                            <h3>#${rec.rank} - ${rec.company} - ${rec.title}</h3>
                            <span class="match-score">${rec.match_score}% Match</span>
                            <div class="reasoning"><strong>Why this is a good match:</strong> ${rec.reasoning}</div>
                            <div class="skills"><strong>Skills to Highlight:</strong> ${rec.skills_to_highlight.join(', ')}</div>
                        </div>
                    `;
                });
                
                recommendationsDiv.innerHTML = html;
                
            } catch (error) {
                recommendationsDiv.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/recommend', methods=['POST'])
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

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'RAG Internship Recommender is running'})

@app.route('/api-status')
def api_status():
    """Check API status"""
    try:
        if is_api_configured():
            api_key = get_api_key()
            return jsonify({
                'status': 'connected',
                'message': f'API key configured: {api_key[:10]}...{api_key[-4:]}',
                'configured': True
            })
        else:
            return jsonify({
                'status': 'not_configured',
                'message': 'API key not set. Set OPENROUTER_API_KEY environment variable.',
                'configured': False
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error checking API status: {str(e)}',
            'configured': False
        })

if __name__ == '__main__':
    print("🚀 Starting RAG Internship Recommendation Web Interface")
    print("="*60)
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔑 Set OPENROUTER_API_KEY environment variable for AI features")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
