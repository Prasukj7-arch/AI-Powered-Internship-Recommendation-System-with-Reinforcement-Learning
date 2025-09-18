import React, { useState } from "react";
import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import MainContent from "@/components/MainContent";
import NotificationPanel from "@/components/NotificationPanel";
import RecruiterDashboard from "@/components/RecruiterDashboard";
import CandidateFeedbackView from "@/components/CandidateFeedbackView";

const Index = () => {
  const [currentView, setCurrentView] = useState<'candidate' | 'recruiter' | 'feedback'>('candidate');

  const renderCurrentView = () => {
    switch (currentView) {
      case 'recruiter':
        return <RecruiterDashboard />;
      case 'feedback':
        return <CandidateFeedbackView />;
      default:
        return (
          <div className="min-h-screen bg-gray-50">
            <Header />
            <div className="flex flex-col lg:flex-row">
              <Sidebar />
              <MainContent />
              <NotificationPanel />
            </div>
            <footer className="bg-white border-t border-border p-4 text-center text-sm text-muted-foreground">
              © PM Internship Scheme, MCA. All Rights Reserved. | Technical Collaboration with BISAG-N
            </footer>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">PM Internship System</h1>
          <div className="flex space-x-4">
            <button
              onClick={() => setCurrentView('candidate')}
              className={`px-4 py-2 rounded-md text-sm font-medium ${
                currentView === 'candidate'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Candidate View
            </button>
            <button
              onClick={() => setCurrentView('recruiter')}
              className={`px-4 py-2 rounded-md text-sm font-medium ${
                currentView === 'recruiter'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Recruiter Dashboard
            </button>
            <button
              onClick={() => setCurrentView('feedback')}
              className={`px-4 py-2 rounded-md text-sm font-medium ${
                currentView === 'feedback'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Feedback & Learning
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      {renderCurrentView()}
    </div>
  );
};

export default Index;
