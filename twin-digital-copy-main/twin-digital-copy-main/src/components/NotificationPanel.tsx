import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Bell, X } from "lucide-react";

const NotificationPanel = () => {
  const notifications = [
    {
      id: 1,
      title: "OTP Based Login for Portal Access",
      content: "Dear Candidates/Interns, Please be informed that, starting f...",
      date: "January 23, 2025 at 14:55",
      type: "announcement"
    },
    {
      id: 2,
      title: "Important Announcement for Candidates",
      content: "Dear Candidates, We would like to remind you of some key gui...",
      date: "December 5, 2024 at 10:38",
      type: "announcement"
    },
    {
      id: 3,
      title: "Confirm Your Joining for Internship and Eligibility for DBT",  
      content: "Dear Candidates, The module for marking your internship jo...",
      date: "November 28, 2024 at 09:41",
      type: "confirmation"
    }
  ];

  return (
    <div className="w-80 bg-white border-l border-border p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Bell className="w-5 h-5" />
          <h3 className="font-semibold">Notifications</h3>
        </div>
        <div className="bg-orange-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
          3
        </div>
      </div>

      {/* Stats */}
      <div className="flex gap-4 mb-4 text-sm">
        <div>
          <span className="font-bold">0</span> applied
        </div>
        <div>
          <span className="font-bold">3</span> remaining
        </div>
      </div>

      {/* Notifications List */}
      <div className="space-y-3">
        {notifications.map((notification) => (
          <Card key={notification.id} className="p-3">
            <div className="flex justify-between items-start mb-2">
              <h4 className="font-medium text-sm leading-tight">{notification.title}</h4>
              <Button variant="ghost" size="sm" className="h-4 w-4 p-0">
                <X className="w-3 h-3" />
              </Button>
            </div>
            <p className="text-xs text-muted-foreground mb-2 line-clamp-2">
              {notification.content}
            </p>
            <div className="flex justify-between items-center">
              <span className="text-xs text-orange-600">{notification.date}</span>
              <Button variant="link" size="sm" className="text-xs p-0 h-auto">
                Read More
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Bottom icons */}
      <div className="flex justify-end gap-2 mt-6">
        <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
          <span className="text-red-600 text-xs font-bold">DBT</span>
        </div>
        <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
          <span className="text-green-600 text-xs">✓</span>
        </div>
        <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
          <X className="w-4 h-4 text-red-600" />
        </div>
      </div>
    </div>
  );
};

export default NotificationPanel;