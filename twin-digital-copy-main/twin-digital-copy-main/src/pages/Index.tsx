import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import MainContent from "@/components/MainContent";
import NotificationPanel from "@/components/NotificationPanel";

const Index = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        <Sidebar />
        <MainContent />
        <NotificationPanel />
      </div>
      <footer className="bg-white border-t border-border p-4 text-center text-sm text-muted-foreground">
        © PM Internship Scheme, MCA. All Rights Reserved. | Technical Collaboration with BISAG-N
      </footer>
    </div>
  );
};

export default Index;
