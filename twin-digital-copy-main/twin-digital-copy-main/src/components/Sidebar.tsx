import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { MapPin, User, Lock, LogOut, AlertTriangle, Edit } from "lucide-react";

const Sidebar = () => {
  return (
    <div className="w-80 bg-white border-r border-border p-4 space-y-4">
      {/* Candidate ID */}
      <div className="bg-orange-100 text-orange-800 px-3 py-1 rounded text-sm font-medium flex items-center gap-2">
        <Edit className="w-4 h-4" />
        Candidate ID 51423
      </div>

      {/* Profile Card */}
      <Card className="p-4">
        <div className="flex items-center gap-3 mb-4">
          <Avatar className="w-16 h-16">
            <AvatarFallback className="text-lg">DU</AvatarFallback>
          </Avatar>
          <div>
            <h3 className="font-semibold">PORNADULLA USHA</h3>
            <p className="text-sm text-muted-foreground">19 Yrs</p>
            <p className="text-sm text-muted-foreground">B.Tech in Mechatronics</p>
          </div>
        </div>

        {/* Profile Completion */}
        <div className="mb-4">
          <div className="flex justify-between text-sm mb-1">
            <span>Profile Completed</span>
            <span className="font-semibold">100%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-500 h-2 rounded-full w-full"></div>
          </div>
        </div>

        {/* Location */}
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
          <MapPin className="w-4 h-4" />
          <span>Tirupati, ANDHRA PRADESH</span>
        </div>

        {/* Profile Actions */}
        <div className="space-y-2">
          <Button variant="outline" size="sm" className="w-full justify-start">
            <User className="w-4 h-4 mr-2" />
            View Profile / CV
          </Button>
          <Button variant="outline" size="sm" className="w-full justify-start">
            <Lock className="w-4 h-4 mr-2" />
            Change Password
          </Button>
          <Button variant="outline" size="sm" className="w-full justify-start">
            <LogOut className="w-4 h-4 mr-2" />
            Sign Out
          </Button>
        </div>
      </Card>

      {/* File a Grievance */}
      <Card className="p-4">
        <div className="text-center mb-3">
          <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <AlertTriangle className="w-6 h-6 text-blue-600" />
          </div>
          <h4 className="font-semibold">File a Grievance</h4>
        </div>
        <Button className="w-full bg-red-600 hover:bg-red-700 text-white">
          Add Grievance
        </Button>
      </Card>

      {/* Grievance Status */}
      <Card className="p-4">
        <h4 className="font-semibold mb-3">Grievance Status</h4>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm">Pending</span>
            <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs">1</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm">Disposed</span>
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">0</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm">Clarification Sought</span>
            <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">1</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm">Re-submitted</span>
            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">0</span>
          </div>
        </div>
      </Card>

      {/* Modify Consent */}
      <Button className="w-full bg-orange-500 hover:bg-orange-600 text-white">
        <AlertTriangle className="w-4 h-4 mr-2" />
        Modify Consent
      </Button>
    </div>
  );
};

export default Sidebar;