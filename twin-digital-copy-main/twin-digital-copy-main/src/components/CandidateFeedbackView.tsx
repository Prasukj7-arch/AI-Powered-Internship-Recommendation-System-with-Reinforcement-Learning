import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import {
  CheckCircle,
  XCircle,
  TrendingUp,
  BookOpen,
  Target,
} from "lucide-react";

interface Feedback {
  id: string;
  decision: "accepted" | "rejected";
  feedback_text: string;
  strengths: string[];
  areas_for_improvement: string[];
  skill_gaps: string[];
  recommendation_score: number;
  created_at: string;
  applications: {
    company_name: string;
    internship_title: string;
    applied_at: string;
  };
}

interface LearningSummary {
  total_applications: number;
  average_score: number;
  common_skill_gaps: Array<{ skill: string; count: number }>;
  learning_progress: {
    skill_improvement_rate: number;
    feedback_quality: number;
    learning_consistency: number;
  };
  recommendations: string[];
}

const CandidateFeedbackView: React.FC = () => {
  const [feedbackHistory, setFeedbackHistory] = useState<Feedback[]>([]);
  const [learningSummary, setLearningSummary] =
    useState<LearningSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [candidateId] = useState("550e8400-e29b-41d4-a716-446655440000"); // Default candidate ID

  useEffect(() => {
    fetchFeedbackHistory();
    fetchLearningSummary();
  }, []);

  const fetchFeedbackHistory = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/candidate/feedback-history/${candidateId}`
      );
      const data = await response.json();
      setFeedbackHistory(data.feedback_history || []);
    } catch (error) {
      console.error("Error fetching feedback history:", error);
    }
  };

  const fetchLearningSummary = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/learning-summary/${candidateId}`
      );
      const data = await response.json();
      setLearningSummary(data.learning_summary);
    } catch (error) {
      console.error("Error fetching learning summary:", error);
    } finally {
      setLoading(false);
    }
  };

  const getDecisionIcon = (decision: string) => {
    return decision === "accepted" ? (
      <CheckCircle className="h-5 w-5 text-green-600" />
    ) : (
      <XCircle className="h-5 w-5 text-red-600" />
    );
  };

  const getDecisionBadge = (decision: string) => {
    return decision === "accepted" ? (
      <Badge className="bg-green-100 text-green-800">Accepted</Badge>
    ) : (
      <Badge className="bg-red-100 text-red-800">Rejected</Badge>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading feedback...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Your Application Feedback
        </h1>

        <Tabs defaultValue="feedback" className="space-y-6">
          <TabsList>
            <TabsTrigger value="feedback">Feedback History</TabsTrigger>
            <TabsTrigger value="learning">Learning Progress</TabsTrigger>
            <TabsTrigger value="insights">AI Insights</TabsTrigger>
          </TabsList>

          <TabsContent value="feedback" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Application Feedback</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {feedbackHistory.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      No feedback received yet. Apply to internships to get
                      feedback!
                    </div>
                  ) : (
                    feedbackHistory.map((feedback) => (
                      <div
                        key={feedback.id}
                        className="border rounded-lg p-6 space-y-4"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            {getDecisionIcon(feedback.decision)}
                            <div>
                              <h3 className="font-semibold text-lg">
                                {feedback.applications.company_name} -{" "}
                                {feedback.applications.internship_title}
                              </h3>
                              <p className="text-sm text-gray-500">
                                {new Date(
                                  feedback.created_at
                                ).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            {getDecisionBadge(feedback.decision)}
                            <Badge variant="outline">
                              Score: {feedback.recommendation_score}/10
                            </Badge>
                          </div>
                        </div>

                        {feedback.feedback_text && (
                          <div>
                            <h4 className="font-medium text-gray-900 mb-2">
                              Feedback
                            </h4>
                            <p className="text-gray-700">
                              {feedback.feedback_text}
                            </p>
                          </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          {feedback.strengths.length > 0 && (
                            <div>
                              <h4 className="font-medium text-green-800 mb-2">
                                Strengths
                              </h4>
                              <div className="flex flex-wrap gap-1">
                                {feedback.strengths.map((strength, index) => (
                                  <Badge
                                    key={index}
                                    className="bg-green-100 text-green-800"
                                  >
                                    {strength}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}

                          {feedback.areas_for_improvement.length > 0 && (
                            <div>
                              <h4 className="font-medium text-yellow-800 mb-2">
                                Areas for Improvement
                              </h4>
                              <div className="flex flex-wrap gap-1">
                                {feedback.areas_for_improvement.map(
                                  (area, index) => (
                                    <Badge
                                      key={index}
                                      className="bg-yellow-100 text-yellow-800"
                                    >
                                      {area}
                                    </Badge>
                                  )
                                )}
                              </div>
                            </div>
                          )}

                          {feedback.skill_gaps.length > 0 && (
                            <div>
                              <h4 className="font-medium text-red-800 mb-2">
                                Skill Gaps
                              </h4>
                              <div className="flex flex-wrap gap-1">
                                {feedback.skill_gaps.map((gap, index) => (
                                  <Badge
                                    key={index}
                                    className="bg-red-100 text-red-800"
                                  >
                                    {gap}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="learning" className="space-y-6">
            {learningSummary && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center">
                      <TrendingUp className="h-8 w-8 text-blue-600" />
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-600">
                          Total Applications
                        </p>
                        <p className="text-2xl font-bold text-gray-900">
                          {learningSummary.total_applications}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center">
                      <Target className="h-8 w-8 text-green-600" />
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-600">
                          Average Score
                        </p>
                        <p className="text-2xl font-bold text-gray-900">
                          {learningSummary.average_score.toFixed(1)}/10
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center">
                      <BookOpen className="h-8 w-8 text-purple-600" />
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-600">
                          Learning Progress
                        </p>
                        <p className="text-2xl font-bold text-gray-900">
                          {(
                            learningSummary.learning_progress
                              .learning_consistency * 100
                          ).toFixed(0)}
                          %
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            <Card>
              <CardHeader>
                <CardTitle>Learning Progress</CardTitle>
              </CardHeader>
              <CardContent>
                {learningSummary && (
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">
                          Skill Improvement Rate
                        </span>
                        <span className="text-sm text-gray-600">
                          {(
                            learningSummary.learning_progress
                              .skill_improvement_rate * 100
                          ).toFixed(1)}
                          %
                        </span>
                      </div>
                      <Progress
                        value={
                          learningSummary.learning_progress
                            .skill_improvement_rate * 100
                        }
                      />
                    </div>

                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">
                          Feedback Quality
                        </span>
                        <span className="text-sm text-gray-600">
                          {(
                            learningSummary.learning_progress.feedback_quality *
                            100
                          ).toFixed(1)}
                          %
                        </span>
                      </div>
                      <Progress
                        value={
                          learningSummary.learning_progress.feedback_quality *
                          100
                        }
                      />
                    </div>

                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">
                          Learning Consistency
                        </span>
                        <span className="text-sm text-gray-600">
                          {(
                            learningSummary.learning_progress
                              .learning_consistency * 100
                          ).toFixed(1)}
                          %
                        </span>
                      </div>
                      <Progress
                        value={
                          learningSummary.learning_progress
                            .learning_consistency * 100
                        }
                      />
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="insights" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>AI Learning Insights</CardTitle>
              </CardHeader>
              <CardContent>
                {learningSummary && (
                  <div className="space-y-6">
                    <div>
                      <h3 className="font-semibold text-lg mb-4">
                        Common Skill Gaps
                      </h3>
                      <div className="space-y-2">
                        {learningSummary.common_skill_gaps.map((gap, index) => (
                          <div
                            key={index}
                            className="flex justify-between items-center py-2 border-b"
                          >
                            <span>{gap.skill}</span>
                            <Badge variant="secondary">
                              Mentioned {gap.count} times
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg mb-4">
                        AI Recommendations
                      </h3>
                      <div className="space-y-2">
                        {learningSummary.recommendations.map(
                          (recommendation, index) => (
                            <div
                              key={index}
                              className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg"
                            >
                              <BookOpen className="h-5 w-5 text-blue-600 mt-0.5" />
                              <span className="text-blue-800">
                                {recommendation}
                              </span>
                            </div>
                          )
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default CandidateFeedbackView;
