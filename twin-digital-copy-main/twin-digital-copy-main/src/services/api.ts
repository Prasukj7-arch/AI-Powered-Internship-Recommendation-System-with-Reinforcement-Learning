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
  async getUserProfile(): Promise<any> {
    return this.request<any>('/user/profile');
  }

  async updateUserProfile(profile: any): Promise<any> {
    return this.request<any>('/user/profile', {
      method: 'POST',
      body: JSON.stringify(profile),
    });
  }

  // Applications
  async applyForInternship(internshipId: string, userId: number): Promise<{
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
      }),
    });
  }

  // User Recommendations
  async getUserRecommendations(userId: number): Promise<any> {
    return this.request<any>(`/recommendations/${userId}`);
  }
}

export const apiService = new ApiService();
export default apiService;
