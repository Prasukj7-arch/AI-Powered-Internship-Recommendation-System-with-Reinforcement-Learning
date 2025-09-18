import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";
import { apiService } from "@/services/api";

interface InternshipCardProps {
  company: string;
  logo?: string;
  internshipId: string;
  title: string;
  areaField: string;
  state: string;
  district: string;
  benefits: string;
  candidatesApplied: number;
  tag?: string;
  recommendation?: number;
  onIncreaseMatch?: () => void;
}

const InternshipCard = ({
  company,
  logo,
  internshipId,
  title,
  areaField,
  state, 
  district,
  benefits,
  candidatesApplied,
  tag,
  recommendation,
  onIncreaseMatch
}: InternshipCardProps) => {
  const [isApplying, setIsApplying] = useState(false);
  const [applied, setApplied] = useState(false);

  const handleApply = async () => {
    try {
      setIsApplying(true);
      const result = await apiService.applyForInternship(internshipId, 51423); // Using sample user ID
      setApplied(true);
      console.log('Application successful:', result);
    } catch (error) {
      console.error('Application failed:', error);
      // You could add a toast notification here
    } finally {
      setIsApplying(false);
    }
  };
  return (
    <Card className={`p-4 space-y-3 relative transition-all duration-300 ${
      recommendation 
        ? 'shadow-lg hover:shadow-xl transform hover:-translate-y-1 bg-gradient-to-br from-white to-green-50 border-green-200' 
        : 'hover:shadow-md'
    }`}>
      {/* Recommendation Header */}
      {recommendation && (
        <div className="absolute -top-3 left-4 bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-1 rounded-full text-xs font-bold shadow-lg">
          RECOMMENDED {recommendation}% MATCH
        </div>
      )}
      {/* Company Header */}
      <div className="flex items-center gap-3">
        <div className="w-12 h-8 bg-gray-100 rounded border flex items-center justify-center">
          <span className="text-xs font-semibold">Logo</span>
        </div>
        <div>
          <h3 className="font-semibold text-sm">{company}</h3>
          {tag && (
            <span className="text-xs px-2 py-1 bg-orange-100 text-orange-800 rounded">
              {tag}
            </span>
          )}
        </div>
      </div>

      {/* Internship Details */}
      <div className="space-y-2 text-sm">
        <div className="grid grid-cols-2 gap-x-4 gap-y-1">
          <div>
            <span className="text-muted-foreground">Internship ID</span>
            <div className="font-medium text-orange-600">{internshipId}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Internship Title</span>
            <div className="font-medium text-orange-600">{title}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Area/Field</span>
            <div>{areaField}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Internship State</span>
            <div className="font-medium text-orange-600">{state}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Internship District</span>
            <div>{district}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Benefits</span>
            <div>{benefits}</div>
          </div>
        </div>
        
        <div>
          <span className="text-muted-foreground">Candidates Already Applied</span>
          <div className="font-medium">{candidatesApplied}</div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className={`flex gap-2 pt-2 ${recommendation ? 'grid grid-cols-3' : ''}`}>
        <Button variant="outline" size="sm" className="flex-1 bg-blue-600 text-white hover:bg-blue-700">
          View
        </Button>
        <Button 
          size="sm" 
          className={`flex-1 ${applied ? 'bg-gray-500' : 'bg-green-600 hover:bg-green-700'} text-white`}
          onClick={handleApply}
          disabled={isApplying || applied}
        >
          {isApplying ? 'Applying...' : applied ? 'Applied' : 'Apply'}
        </Button>
        {recommendation && (
          <Button 
            variant="outline" 
            size="sm" 
            className="flex-1 border-orange-300 text-orange-600 hover:bg-orange-50"
            onClick={onIncreaseMatch}
          >
            Increase Match
          </Button>
        )}
      </div>
    </Card>
  );
};

export default InternshipCard;