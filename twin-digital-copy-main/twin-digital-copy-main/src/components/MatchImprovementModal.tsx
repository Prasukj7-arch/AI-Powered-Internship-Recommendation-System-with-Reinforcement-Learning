import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { CheckCircle, MapPin, User, Briefcase } from "lucide-react";

interface MatchImprovementModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const MatchImprovementModal = ({ isOpen, onClose }: MatchImprovementModalProps) => {
  const improvements = [
    {
      icon: <MapPin className="w-5 h-5 text-blue-600" />,
      title: "Update Location Preferences",
      description: "Adjust your preferred locations to match more opportunities",
      action: "Set preferred cities and willingness to relocate"
    },
    {
      icon: <User className="w-5 h-5 text-green-600" />,
      title: "Complete Skills Assessment",
      description: "Take skill tests to improve your profile matching",
      action: "Complete pending skill assessments"
    },
    {
      icon: <Briefcase className="w-5 h-5 text-orange-600" />,
      title: "Add Relevant Experience",
      description: "Include projects, internships, or volunteer work",
      action: "Update your experience section"
    }
  ];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold text-center">
            How to Improve Your Match Score
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4 py-4">
          {improvements.map((item, index) => (
            <div key={index} className="flex gap-3 p-3 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0 mt-0.5">
                {item.icon}
              </div>
              <div className="flex-1 space-y-2">
                <h4 className="font-medium text-sm">{item.title}</h4>
                <p className="text-xs text-muted-foreground">{item.description}</p>
                <Button size="sm" variant="outline" className="text-xs h-7">
                  {item.action}
                </Button>
              </div>
            </div>
          ))}
        </div>
        
        <div className="flex justify-center pt-2">
          <Button onClick={onClose} className="bg-orange-500 hover:bg-orange-600 text-white">
            Got it!
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default MatchImprovementModal;