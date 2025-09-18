import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Bell, Settings, HelpCircle, FileText, Video, Building2 } from "lucide-react";

const Header = () => {
  return (
    <header className="bg-white border-b border-border px-4 py-2">
      <div className="flex items-center justify-between max-w-full">
        {/* Left side - Ministry logo */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-12 h-12 bg-gray-100 rounded border flex items-center justify-center">
              <span className="text-xs font-semibold text-center">MCA</span>
            </div>
            <div className="text-xs">
              <div className="font-semibold">MINISTRY OF</div>
              <div className="font-semibold">CORPORATE</div>
              <div className="font-semibold">AFFAIRS</div>
              <div className="text-gray-500">GOVERNMENT OF INDIA</div>
            </div>
          </div>
          
          {/* PM Internship logo */}
          <div className="flex items-center gap-2 ml-8">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-xs font-bold">PM</span>
            </div>
            <div className="text-lg font-bold text-blue-600">Internship</div>
          </div>
        </div>

        {/* Center navigation */}
        <div className="flex items-center gap-6">
          <Button variant="ghost" size="sm" className="text-sm">
            <HelpCircle className="w-4 h-4 mr-1" />
            FAQs
          </Button>
          <Button variant="ghost" size="sm" className="text-sm">
            <FileText className="w-4 h-4 mr-1" />
            Guidelines
          </Button>
          <Button variant="ghost" size="sm" className="text-sm">
            <Building2 className="w-4 h-4 mr-1" />
            Partner Companies
          </Button>
          <Button variant="ghost" size="sm" className="text-sm">
            <FileText className="w-4 h-4 mr-1" />
            Manuals
          </Button>
          <Button variant="ghost" size="sm" className="text-sm">
            <Video className="w-4 h-4 mr-1" />
            Tutorials/Guidance Videos
          </Button>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-3">
          <Button size="sm" className="bg-orange-500 hover:bg-orange-600 text-white">
            Admin Portal
          </Button>
          <Button size="sm" className="bg-orange-500 hover:bg-orange-600 text-white">
            My Portal
          </Button>
          <Select defaultValue="en">
            <SelectTrigger className="w-24 h-8">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="en">Language</SelectItem>
              <SelectItem value="hi">हिंदी</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="ghost" size="sm">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;