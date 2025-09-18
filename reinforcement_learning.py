"""
Reinforcement Learning System for PM Internship Recommendations
This system learns from recruiter feedback to improve future recommendations
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio
from supabase_client import supabase_client
from collections import defaultdict, Counter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReinforcementLearningSystem:
    def __init__(self):
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # Exploration rate
        self.skill_weights = {}
        self.company_preferences = {}
        self.location_preferences = {}
        self.sector_preferences = {}
        self.feedback_history = []
        
    async def process_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """
        Process recruiter feedback and update the learning model
        """
        try:
            application_id = feedback_data.get('application_id')
            decision = feedback_data.get('decision')  # 'accepted' or 'rejected'
            feedback_score = feedback_data.get('recommendation_score', 5)  # 1-10 scale
            skill_gaps = feedback_data.get('skill_gaps', [])
            strengths = feedback_data.get('strengths', [])
            areas_for_improvement = feedback_data.get('areas_for_improvement', [])
            
            # Get the original application data
            application = await supabase_client.get_application_by_id(application_id)
            if not application:
                logger.error(f"Application {application_id} not found")
                return False
            
            candidate_profile = application.get('application_data', {}).get('candidate_profile', {})
            internship_details = application.get('application_data', {}).get('internship_details', {})
            
            # Calculate reward based on decision and feedback score
            reward = self._calculate_reward(decision, feedback_score)
            
            # Update learning data
            learning_data = {
                'candidate_id': application['candidate_id'],
                'application_id': application_id,
                'feedback_id': feedback_data.get('id'),
                'original_recommendation_score': self._calculate_original_score(candidate_profile, internship_details),
                'feedback_score': feedback_score,
                'skill_improvements': areas_for_improvement,
                'recommendation_improvements': self._generate_improvements(skill_gaps, strengths, areas_for_improvement),
                'reward': reward,
                'decision': decision
            }
            
            # Save learning data to database
            await supabase_client.save_learning_data(learning_data)
            
            # Update the learning model
            await self._update_model(candidate_profile, internship_details, reward, skill_gaps, strengths, areas_for_improvement)
            
            # Update candidate profile based on feedback
            await self._update_candidate_profile(application['candidate_id'], skill_gaps, strengths, areas_for_improvement)
            
            logger.info(f"Processed feedback for application {application_id}: {decision} (score: {feedback_score})")
            return True
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            return False
    
    def _calculate_reward(self, decision: str, feedback_score: int) -> float:
        """
        Calculate reward based on decision and feedback score
        """
        if decision == 'accepted':
            # Higher score for accepted applications
            base_reward = 1.0
            score_multiplier = feedback_score / 10.0
            return base_reward * score_multiplier
        else:
            # Lower reward for rejected applications, but still learn from them
            base_reward = -0.5
            score_multiplier = (10 - feedback_score) / 10.0
            return base_reward * score_multiplier
    
    def _calculate_original_score(self, candidate_profile: Dict, internship_details: Dict) -> float:
        """
        Calculate the original recommendation score
        """
        # This would be the score that was originally given to the recommendation
        # For now, we'll use a simple calculation based on skill matching
        candidate_skills = candidate_profile.get('skills', '').lower().split(', ')
        required_skills = internship_details.get('skills', '').lower().split(', ')
        
        if not required_skills or not candidate_skills:
            return 0.5
        
        # Calculate skill overlap
        skill_overlap = len(set(candidate_skills) & set(required_skills))
        total_skills = len(set(required_skills))
        
        if total_skills == 0:
            return 0.5
        
        return skill_overlap / total_skills
    
    def _generate_improvements(self, skill_gaps: List[str], strengths: List[str], areas_for_improvement: List[str]) -> Dict[str, Any]:
        """
        Generate improvement suggestions based on feedback
        """
        return {
            'skill_gaps_to_address': skill_gaps,
            'strengths_to_highlight': strengths,
            'areas_for_improvement': areas_for_improvement,
            'recommended_actions': self._generate_recommended_actions(skill_gaps, areas_for_improvement),
            'priority_skills': self._prioritize_skills(skill_gaps, areas_for_improvement)
        }
    
    def _generate_recommended_actions(self, skill_gaps: List[str], areas_for_improvement: List[str]) -> List[str]:
        """
        Generate specific recommended actions for the candidate
        """
        actions = []
        
        for skill in skill_gaps:
            actions.append(f"Take online course or certification in {skill}")
            actions.append(f"Practice {skill} through projects")
            actions.append(f"Join {skill} community or forum")
        
        for area in areas_for_improvement:
            actions.append(f"Focus on improving {area}")
            actions.append(f"Seek mentorship in {area}")
            actions.append(f"Get hands-on experience with {area}")
        
        return actions[:10]  # Limit to top 10 actions
    
    def _prioritize_skills(self, skill_gaps: List[str], areas_for_improvement: List[str]) -> List[Dict[str, Any]]:
        """
        Prioritize skills based on frequency and importance
        """
        all_skills = skill_gaps + areas_for_improvement
        skill_counts = Counter(all_skills)
        
        prioritized = []
        for skill, count in skill_counts.most_common():
            prioritized.append({
                'skill': skill,
                'priority': 'high' if count > 1 else 'medium',
                'frequency': count,
                'category': 'gap' if skill in skill_gaps else 'improvement'
            })
        
        return prioritized
    
    async def _update_model(self, candidate_profile: Dict, internship_details: Dict, reward: float, 
                           skill_gaps: List[str], strengths: List[str], areas_for_improvement: List[str]):
        """
        Update the learning model based on feedback
        """
        try:
            # Update skill weights
            candidate_skills = [skill.strip().lower() for skill in candidate_profile.get('skills', '').split(',')]
            required_skills = [skill.strip().lower() for skill in internship_details.get('skills', '').split(',')]
            
            # Update weights for skills that were gaps
            for skill in skill_gaps:
                skill_lower = skill.lower()
                if skill_lower in self.skill_weights:
                    self.skill_weights[skill_lower] += self.learning_rate * reward
                else:
                    self.skill_weights[skill_lower] = self.learning_rate * reward
            
            # Update weights for skills that were strengths
            for skill in strengths:
                skill_lower = skill.lower()
                if skill_lower in self.skill_weights:
                    self.skill_weights[skill_lower] += self.learning_rate * reward * 0.5
                else:
                    self.skill_weights[skill_lower] = self.learning_rate * reward * 0.5
            
            # Update company preferences
            company = internship_details.get('company', '').lower()
            if company:
                if company in self.company_preferences:
                    self.company_preferences[company] += self.learning_rate * reward
                else:
                    self.company_preferences[company] = self.learning_rate * reward
            
            # Update location preferences
            location = internship_details.get('location', '').lower()
            if location:
                if location in self.location_preferences:
                    self.location_preferences[location] += self.learning_rate * reward
                else:
                    self.location_preferences[location] = self.learning_rate * reward
            
            # Update sector preferences
            sector = internship_details.get('sector', '').lower()
            if sector:
                if sector in self.sector_preferences:
                    self.sector_preferences[sector] += self.learning_rate * reward
                else:
                    self.sector_preferences[sector] = self.learning_rate * reward
            
            logger.info("Updated learning model with feedback")
            
        except Exception as e:
            logger.error(f"Error updating model: {e}")
    
    async def _update_candidate_profile(self, candidate_id: str, skill_gaps: List[str], 
                                      strengths: List[str], areas_for_improvement: List[str]):
        """
        Update candidate profile based on feedback
        """
        try:
            # Get current profile
            applications = await supabase_client.get_applications_by_candidate(candidate_id)
            if not applications:
                return
            
            current_profile = applications[0].get('application_data', {}).get('candidate_profile', {})
            
            # Update skills based on feedback
            current_skills = current_profile.get('skills', '').split(', ')
            
            # Add new skills from strengths
            for strength in strengths:
                if strength not in current_skills:
                    current_skills.append(strength)
            
            # Update profile
            updated_profile = {
                **current_profile,
                'skills': ', '.join(current_skills),
                'skill_gaps_identified': skill_gaps,
                'strengths_identified': strengths,
                'areas_for_improvement': areas_for_improvement,
                'last_updated': datetime.now().isoformat()
            }
            
            # Save updated profile
            await supabase_client.update_candidate_profile(candidate_id, updated_profile)
            
            logger.info(f"Updated candidate profile for {candidate_id}")
            
        except Exception as e:
            logger.error(f"Error updating candidate profile: {e}")
    
    async def get_improved_recommendations(self, candidate_profile: Dict, internships: List[Dict], 
                                         num_recommendations: int = 5) -> List[Dict[str, Any]]:
        """
        Get improved recommendations based on learning
        """
        try:
            candidate_id = candidate_profile.get('candidate_id')
            if not candidate_id:
                return []
            
            # Get learning insights
            insights = await supabase_client.get_learning_insights(candidate_id)
            
            # Score each internship based on learned preferences
            scored_internships = []
            
            for internship in internships:
                score = self._calculate_improved_score(candidate_profile, internship, insights)
                scored_internships.append({
                    **internship,
                    'improved_score': score,
                    'learning_insights': self._get_recommendation_insights(candidate_profile, internship, insights)
                })
            
            # Sort by improved score
            scored_internships.sort(key=lambda x: x['improved_score'], reverse=True)
            
            # Return top recommendations
            return scored_internships[:num_recommendations]
            
        except Exception as e:
            logger.error(f"Error getting improved recommendations: {e}")
            return []
    
    def _calculate_improved_score(self, candidate_profile: Dict, internship: Dict, insights: Dict) -> float:
        """
        Calculate improved score based on learning
        """
        base_score = 0.5
        
        # Skill matching with learned weights
        candidate_skills = [skill.strip().lower() for skill in candidate_profile.get('skills', '').split(',')]
        required_skills = [skill.strip().lower() for skill in internship.get('skills', '').split(',')]
        
        skill_score = 0
        if required_skills:
            for skill in required_skills:
                if skill in candidate_skills:
                    # Apply learned weight
                    weight = self.skill_weights.get(skill, 1.0)
                    skill_score += weight
                else:
                    # Penalty for missing skills
                    weight = self.skill_weights.get(skill, 0.5)
                    skill_score += weight * 0.3
            
            skill_score = skill_score / len(required_skills)
        else:
            skill_score = 0.5
        
        # Company preference
        company = internship.get('company', '').lower()
        company_score = self.company_preferences.get(company, 0.5)
        
        # Location preference
        location = internship.get('location', '').lower()
        location_score = self.location_preferences.get(location, 0.5)
        
        # Sector preference
        sector = internship.get('sector', '').lower()
        sector_score = self.sector_preferences.get(sector, 0.5)
        
        # Combine scores with weights
        final_score = (
            skill_score * 0.4 +
            company_score * 0.2 +
            location_score * 0.2 +
            sector_score * 0.2
        )
        
        return min(max(final_score, 0.0), 1.0)  # Clamp between 0 and 1
    
    def _get_recommendation_insights(self, candidate_profile: Dict, internship: Dict, insights: Dict) -> Dict[str, Any]:
        """
        Get insights for why this internship is recommended
        """
        return {
            'learning_applied': len(insights.get('common_skill_gaps', [])) > 0,
            'skill_alignment': self._calculate_skill_alignment(candidate_profile, internship),
            'improvement_areas_addressed': self._check_improvement_areas(candidate_profile, internship, insights),
            'confidence_level': self._calculate_confidence(candidate_profile, internship, insights)
        }
    
    def _calculate_skill_alignment(self, candidate_profile: Dict, internship: Dict) -> float:
        """
        Calculate how well candidate skills align with internship requirements
        """
        candidate_skills = [skill.strip().lower() for skill in candidate_profile.get('skills', '').split(',')]
        required_skills = [skill.strip().lower() for skill in internship.get('skills', '').split(',')]
        
        if not required_skills:
            return 0.5
        
        overlap = len(set(candidate_skills) & set(required_skills))
        return overlap / len(required_skills)
    
    def _check_improvement_areas(self, candidate_profile: Dict, internship: Dict, insights: Dict) -> List[str]:
        """
        Check which improvement areas this internship addresses
        """
        addressed_areas = []
        common_gaps = [gap['skill'] for gap in insights.get('common_skill_gaps', [])]
        
        for gap in common_gaps:
            if gap.lower() in internship.get('skills', '').lower():
                addressed_areas.append(gap)
        
        return addressed_areas
    
    def _calculate_confidence(self, candidate_profile: Dict, internship: Dict, insights: Dict) -> str:
        """
        Calculate confidence level for this recommendation
        """
        skill_alignment = self._calculate_skill_alignment(candidate_profile, internship)
        feedback_count = insights.get('total_feedback_received', 0)
        
        if skill_alignment > 0.8 and feedback_count > 3:
            return 'high'
        elif skill_alignment > 0.6 and feedback_count > 1:
            return 'medium'
        else:
            return 'low'
    
    async def get_learning_summary(self, candidate_id: str) -> Dict[str, Any]:
        """
        Get a summary of learning progress for a candidate
        """
        try:
            insights = await supabase_client.get_learning_insights(candidate_id)
            
            return {
                'total_applications': insights.get('total_feedback_received', 0),
                'average_score': insights.get('average_feedback_score', 0),
                'common_skill_gaps': insights.get('common_skill_gaps', []),
                'learning_progress': self._calculate_learning_progress(candidate_id, insights),
                'recommendations': self._get_learning_recommendations(insights)
            }
            
        except Exception as e:
            logger.error(f"Error getting learning summary: {e}")
            return {}
    
    def _calculate_learning_progress(self, candidate_id: str, insights: Dict) -> Dict[str, Any]:
        """
        Calculate learning progress metrics
        """
        return {
            'skill_improvement_rate': len(insights.get('common_skill_gaps', [])) / max(insights.get('total_feedback_received', 1), 1),
            'feedback_quality': insights.get('average_feedback_score', 0) / 10.0,
            'learning_consistency': min(insights.get('total_feedback_received', 0) / 5.0, 1.0)
        }
    
    def _get_learning_recommendations(self, insights: Dict) -> List[str]:
        """
        Get recommendations for further learning
        """
        recommendations = []
        
        if insights.get('average_feedback_score', 0) < 6:
            recommendations.append("Focus on improving core technical skills")
        
        if len(insights.get('common_skill_gaps', [])) > 3:
            recommendations.append("Consider taking comprehensive skill development courses")
        
        if insights.get('total_feedback_received', 0) < 3:
            recommendations.append("Apply to more internships to get more feedback")
        
        return recommendations

# Global instance
rl_system = ReinforcementLearningSystem()
