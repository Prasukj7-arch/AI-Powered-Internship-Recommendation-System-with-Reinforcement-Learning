/**
 * API Service for PM Internship Recommendation System
 * Handles all communication with the backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

export interface Internship {
  id: number;
  company: string;
  internshipId: string;
  title: string;
  areaField: string;
  state: string;
  district: string;
  benefits: string;
  candidatesApplied: number;
  tag?: string;
  recommendation?: number;
}

export interface CandidateProfile {
  name: string;
  education: string;
  skills: string;
  experience?: string;
  interests?: string;
  location?: string;
  goals?: string;
}

export interface RecommendationResult {
  candidate_profile: string;
  total_internships_analyzed: number;
  recommendations: Array<{
    rank: number;
    company: string;
    title: string;
    match_score: number;
    reasoning: string;
    skills_to_highlight: string[];
  }>;
  method: 'primary' | 'backup';
  fallback_used: boolean;
  timestamp: string;
}

export interface SystemStatus {
  primary_available: boolean;
  backup_available: boolean;
  api_configured: boolean;
  backup_chromadb_ready?: boolean;
  backup_chunks_count?: number;
  error?: string;
}

export interface InternshipFilters {
  state?: string;
  district?: string;
  sector?: string;
  field?: string;
  search?: string;
}

class ApiService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // System Status
  async getSystemStatus(): Promise<SystemStatus> {
    return this.request<SystemStatus>('/system-status');
  }

  // Health Check
  async getHealth(): Promise<{ status: string; message: string }> {
    return this.request<{ status: string; message: string }>('/health');
  }

  // Internships
  async getInternships(filters: InternshipFilters = {}): Promise<{
    internships: Internship[];
    total: number;
    filters: InternshipFilters;
  }> {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });

    const queryString = params.toString();
    const endpoint = queryString ? `/internships?${queryString}` : '/internships';
    
    return this.request<{
      internships: Internship[];
      total: number;
      filters: InternshipFilters;
    }>(endpoint);
  }

  // Recommendations
  async getRecommendations(profile: CandidateProfile): Promise<RecommendationResult> {
    return this.request<RecommendationResult>('/recommend', {
      method: 'POST',
      body: JSON.stringify(profile),
    });
  }

  // User Profile
  async getUserProfile(): Promise<unknown> {
    return this.request<unknown>('/user/profile');
  }

  async updateUserProfile(profile: any): Promise<unknown> {
    return this.request<unknown>('/user/profile', {
      method: 'POST',
      body: JSON.stringify(profile),
    });
  }

  // Applications
  async applyForInternship(internshipId: string, userId: string | number, candidateProfile?: any): Promise<{
    success: boolean;
    message: string;
    application_id: string;
  }> {
    return this.request<{
      success: boolean;
      message: string;
      application_id: string;
    }>('/apply', {
      method: 'POST',
      body: JSON.stringify({
        internship_id: internshipId,
        user_id: userId,
        candidate_profile: candidateProfile,
      }),
    });
  }

  // Improved Recommendations
  async getImprovedRecommendations(profile: CandidateProfile): Promise<RecommendationResult> {
    return this.request<RecommendationResult>('/improved-recommendations', {
      method: 'POST',
      body: JSON.stringify(profile),
    });
  }

  // Recruiter Dashboard
  async getRecruiterApplications(): Promise<{
    applications: any[];
    total: number;
  }> {
    return this.request<{
      applications: any[];
      total: number;
    }>('/recruiter/applications');
  }

  async getRecruiterDashboard(): Promise<any> {
    return this.request<any>('/recruiter/dashboard');
  }

  async reviewApplication(applicationId: string, reviewData: any): Promise<{
    message: string;
    application_id: string;
    decision: string;
    feedback_id: string;
  }> {
    return this.request<{
      message: string;
      application_id: string;
      decision: string;
      feedback_id: string;
    }>(`/recruiter/application/${applicationId}/review`, {
      method: 'POST',
      body: JSON.stringify(reviewData),
    });
  }

  // Candidate Feedback
  async getCandidateApplications(candidateId: string): Promise<{
    applications: any[];
    total: number;
  }> {
    return this.request<{
      applications: any[];
      total: number;
    }>(`/candidate/applications/${candidateId}`);
  }

  async getCandidateFeedbackHistory(candidateId: string): Promise<{
    candidate_id: string;
    feedback_history: any[];
    total_feedback: number;
  }> {
    return this.request<{
      candidate_id: string;
      feedback_history: any[];
      total_feedback: number;
    }>(`/candidate/feedback-history/${candidateId}`);
  }

  async getLearningSummary(candidateId: string): Promise<{
    candidate_id: string;
    learning_summary: any;
  }> {
    return this.request<{
      candidate_id: string;
      learning_summary: any;
    }>(`/learning-summary/${candidateId}`);
  }

  // User Recommendations
  async getUserRecommendations(userId: number): Promise<any> {
    return this.request<any>(`/recommendations/${userId}`);
  }
}

export const apiService = new ApiService();
export default apiService;
