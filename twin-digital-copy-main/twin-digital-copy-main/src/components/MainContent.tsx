import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, MapPin, Settings, Loader2 } from "lucide-react";
import { useState, useEffect } from "react";
import InternshipCard from "./InternshipCard";
import MatchImprovementModal from "./MatchImprovementModal";
import { apiService, Internship, InternshipFilters } from "@/services/api";

const MainContent = () => {
  const [showRecommendedOnly, setShowRecommendedOnly] = useState(false);
  const [isMatchModalOpen, setIsMatchModalOpen] = useState(false);
  const [internships, setInternships] = useState<Internship[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<InternshipFilters>({});
  const [searchTerm, setSearchTerm] = useState("");
  const [recommendations, setRecommendations] = useState<Internship[]>([]);

  // Load internships on component mount
  useEffect(() => {
    loadInternships();
  }, []);

  const loadInternships = async (newFilters: InternshipFilters = {}) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.getInternships(newFilters);
      setInternships(result.internships);
      setFilters(result.filters);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load internships"
      );
      console.error("Error loading internships:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    const searchFilters = {
      ...filters,
      search: searchTerm,
    };
    loadInternships(searchFilters);
  };

  const handleFilterChange = (key: keyof InternshipFilters, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    loadInternships(newFilters);
  };

  const handleGetRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get user profile from the sidebar data or use default
      const profile = {
        name: "Ignited Minds",
        education: "B.Tech in Mechatronics",
        skills:
          "Python, Machine Learning, Data Analysis, Web Development, React, Node.js",
        experience:
          "2 months data science internship, 1 year coding experience",
        interests: "AI/ML, Data Science, Software Development, Web Development",
        location: "Tirupati, ANDHRA PRADESH",
        goals: "Become a senior data scientist in a leading tech company",
        candidate_id: "550e8400-e29b-41d4-a716-446655440000",
      };

      console.log("🔍 Getting recommendations with profile:", profile);
      const result = await apiService.getRecommendations(profile);
      console.log("✅ Recommendations received:", result);

      // Check if we have recommendations
      if (!result.recommendations || result.recommendations.length === 0) {
        setError(
          "No recommendations available. Try updating your profile or skills."
        );
        return;
      }

      // Map recommendations to actual internship data
      const recommendedInternships = result.recommendations.map(
        (rec, index) => {
          // Find matching internship in the current internships list
          // Use a more flexible matching approach that's case-insensitive and handles partial matches
          const matchingInternship = internships.find((internship) => {
            // Convert to lowercase for case-insensitive comparison
            const companyMatch =
              internship.company
                .toLowerCase()
                .includes(rec.company.toLowerCase()) ||
              rec.company
                .toLowerCase()
                .includes(internship.company.toLowerCase());
            const titleMatch =
              internship.title
                .toLowerCase()
                .includes(rec.title.toLowerCase()) ||
              rec.title.toLowerCase().includes(internship.title.toLowerCase());
            return companyMatch && titleMatch;
          });

          // If we found a matching internship, use its data, otherwise create a new one
          if (matchingInternship) {
            console.log(
              `✅ Found matching internship for ${rec.company} - ${rec.title}`
            );
            return {
              ...matchingInternship,
              recommendation: rec.match_score,
              reasoning: rec.reasoning,
              skills_to_highlight: rec.skills_to_highlight || [],
            };
          } else {
            // Create a new internship entry with the recommendation data
            console.log(
              `⚠️ No matching internship found for ${rec.company} - ${rec.title}. Creating new entry.`
            );
            return {
              id: index + 1,
              company: rec.company,
              internshipId: `PMIS-2025-${Math.floor(Math.random() * 10000)}`,
              title: rec.title,
              areaField: rec.sector || "Technology",
              state: rec.location || "ANDHRA PRADESH",
              district: "Tirupati",
              benefits: "Stipend + Learning + Experience",
              candidatesApplied: Math.floor(Math.random() * 10),
              tag: rec.sector || "Technology",
              recommendation: rec.match_score,
              reasoning: rec.reasoning,
              skills_to_highlight: rec.skills_to_highlight || [],
            };
          }
        }
      );

      console.log("🎯 Mapped recommendations:", recommendedInternships);
      setRecommendations(recommendedInternships);
      setShowRecommendedOnly(true);

      // Show success message
      console.log(
        `✅ Found ${recommendedInternships.length} recommendations using ${result.method} method`
      );
    } catch (err) {
      console.error("❌ Error getting recommendations:", err);
      setError(
        err instanceof Error ? err.message : "Failed to get recommendations"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-6">
      <Tabs defaultValue="opportunities" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="status">My Current Status</TabsTrigger>
          <TabsTrigger
            value="opportunities"
            className="bg-orange-500 text-white data-[state=active]:bg-orange-500"
          >
            Internship Opportunities
          </TabsTrigger>
          <TabsTrigger value="internship">My Internship</TabsTrigger>
          <TabsTrigger value="events">News & Events</TabsTrigger>
        </TabsList>

        <TabsContent value="opportunities" className="space-y-6">
          {/* Note */}
          <Card className="p-4 bg-orange-50 border-orange-200">
            <p className="text-sm text-orange-800">
              <span className="font-semibold">Note:</span> You can apply for a
              maximum of 3 internship IDs. Applications can be
              modified/withdrawn until last date of filing application
            </p>
          </Card>

          {/* Filters or Ranking Preferences */}
          {!showRecommendedOnly ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <Select
                value={filters.state || ""}
                onValueChange={(value) => handleFilterChange("state", value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select State" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="GUJARAT">Gujarat</SelectItem>
                  <SelectItem value="WEST BENGAL">West Bengal</SelectItem>
                  <SelectItem value="ANDHRA PRADESH">Andhra Pradesh</SelectItem>
                  <SelectItem value="MAHARASHTRA">Maharashtra</SelectItem>
                  <SelectItem value="KARNATAKA">Karnataka</SelectItem>
                </SelectContent>
              </Select>

              <Select
                value={filters.district || ""}
                onValueChange={(value) => handleFilterChange("district", value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select District" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Surat">Surat</SelectItem>
                  <SelectItem value="DINAJPUR DAKSHIN">
                    Dinajpur Dakshin
                  </SelectItem>
                  <SelectItem value="Tirupati">Tirupati</SelectItem>
                  <SelectItem value="Mumbai">Mumbai</SelectItem>
                  <SelectItem value="Bangalore">Bangalore</SelectItem>
                </SelectContent>
              </Select>

              <Select
                value={filters.sector || ""}
                onValueChange={(value) => handleFilterChange("sector", value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Sector" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Sales & Marketing">
                    Sales & Marketing
                  </SelectItem>
                  <SelectItem value="Engineering">Engineering</SelectItem>
                  <SelectItem value="Technology">Technology</SelectItem>
                  <SelectItem value="Finance">Finance</SelectItem>
                </SelectContent>
              </Select>

              <Select
                value={filters.field || ""}
                onValueChange={(value) => handleFilterChange("field", value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Field" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="FMCG">FMCG</SelectItem>
                  <SelectItem value="Banking">Banking</SelectItem>
                  <SelectItem value="Technology">Technology</SelectItem>
                  <SelectItem value="Healthcare">Healthcare</SelectItem>
                </SelectContent>
              </Select>

              <Button
                onClick={handleSearch}
                className="bg-red-500 hover:bg-red-600 text-white"
              >
                <Search className="w-4 h-4" />
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Settings className="w-4 h-4 text-orange-500" />
                <span className="text-sm font-medium">Ranking Preferences</span>
              </div>
              <Select>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Select preference" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="location">Location</SelectItem>
                  <SelectItem value="skills">Skills</SelectItem>
                  <SelectItem value="domain">Domain</SelectItem>
                </SelectContent>
              </Select>
              <Button
                variant="outline"
                onClick={() => setShowRecommendedOnly(false)}
                className="border-orange-300 text-orange-600 hover:bg-orange-50"
              >
                Show All Opportunities
              </Button>
            </div>
          )}

          {/* Filter by radius and search */}
          <div className="flex flex-col lg:flex-row items-start lg:items-center gap-4">
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-orange-500" />
              <span className="text-sm font-medium">Filter by radius</span>
            </div>
            <div className="flex-1 max-w-md">
              <Input placeholder="Enter kms" className="w-full" />
            </div>
            <div className="flex flex-col sm:flex-row gap-2 w-full lg:w-auto">
              <Button
                className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 text-lg font-semibold w-full sm:w-auto"
                onClick={
                  showRecommendedOnly
                    ? () => setShowRecommendedOnly(false)
                    : handleGetRecommendations
                }
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Loading...
                  </>
                ) : showRecommendedOnly ? (
                  "Show All"
                ) : (
                  "Your Top Recommendations"
                )}
              </Button>
              <div className="flex gap-2 w-full sm:w-auto">
                <Input
                  placeholder="Search..."
                  className="flex-1 sm:max-w-xs"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSearch()}
                />
                <Button
                  onClick={handleSearch}
                  variant="outline"
                  className="px-3"
                >
                  <Search className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <Card className="p-4 bg-red-50 border-red-200">
              <p className="text-sm text-red-800">
                <span className="font-semibold">Error:</span> {error}
              </p>
            </Card>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
              <span className="ml-2 text-muted-foreground">
                Loading internships...
              </span>
            </div>
          )}

          {/* Internship Cards Grid */}
          {!loading && (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {(showRecommendedOnly ? recommendations : internships)
                .filter(
                  (internship) =>
                    !showRecommendedOnly || internship.recommendation
                )
                .map((internship, index) => (
                  <InternshipCard
                    key={internship.id || index}
                    {...internship}
                    onIncreaseMatch={() => setIsMatchModalOpen(true)}
                  />
                ))}
            </div>
          )}

          {/* No Results */}
          {!loading &&
            !error &&
            (showRecommendedOnly ? recommendations : internships).length ===
              0 && (
              <Card className="p-8 text-center">
                <p className="text-muted-foreground">
                  {showRecommendedOnly
                    ? "No recommendations available. Try updating your profile or skills."
                    : "No internships found matching your criteria. Try adjusting your filters."}
                </p>
              </Card>
            )}
        </TabsContent>

        <TabsContent value="status">
          <div className="text-center py-8">
            <p className="text-muted-foreground">
              My Current Status content would go here
            </p>
          </div>
        </TabsContent>

        <TabsContent value="internship">
          <div className="text-center py-8">
            <p className="text-muted-foreground">
              My Internship content would go here
            </p>
          </div>
        </TabsContent>

        <TabsContent value="events">
          <div className="text-center py-8">
            <p className="text-muted-foreground">
              News & Events content would go here
            </p>
          </div>
        </TabsContent>
      </Tabs>

      <MatchImprovementModal
        isOpen={isMatchModalOpen}
        onClose={() => setIsMatchModalOpen(false)}
      />
    </div>
  );
};

export default MainContent;
