import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { User, BarChart3, BookOpen } from "lucide-react";

interface HeaderProps {
  currentView: 'candidate' | 'recruiter' | 'feedback';
  onViewChange: (view: 'candidate' | 'recruiter' | 'feedback') => void;
}

const Header = ({ currentView, onViewChange }: HeaderProps) => {
  return (
    <header className="bg-white border-b border-border px-4 py-2">
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between max-w-full gap-4">
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

        {/* Right side */}
        <div className="flex flex-wrap items-center gap-2 lg:gap-3">
          <Button 
            size="sm" 
            className={`${currentView === 'recruiter' ? 'bg-blue-600' : 'bg-orange-500 hover:bg-orange-600'} text-white`}
            onClick={() => onViewChange('recruiter')}
          >
            <BarChart3 className="w-4 h-4 mr-1" />
            Admin Portal
          </Button>
          <Button 
            size="sm" 
            className={`${currentView === 'candidate' ? 'bg-blue-600' : 'bg-orange-500 hover:bg-orange-600'} text-white`}
            onClick={() => onViewChange('candidate')}
          >
            <User className="w-4 h-4 mr-1" />
            My Portal
          </Button>
          <Button 
            size="sm" 
            className={`${currentView === 'feedback' ? 'bg-blue-600' : 'bg-orange-500 hover:bg-orange-600'} text-white`}
            onClick={() => onViewChange('feedback')}
          >
            <BookOpen className="w-4 h-4 mr-1" />
            Learning
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
        </div>
      </div>
    </header>
  );
};

export default Header;