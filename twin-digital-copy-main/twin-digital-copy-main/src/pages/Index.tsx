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
          <div className="flex flex-col lg:flex-row">
            <Sidebar />
            <MainContent />
            <NotificationPanel />
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Integrated Header with Navigation */}
      <Header currentView={currentView} onViewChange={setCurrentView} />
      
      {/* Main Content - grows to fill available space */}
      <div className="flex-1">
        {renderCurrentView()}
      </div>
      
      {/* Footer - sticks to bottom */}
      <footer className="bg-white border-t border-border p-4 text-center text-sm text-muted-foreground mt-auto">
        © PM Internship Scheme, MCA. All Rights Reserved. | Technical Collaboration with BISAG-N
      </footer>
    </div>
  );
};

export default Index;
