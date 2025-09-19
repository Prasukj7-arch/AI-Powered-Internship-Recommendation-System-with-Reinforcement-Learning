"""
Final Working PM Internship Recommendation System
- Uses RAG recommender for AI-powered recommendations
- Connects to Supabase when available
- Provides real LLM-generated recommendations
"""

import os
import json
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from supabase_client import supabase_client
import uuid
from datetime import datetime
from reinforcement_learning import rl_system

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables
internships_data = []
recommender = None

def load_internships_from_csv():
    """Load internships from CSV"""
    global internships_data
    try:
        df = pd.read_csv('internships_all_streams_edited.csv')
        print(f"✅ Loaded {len(df)} internships from CSV")
        
        # Convert to the format expected by frontend
        internships_data = []
        for _, row in df.iterrows():
            internship = {
                "id": len(internships_data) + 1,
                "company": row.get('Company Name', ''),
                "internshipId": f"PMIS-2025-{len(internships_data) + 1}",
                "title": row.get('Internship Title', ''),
                "areaField": row.get('Area/Field', ''),
                "state": row.get('State/UT', ''),
                "district": row.get('District', ''),
                "benefits": row.get('Benefits', ''),
                "candidatesApplied": row.get('Candidates Already Applied', 0),
                "tag": row.get('Sector', ''),
                "sector": row.get('Sector', ''),
                "specialization": row.get('Specialization', ''),
                "skills": row.get('Preferred Skill(s)', ''),
                "description": row.get('Description', ''),
                "qualification": row.get('Minimum Qualification', ''),
                "location": row.get('Location', ''),
                "village": row.get('Village', ''),
                "zipCode": row.get('ZIP/Postal Code', ''),
                "opportunities": row.get('No. of Opportunities', 1)
            }
            internships_data.append(internship)
        
        return True
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False

def initialize_rag_recommender():
    """Initialize the RAG recommender system"""
    global recommender
    try:
        print("🤖 Initializing RAG recommender...")
        
        # Import and initialize the RAG recommender
        from integrated_recommender import IntegratedRecommender
        
        # Initialize with CSV data
        recommender = IntegratedRecommender(csv_file_path='internships_all_streams_edited.csv')
        print("✅ RAG recommender initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing RAG recommender: {e}")
        return False

def get_recommendations(candidate_profile):
    """Get recommendations using RAG system"""
    global recommender
    
    if not recommender:
        print("⚠️ RAG recommender not available")
        return []
    
    try:
        print(f"🔍 Getting RAG recommendations for: {candidate_profile.get('name', 'Unknown')}")
        
        # Get recommendations using RAG
        result = recommender.recommend_internships(candidate_profile, num_recommendations=5)
        
        if not result or 'recommendations' not in result:
            print("⚠️ No RAG recommendations returned")
            return []
        
        recommendations = result['recommendations']
        print(f"✅ Generated {len(recommendations)} RAG recommendations using {result.get('method', 'unknown')} method")
        
        # Convert to the format expected by frontend
        formatted_recommendations = []
        for i, rec in enumerate(recommendations):
            formatted_rec = {
                "rank": i + 1,
                "company": rec.get('company', ''),
                "title": rec.get('title', ''),
                "match_score": rec.get('match_score', 0),
                "reasoning": rec.get('reasoning', ''),
                "skills_to_highlight": rec.get('skills_to_highlight', []),
                "location": rec.get('location', ''),
                "sector": rec.get('sector', ''),
                "opportunities_available": rec.get('opportunities_available', 1)
            }
            formatted_recommendations.append(formatted_rec)
        
        return formatted_recommendations
        
    except Exception as e:
        print(f"❌ Error getting RAG recommendations: {e}")
        return []

@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    try:
        return send_from_directory('twin-digital-copy-main/twin-digital-copy-main/dist', 'index.html')
    except FileNotFoundError:
        return jsonify({"error": "Frontend not built. Please run 'npm run build' in the frontend directory."}), 404

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static assets"""
    return send_from_directory('twin-digital-copy-main/twin-digital-copy-main/dist/assets', filename)

@app.route('/favicon.ico')
def serve_favicon():
    """Serve favicon"""
    return send_from_directory('twin-digital-copy-main/twin-digital-copy-main/dist', 'favicon.ico')

@app.route('/api/internships', methods=['GET'])
def get_internships():
    """Get internships with optional filters"""
    try:
        # Get query parameters
        search_term = request.args.get('search', '').lower()
        state = request.args.get('state', '')
        sector = request.args.get('sector', '')
        specialization = request.args.get('specialization', '')
        limit = int(request.args.get('limit', 50))
        
        # Filter internships
        filtered_internships = internships_data
        
        if search_term:
            filtered_internships = [i for i in filtered_internships 
                                  if search_term in i.get('company', '').lower() 
                                  or search_term in i.get('title', '').lower()
                                  or search_term in i.get('skills', '').lower()]
        
        if state:
            filtered_internships = [i for i in filtered_internships 
                                  if i.get('state', '') == state]
        
        if sector:
            filtered_internships = [i for i in filtered_internships 
                                  if i.get('sector', '') == sector]
        
        if specialization:
            filtered_internships = [i for i in filtered_internships 
                                  if specialization.lower() in i.get('specialization', '').lower()]
        
        # Apply limit
        filtered_internships = filtered_internships[:limit]
        
        # Get filter options
        filter_options = {
            "states": list(set([i.get('state', '') for i in internships_data if i.get('state')])),
            "sectors": list(set([i.get('sector', '') for i in internships_data if i.get('sector')])),
            "specializations": list(set([i.get('specialization', '') for i in internships_data if i.get('specialization')])),
            "courses": [],
            "skills": []
        }
        
        return jsonify({
            "internships": filtered_internships,
            "filters": filter_options,
            "total": len(filtered_internships)
        })
        
    except Exception as e:
        print(f"❌ Error fetching internships: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def get_recommendations_endpoint():
    """Get AI-powered recommendations using RAG system"""
    try:
        # Get candidate data from request
        candidate_data = request.get_json()
        
        if not candidate_data:
            return jsonify({"error": "No candidate data provided"}), 400
        
        print(f"🔍 Getting recommendations for: {candidate_data.get('name', 'Unknown')}")
        
        # Get recommendations using RAG system
        recommendations = get_recommendations(candidate_data)
        
        if not recommendations:
            return jsonify({"error": "No recommendations found"}), 404
        
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        return jsonify({
            "recommendations": recommendations,
            "method": "RAG_AI_System",
            "fallback_used": False,
            "total_analyzed": len(internships_data)
        })
        
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/apply', methods=['POST'])
def apply_for_internship():
    """Apply for an internship"""
    try:
        data = request.get_json()
        internship_id = data.get('internship_id')
        user_id = data.get('user_id')
        candidate_profile = data.get('candidate_profile', {})
        
        if not internship_id or not user_id:
            return jsonify({"error": "Missing internship_id or user_id"}), 400
        
        # Find the internship details
        internship = next((i for i in internships_data if i.get('internshipId') == internship_id), None)
        if not internship:
            return jsonify({"error": "Internship not found"}), 404
        
        # Prepare application data for Supabase
        # Convert user_id to UUID format or use a default UUID
        if isinstance(user_id, int):
            # Convert integer to UUID string format
            candidate_uuid = f"550e8400-e29b-41d4-a716-{user_id:012d}"
        else:
            candidate_uuid = str(user_id)
        
        application_data = {
            "candidate_id": candidate_uuid,
            "internship_id": internship_id,
            "company_name": internship.get('company', ''),
            "internship_title": internship.get('title', ''),
            "application_data": {
                "candidate_profile": candidate_profile,
                "internship_details": internship,
                "applied_at": datetime.now().isoformat()
            },
            "status": "pending"
        }
        
        # Save to Supabase if available
        if supabase_client.is_connected():
            import asyncio
            result = asyncio.run(supabase_client.create_application(application_data))
            if result:
                application_id = result.get('id')
                print(f"✅ Application saved to Supabase: {application_id}")
            else:
                print("⚠️ Failed to save application to Supabase")
        else:
            print("⚠️ Supabase not connected, application not persisted")
        
        return jsonify({
            "message": "Application submitted successfully",
            "internship_id": internship_id,
            "user_id": user_id,
            "status": "pending",
            "application_id": str(uuid.uuid4()) if not supabase_client.is_connected() else None
        })
        
    except Exception as e:
        print(f"❌ Error processing application: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            "status": "healthy",
            "total_internships": len(internships_data),
            "rag_available": bool(recommender),
            "timestamp": str(pd.Timestamp.now())
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/api/system-status', methods=['GET'])
def system_status():
    """Get detailed system status"""
    try:
        return jsonify({
            "supabase_connected": supabase_client.is_connected(),
            "rag_available": bool(recommender),
            "backup_available": True,
            "total_internships": len(internships_data),
            "unique_states": len(set([i.get('state', '') for i in internships_data])),
            "unique_sectors": len(set([i.get('sector', '') for i in internships_data])),
            "api_configured": True,
            "recommendation_method": "RAG_AI_System" if recommender else "Not_Available"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New endpoints for recruiter dashboard and feedback system

@app.route('/api/recruiter/applications', methods=['GET'])
def get_pending_applications():
    """Get all pending applications for recruiters"""
    try:
        if not supabase_client.is_connected():
            return jsonify({"error": "Database not connected"}), 500
        
        import asyncio
        applications = asyncio.run(supabase_client.get_pending_applications())
        
        return jsonify({
            "applications": applications,
            "total": len(applications)
        })
        
    except Exception as e:
        print(f"❌ Error fetching applications: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/recruiter/application/<application_id>/review', methods=['POST'])
def review_application(application_id):
    """Review an application (accept/reject with feedback)"""
    try:
        data = request.get_json()
        decision = data.get('decision')  # 'accepted' or 'rejected'
        feedback_text = data.get('feedback_text', '')
        strengths = data.get('strengths', [])
        areas_for_improvement = data.get('areas_for_improvement', [])
        skill_gaps = data.get('skill_gaps', [])
        recommendation_score = data.get('recommendation_score')
        recruiter_id = data.get('recruiter_id', 'recruiter-001')  # Default recruiter ID
        
        if decision not in ['accepted', 'rejected']:
            return jsonify({"error": "Invalid decision. Must be 'accepted' or 'rejected'"}), 400
        
        if not supabase_client.is_connected():
            return jsonify({"error": "Database not connected"}), 500
        
        import asyncio
        
        # Update application status
        success = asyncio.run(supabase_client.update_application_status(
            application_id, decision, recruiter_id
        ))
        
        if not success:
            return jsonify({"error": "Failed to update application status"}), 500
        
        # Create feedback
        feedback_data = {
            "application_id": application_id,
            "recruiter_id": recruiter_id,
            "decision": decision,
            "feedback_text": feedback_text,
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "skill_gaps": skill_gaps,
            "recommendation_score": recommendation_score
        }
        
        feedback_result = asyncio.run(supabase_client.create_feedback(feedback_data))
        
        if feedback_result:
            # Process feedback through reinforcement learning system
            asyncio.run(rl_system.process_feedback(feedback_data))
            
            print(f"✅ Application {application_id} reviewed as {decision}")
            return jsonify({
                "message": f"Application {decision} successfully",
                "application_id": application_id,
                "decision": decision,
                "feedback_id": feedback_result.get('id')
            })
        else:
            return jsonify({"error": "Failed to create feedback"}), 500
        
    except Exception as e:
        print(f"❌ Error reviewing application: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/candidate/applications/<candidate_id>', methods=['GET'])
def get_candidate_applications(candidate_id):
    """Get all applications for a specific candidate"""
    try:
        if not supabase_client.is_connected():
            return jsonify({"error": "Database not connected"}), 500
        
        import asyncio
        applications = asyncio.run(supabase_client.get_applications_by_candidate(candidate_id))
        
        return jsonify({
            "applications": applications,
            "total": len(applications)
        })
        
    except Exception as e:
        print(f"❌ Error fetching candidate applications: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/candidate/feedback/<application_id>', methods=['GET'])
def get_application_feedback(application_id):
    """Get feedback for a specific application"""
    try:
        if not supabase_client.is_connected():
            return jsonify({"error": "Database not connected"}), 500
        
        import asyncio
        feedback = asyncio.run(supabase_client.get_feedback_for_application(application_id))
        
        if not feedback:
            return jsonify({"error": "No feedback found for this application"}), 404
        
        return jsonify({"feedback": feedback})
        
    except Exception as e:
        print(f"❌ Error fetching feedback: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/recruiter/dashboard', methods=['GET'])
def get_recruiter_dashboard():
    """Get recruiter dashboard data"""
    try:
        if not supabase_client.is_connected():
            return jsonify({"error": "Database not connected"}), 500
        
        import asyncio
        dashboard_data = asyncio.run(supabase_client.get_recruiter_dashboard_data())
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        print(f"❌ Error fetching dashboard data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/improved-recommendations', methods=['POST'])
def get_improved_recommendations():
    """Get improved recommendations using reinforcement learning"""
    try:
        candidate_data = request.get_json()
        
        if not candidate_data:
            return jsonify({"error": "No candidate data provided"}), 400
        
        print(f"🤖 Getting improved recommendations for: {candidate_data.get('name', 'Unknown')}")
        
        # Get improved recommendations using RL system
        import asyncio
        improved_recommendations = asyncio.run(rl_system.get_improved_recommendations(
            candidate_data, internships_data, num_recommendations=5
        ))
        
        if not improved_recommendations:
            # Fallback to regular recommendations
            recommendations = get_recommendations(candidate_data)
            return jsonify({
                "recommendations": recommendations,
                "method": "RAG_AI_System_Fallback",
                "learning_applied": False
            })
        
        # Format recommendations
        formatted_recommendations = []
        for i, rec in enumerate(improved_recommendations):
            formatted_rec = {
                "rank": i + 1,
                "company": rec.get('company', ''),
                "title": rec.get('title', ''),
                "match_score": int(rec.get('improved_score', 0) * 100),
                "reasoning": f"AI-optimized recommendation based on learning from feedback (Score: {rec.get('improved_score', 0):.2f})",
                "skills_to_highlight": rec.get('learning_insights', {}).get('strengths_to_highlight', []),
                "location": rec.get('location', ''),
                "sector": rec.get('sector', ''),
                "opportunities_available": rec.get('opportunities', 1),
                "learning_insights": rec.get('learning_insights', {}),
                "confidence_level": rec.get('learning_insights', {}).get('confidence_level', 'medium')
            }
            formatted_recommendations.append(formatted_rec)
        
        print(f"✅ Generated {len(formatted_recommendations)} improved recommendations")
        
        return jsonify({
            "recommendations": formatted_recommendations,
            "method": "Reinforcement_Learning_Enhanced",
            "learning_applied": True,
            "total_analyzed": len(internships_data)
        })
        
    except Exception as e:
        print(f"❌ Error getting improved recommendations: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/learning-summary/<candidate_id>', methods=['GET'])
def get_learning_summary(candidate_id):
    """Get learning summary for a candidate"""
    try:
        import asyncio
        summary = asyncio.run(rl_system.get_learning_summary(candidate_id))
        
        return jsonify({
            "candidate_id": candidate_id,
            "learning_summary": summary
        })
        
    except Exception as e:
        print(f"❌ Error getting learning summary: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/candidate/feedback-history/<candidate_id>', methods=['GET'])
def get_candidate_feedback_history(candidate_id):
    """Get feedback history for a candidate"""
    try:
        if not supabase_client.is_connected():
            return jsonify({"error": "Database not connected"}), 500
        
        import asyncio
        feedback_history = asyncio.run(supabase_client.get_candidate_feedback_history(candidate_id))
        
        return jsonify({
            "candidate_id": candidate_id,
            "feedback_history": feedback_history,
            "total_feedback": len(feedback_history)
        })
        
    except Exception as e:
        print(f"❌ Error fetching feedback history: {e}")
        return jsonify({"error": str(e)}), 500

def main():
    """Main function to start the application"""
    print("🚀 Starting PM Internship Recommendation System with RAG")
    print("=" * 60)
    print("📱 Frontend: http://localhost:8000")
    print("🔧 API: http://localhost:8000/api/")
    print("=" * 60)
    
    # Load internships data
    if not load_internships_from_csv():
        print("❌ Failed to load internships data")
        return
    
    print(f"✅ Loaded {len(internships_data)} internships")
    
    # Initialize RAG recommender
    if initialize_rag_recommender():
        print("🤖 RAG AI system ready")
    else:
        print("❌ RAG system failed to initialize")
    
    print("=" * 60)
    
    # Start Flask app
    try:
        app.run(host='0.0.0.0', port=8000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")

if __name__ == '__main__':
    main()
