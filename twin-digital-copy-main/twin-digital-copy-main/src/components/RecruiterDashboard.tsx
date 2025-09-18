import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { CheckCircle, XCircle, Clock, Users, Building, TrendingUp } from 'lucide-react';

interface Application {
  id: string;
  candidate_id: string;
  company_name: string;
  internship_title: string;
  status: 'pending' | 'accepted' | 'rejected';
  applied_at: string;
  users: {
    name: string;
    email: string;
    profile_data: any;
  };
  application_data: {
    candidate_profile: any;
    internship_details: any;
  };
}

interface DashboardStats {
  total_applications: number;
  pending_applications: number;
  accepted_applications: number;
  rejected_applications: number;
  applications_by_company: Record<string, number>;
  recent_applications: Application[];
}

const RecruiterDashboard: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);
  const [feedback, setFeedback] = useState({
    decision: '',
    feedback_text: '',
    strengths: [] as string[],
    areas_for_improvement: [] as string[],
    skill_gaps: [] as string[],
    recommendation_score: 5
  });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchApplications();
    fetchDashboardStats();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/recruiter/applications');
      const data = await response.json();
      setApplications(data.applications || []);
    } catch (error) {
      console.error('Error fetching applications:', error);
    }
  };

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/recruiter/dashboard');
      const data = await response.json();
      setDashboardStats(data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReviewApplication = (application: Application) => {
    setSelectedApplication(application);
    setFeedback({
      decision: '',
      feedback_text: '',
      strengths: [],
      areas_for_improvement: [],
      skill_gaps: [],
      recommendation_score: 5
    });
  };

  const handleSubmitReview = async () => {
    if (!selectedApplication || !feedback.decision) return;

    setSubmitting(true);
    try {
      const response = await fetch(`http://localhost:5000/api/recruiter/application/${selectedApplication.id}/review`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
          ...feedback,
          recruiter_id: '550e8400-e29b-41d4-a716-446655440001'
          }),
      });

      if (response.ok) {
        await fetchApplications();
        await fetchDashboardStats();
        setSelectedApplication(null);
        setFeedback({
          decision: '',
          feedback_text: '',
          strengths: [],
          areas_for_improvement: [],
          skill_gaps: [],
          recommendation_score: 5
        });
      }
    } catch (error) {
      console.error('Error submitting review:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const addToArray = (field: keyof typeof feedback, value: string) => {
    if (value.trim()) {
      setFeedback(prev => ({
      ...prev,
        [field]: [...(prev[field] as string[]), value.trim()]
    }));
    }
  };

  const removeFromArray = (field: keyof typeof feedback, index: number) => {
    setFeedback(prev => ({
      ...prev,
      [field]: (prev[field] as string[]).filter((_, i) => i !== index)
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Recruiter Dashboard</h1>
        
        {/* Stats Cards */}
        {dashboardStats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <Users className="h-8 w-8 text-blue-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Applications</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardStats.total_applications}</p>
                  </div>
                </div>
          </CardContent>
        </Card>
        
        <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <Clock className="h-8 w-8 text-yellow-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Pending</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardStats.pending_applications}</p>
                  </div>
                </div>
          </CardContent>
        </Card>
        
        <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <CheckCircle className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Accepted</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardStats.accepted_applications}</p>
                  </div>
                </div>
          </CardContent>
        </Card>
        
        <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <XCircle className="h-8 w-8 text-red-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Rejected</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardStats.rejected_applications}</p>
                  </div>
                </div>
          </CardContent>
        </Card>
      </div>
        )}

        <Tabs defaultValue="applications" className="space-y-6">
          <TabsList>
            <TabsTrigger value="applications">Applications</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          <TabsContent value="applications" className="space-y-6">
      <Card>
        <CardHeader>
                <CardTitle>Pending Applications</CardTitle>
        </CardHeader>
        <CardContent>
                <div className="space-y-4">
                  {applications.filter(app => app.status === 'pending').map((application) => (
                    <div key={application.id} className="border rounded-lg p-4 hover:bg-gray-50">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg">{application.users.name}</h3>
                          <p className="text-gray-600">{application.company_name} - {application.internship_title}</p>
                          <p className="text-sm text-gray-500">Applied: {new Date(application.applied_at).toLocaleDateString()}</p>
                          <div className="mt-2">
                            <Badge variant="outline" className="mr-2">
                              {application.status}
                          </Badge>
                        </div>
                      </div>
                        <Button 
                          onClick={() => handleReviewApplication(application)}
                          className="ml-4"
                        >
                          Review
                        </Button>
                      </div>
                    </div>
                  ))}
                  
                  {applications.filter(app => app.status === 'pending').length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      No pending applications
                  </div>
                )}
                </div>
              </CardContent>
            </Card>
              </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Application Analytics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <h3 className="font-semibold">Applications by Company</h3>
                  {dashboardStats?.applications_by_company && Object.entries(dashboardStats.applications_by_company).map(([company, count]) => (
                    <div key={company} className="flex justify-between items-center py-2 border-b">
                      <span>{company}</span>
                      <Badge variant="secondary">{count}</Badge>
                    </div>
                  ))}
                </div>
        </CardContent>
      </Card>
          </TabsContent>
        </Tabs>

      {/* Review Modal */}
          {selectedApplication && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <CardHeader>
                <CardTitle>Review Application</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="font-semibold text-lg">{selectedApplication.users.name}</h3>
                  <p className="text-gray-600">{selectedApplication.company_name} - {selectedApplication.internship_title}</p>
              </div>

                <div>
                  <Label htmlFor="decision">Decision</Label>
                  <Select value={feedback.decision} onValueChange={(value) => setFeedback(prev => ({ ...prev, decision: value }))}>
                  <SelectTrigger>
                      <SelectValue placeholder="Select decision" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="accepted">Accept</SelectItem>
                    <SelectItem value="rejected">Reject</SelectItem>
                  </SelectContent>
                </Select>
              </div>

                <div>
                  <Label htmlFor="feedback_text">Feedback</Label>
                <Textarea
                    id="feedback_text"
                    value={feedback.feedback_text}
                    onChange={(e) => setFeedback(prev => ({ ...prev, feedback_text: e.target.value }))}
                    placeholder="Provide detailed feedback..."
                  rows={4}
                />
              </div>

                <div>
                  <Label htmlFor="recommendation_score">Recommendation Score (1-10)</Label>
                  <Input
                    id="recommendation_score"
                    type="number"
                    min="1"
                    max="10"
                    value={feedback.recommendation_score}
                    onChange={(e) => setFeedback(prev => ({ ...prev, recommendation_score: parseInt(e.target.value) || 5 }))}
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label>Strengths</Label>
              <div className="space-y-2">
                      {feedback.strengths.map((strength, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <Badge variant="secondary">{strength}</Badge>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => removeFromArray('strengths', index)}
                          >
                            ×
                          </Button>
                        </div>
                      ))}
                <div className="flex gap-2">
                  <Input
                          placeholder="Add strength"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                              addToArray('strengths', e.currentTarget.value);
                        e.currentTarget.value = '';
                      }
                    }}
                  />
                </div>
                </div>
              </div>

                  <div>
                    <Label>Areas for Improvement</Label>
              <div className="space-y-2">
                      {feedback.areas_for_improvement.map((area, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <Badge variant="secondary">{area}</Badge>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => removeFromArray('areas_for_improvement', index)}
                          >
                            ×
                          </Button>
                        </div>
                      ))}
                <div className="flex gap-2">
                  <Input
                          placeholder="Add improvement area"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                              addToArray('areas_for_improvement', e.currentTarget.value);
                        e.currentTarget.value = '';
                      }
                    }}
                  />
                </div>
                </div>
              </div>

                  <div>
                    <Label>Skill Gaps</Label>
              <div className="space-y-2">
                      {feedback.skill_gaps.map((gap, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <Badge variant="secondary">{gap}</Badge>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => removeFromArray('skill_gaps', index)}
                          >
                            ×
                          </Button>
                        </div>
                      ))}
                <div className="flex gap-2">
                  <Input
                          placeholder="Add skill gap"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                              addToArray('skill_gaps', e.currentTarget.value);
                        e.currentTarget.value = '';
                      }
                    }}
                  />
                </div>
                    </div>
                </div>
              </div>

                <div className="flex justify-end gap-4">
                  <Button
                    variant="outline"
                    onClick={() => setSelectedApplication(null)}
                  >
                  Cancel
                </Button>
                  <Button
                    onClick={handleSubmitReview}
                    disabled={submitting || !feedback.decision}
                  >
                    {submitting ? 'Submitting...' : 'Submit Review'}
                </Button>
              </div>
              </CardContent>
            </Card>
            </div>
          )}
      </div>
    </div>
  );
};

export default RecruiterDashboard;
