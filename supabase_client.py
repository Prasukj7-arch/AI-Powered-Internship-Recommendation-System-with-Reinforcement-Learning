

"""
Supabase client configuration and database operations
"""

import os
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.url or not self.key:
            print("⚠️ Supabase credentials not found. Set SUPABASE_URL and SUPABASE_ANON_KEY in .env")
            self.client = None
        else:
            self.client: Client = create_client(self.url, self.key)
            print("✅ Supabase client initialized")

    def is_connected(self) -> bool:
        """Check if Supabase is connected"""
        return self.client is not None

    async def create_application(self, application_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new application"""
        if not self.client:
            return None
        
        try:
            result = self.client.table('applications').insert(application_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Error creating application: {e}")
            return None

    async def get_applications_by_candidate(self, candidate_id: str) -> List[Dict[str, Any]]:
        """Get all applications for a candidate"""
        if not self.client:
            return []
        
        try:
            result = self.client.table('applications').select('*').eq('candidate_id', candidate_id).execute()
            return result.data or []
        except Exception as e:
            print(f"❌ Error fetching applications: {e}")
            return []

    async def get_pending_applications(self) -> List[Dict[str, Any]]:
        """Get all pending applications for recruiters"""
        if not self.client:
            return []
        
        try:
            result = self.client.table('applications').select('*, users!applications_candidate_id_fkey(*)').eq('status', 'pending').execute()
            return result.data or []
        except Exception as e:
            print(f"❌ Error fetching pending applications: {e}")
            return []

    async def update_application_status(self, application_id: str, status: str, recruiter_id: str) -> bool:
        """Update application status"""
        if not self.client:
            return False
        
        try:
            update_data = {
                'status': status,
                'recruiter_id': recruiter_id,
                'reviewed_at': datetime.now().isoformat()
            }
            
            result = self.client.table('applications').update(update_data).eq('id', application_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"❌ Error updating application status: {e}")
            return False

    async def create_feedback(self, feedback_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create feedback for an application"""
        if not self.client:
            return None
        
        try:
            result = self.client.table('feedback').insert(feedback_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Error creating feedback: {e}")
            return None

    async def get_feedback_for_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get feedback for a specific application"""
        if not self.client:
            return None
        
        try:
            result = self.client.table('feedback').select('*').eq('application_id', application_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Error fetching feedback: {e}")
            return None

    async def save_learning_data(self, learning_data: Dict[str, Any]) -> bool:
        """Save learning data for reinforcement learning"""
        if not self.client:
            return False
        
        try:
            result = self.client.table('learning_data').insert(learning_data).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"❌ Error saving learning data: {e}")
            return False

    async def get_learning_data_for_candidate(self, candidate_id: str) -> List[Dict[str, Any]]:
        """Get learning data for a candidate"""
        if not self.client:
            return []
        
        try:
            result = self.client.table('learning_data').select('*').eq('candidate_id', candidate_id).execute()
            return result.data or []
        except Exception as e:
            print(f"❌ Error fetching learning data: {e}")
            return []

    async def save_recommendation_history(self, history_data: Dict[str, Any]) -> bool:
        """Save recommendation history"""
        if not self.client:
            return False
        
        try:
            result = self.client.table('recommendation_history').insert(history_data).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"❌ Error saving recommendation history: {e}")
            return False

    async def get_candidate_stats(self, candidate_id: str) -> Dict[str, Any]:
        """Get candidate statistics"""
        if not self.client:
            return {}
        
        try:
            # Get applications for this candidate
            applications_result = self.client.table('applications').select('*').eq('candidate_id', candidate_id).execute()
            applications = applications_result.data or []
            
            # Get feedback for this candidate
            feedback_result = self.client.table('feedback').select('*').eq('application_id', applications[0].get('id')).execute() if applications else []
            feedback = feedback_result.data or []
            
            # Calculate statistics
            total_applications = len(applications)
            accepted_applications = len([app for app in applications if app.get('status') == 'accepted'])
            rejected_applications = len([app for app in applications if app.get('status') == 'rejected'])
            pending_applications = len([app for app in applications if app.get('status') == 'pending'])
            
            # Calculate average feedback score
            scores = [f.get('recommendation_score', 0) for f in feedback if f.get('recommendation_score')]
            average_feedback_score = sum(scores) / len(scores) if scores else 0
            
            return {
                'total_applications': total_applications,
                'accepted_applications': accepted_applications,
                'rejected_applications': rejected_applications,
                'pending_applications': pending_applications,
                'average_feedback_score': average_feedback_score,
                'total_recommendations': 0  # This would need to be calculated from recommendation_history
            }
        except Exception as e:
            print(f"❌ Error fetching candidate stats: {e}")
            return {}

    async def get_recruiter_dashboard_data(self) -> Dict[str, Any]:
        """Get recruiter dashboard data"""
        if not self.client:
            return {}
        
        try:
            # Get all applications
            applications_result = self.client.table('applications').select('*').execute()
            applications = applications_result.data or []
            
            # Calculate statistics
            total_applications = len(applications)
            pending_applications = len([app for app in applications if app.get('status') == 'pending'])
            accepted_applications = len([app for app in applications if app.get('status') == 'accepted'])
            rejected_applications = len([app for app in applications if app.get('status') == 'rejected'])
            
            # Get applications by company
            company_counts = {}
            for app in applications:
                company = app.get('company_name', 'Unknown')
                company_counts[company] = company_counts.get(company, 0) + 1
            
            # Get recent applications (last 20)
            recent_applications = sorted(applications, key=lambda x: x.get('applied_at', ''), reverse=True)[:20]
            
            return {
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'accepted_applications': accepted_applications,
                'rejected_applications': rejected_applications,
                'applications_by_company': company_counts,
                'recent_applications': recent_applications
            }
        except Exception as e:
            print(f"❌ Error fetching recruiter dashboard data: {e}")
            return {}

    async def get_applications_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get applications by status"""
        if not self.client:
            return []
        
        try:
            result = self.client.table('applications').select('*, users(*)').eq('status', status).execute()
            return result.data or []
        except Exception as e:
            print(f"❌ Error fetching applications by status: {e}")
            return []

    async def get_application_by_id(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get application by ID"""
        if not self.client:
            return None
        
        try:
            result = self.client.table('applications').select('*, users(*), feedback(*)').eq('id', application_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Error fetching application by ID: {e}")
            return None

    async def get_candidate_feedback_history(self, candidate_id: str) -> List[Dict[str, Any]]:
        """Get all feedback for a candidate"""
        if not self.client:
            return []
        
        try:
            result = self.client.table('feedback').select('*, applications(*), users(*)').eq('applications.candidate_id', candidate_id).execute()
            return result.data or []
        except Exception as e:
            print(f"❌ Error fetching candidate feedback history: {e}")
            return []

    async def update_candidate_profile(self, candidate_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update candidate profile"""
        if not self.client:
            return False
        
        try:
            result = self.client.table('users').update({'profile_data': profile_data}).eq('id', candidate_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"❌ Error updating candidate profile: {e}")
            return False

    async def get_learning_insights(self, candidate_id: str) -> Dict[str, Any]:
        """Get learning insights for a candidate"""
        if not self.client:
            return {}
        
        try:
            # Get all learning data for the candidate
            learning_data = await self.get_learning_data_for_candidate(candidate_id)
            
            # Get feedback history
            feedback_history = await self.get_candidate_feedback_history(candidate_id)
            
            # Calculate insights
            insights = {
                'total_feedback_received': len(feedback_history),
                'average_feedback_score': 0,
                'common_skill_gaps': [],
                'improvement_areas': [],
                'recommendation_accuracy': 0,
                'learning_progress': []
            }
            
            if feedback_history:
                scores = [f.get('recommendation_score', 0) for f in feedback_history if f.get('recommendation_score')]
                if scores:
                    insights['average_feedback_score'] = sum(scores) / len(scores)
                
                # Extract common skill gaps
                all_skill_gaps = []
                for feedback in feedback_history:
                    if feedback.get('skill_gaps'):
                        all_skill_gaps.extend(feedback['skill_gaps'])
                
                # Count skill gaps
                from collections import Counter
                skill_gap_counts = Counter(all_skill_gaps)
                insights['common_skill_gaps'] = [{'skill': skill, 'count': count} for skill, count in skill_gap_counts.most_common(5)]
            
            return insights
            
        except Exception as e:
            print(f"❌ Error getting learning insights: {e}")
            return {}

# Global instance
supabase_client = SupabaseClient()
