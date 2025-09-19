-- PM Internship Recommendation System Database Schema
-- This file contains all the necessary tables for the application system

-- Create the main Internships table (already exists)
CREATE TABLE IF NOT EXISTS public."Internships" (
  "Company Name" text not null,
  "Internship Title" text not null,
  "Sector" text not null,
  "Area/Field" text not null,
  "No. of Opportunities" bigint not null,
  "Location" text not null,
  "State/UT" text not null,
  "District" text not null,
  "Village" text not null,
  "ZIP/Postal Code" bigint not null,
  "Minimum Qualification" text not null,
  "Description" text not null,
  "Course" text not null,
  "Specialization" text not null,
  "Certification(s)" text not null,
  "Preferred Skill(s)" text not null,
  "Qualification Description" text not null,
  "Benefits" text not null,
  "Benefits Description" text not null,
  "Candidates Already Applied" bigint not null,
  constraint Internships_pkey primary key (
    "Company Name",
    "Internship Title",
    "Sector",
    "Area/Field",
    "No. of Opportunities",
    "Location",
    "State/UT",
    "District",
    "Village",
    "ZIP/Postal Code",
    "Minimum Qualification",
    "Description",
    "Course",
    "Specialization",
    "Certification(s)",
    "Preferred Skill(s)",
    "Qualification Description",
    "Benefits",
    "Benefits Description",
    "Candidates Already Applied"
  )
) TABLESPACE pg_default;

-- Create users table for candidates and recruiters
CREATE TABLE IF NOT EXISTS public.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  user_type TEXT NOT NULL CHECK (user_type IN ('candidate', 'recruiter')),
  profile_data JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create applications table
CREATE TABLE IF NOT EXISTS public.applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  internship_id TEXT NOT NULL,
  company_name TEXT NOT NULL,
  internship_title TEXT NOT NULL,
  application_data JSONB NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
  recruiter_id UUID REFERENCES users(id) ON DELETE SET NULL,
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  reviewed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create feedback table
CREATE TABLE IF NOT EXISTS public.feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  recruiter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  decision TEXT NOT NULL CHECK (decision IN ('accepted', 'rejected')),
  feedback_text TEXT,
  strengths TEXT[],
  areas_for_improvement TEXT[],
  skill_gaps TEXT[],
  recommendation_score INTEGER CHECK (recommendation_score >= 1 AND recommendation_score <= 10),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create learning data table for reinforcement learning
CREATE TABLE IF NOT EXISTS public.learning_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  feedback_id UUID NOT NULL REFERENCES feedback(id) ON DELETE CASCADE,
  original_recommendation_score FLOAT,
  feedback_score FLOAT,
  skill_improvements TEXT[],
  recommendation_improvements JSONB,
  learning_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create recommendation history table
CREATE TABLE IF NOT EXISTS public.recommendation_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  session_id TEXT NOT NULL,
  recommendations JSONB NOT NULL,
  candidate_profile JSONB NOT NULL,
  method_used TEXT NOT NULL,
  feedback_applied BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_applications_candidate_id ON public.applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON public.applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_internship_id ON public.applications(internship_id);
CREATE INDEX IF NOT EXISTS idx_feedback_application_id ON public.feedback(application_id);
CREATE INDEX IF NOT EXISTS idx_learning_data_candidate_id ON public.learning_data(candidate_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_history_candidate_id ON public.recommendation_history(candidate_id);

-- Create functions for statistics
CREATE OR REPLACE FUNCTION get_candidate_stats(candidate_uuid UUID)
RETURNS JSONB AS $$
DECLARE
  result JSONB;
BEGIN
  SELECT jsonb_build_object(
    'total_applications', COUNT(*),
    'accepted_applications', COUNT(*) FILTER (WHERE status = 'accepted'),
    'rejected_applications', COUNT(*) FILTER (WHERE status = 'rejected'),
    'pending_applications', COUNT(*) FILTER (WHERE status = 'pending'),
    'average_feedback_score', AVG(f.recommendation_score) FILTER (WHERE f.recommendation_score IS NOT NULL),
    'total_recommendations', (SELECT COUNT(*) FROM recommendation_history WHERE candidate_id = candidate_uuid)
  )
  INTO result
  FROM applications a
  LEFT JOIN feedback f ON a.id = f.application_id
  WHERE a.candidate_id = candidate_uuid;
  
  RETURN COALESCE(result, '{}'::jsonb);
END;
$$ LANGUAGE plpgsql;

-- Create function for recruiter dashboard
CREATE OR REPLACE FUNCTION get_recruiter_dashboard()
RETURNS JSONB AS $$
DECLARE
  result JSONB;
BEGIN
  SELECT jsonb_build_object(
    'total_applications', COUNT(*),
    'pending_applications', COUNT(*) FILTER (WHERE status = 'pending'),
    'accepted_applications', COUNT(*) FILTER (WHERE status = 'accepted'),
    'rejected_applications', COUNT(*) FILTER (WHERE status = 'rejected'),
    'applications_by_company', (
      SELECT jsonb_object_agg(company_name, company_count)
      FROM (
        SELECT company_name, COUNT(*) as company_count
        FROM applications
        GROUP BY company_name
        ORDER BY company_count DESC
        LIMIT 10
      ) company_stats
    ),
    'recent_applications', (
      SELECT jsonb_agg(
        jsonb_build_object(
          'id', id,
          'candidate_name', u.name,
          'company_name', company_name,
          'internship_title', internship_title,
          'applied_at', applied_at,
          'status', status
        )
      )
      FROM applications a
      JOIN users u ON a.candidate_id = u.id
      ORDER BY applied_at DESC
      LIMIT 20
    )
  )
  INTO result
  FROM applications;
  
  RETURN COALESCE(result, '{}'::jsonb);
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON public.applications
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_feedback_updated_at BEFORE UPDATE ON public.feedback
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO public.users (id, email, name, user_type, profile_data) VALUES
  ('550e8400-e29b-41d4-a716-446655440000', 'candidate@example.com', 'Ignited Minds', 'candidate', 
   '{"education": "B.Tech in Mechatronics", "skills": "Python, Machine Learning, Data Analysis", "location": "Tirupati, ANDHRA PRADESH"}'),
  ('550e8400-e29b-41d4-a716-446655440001', 'recruiter@example.com', 'Recruiter One', 'recruiter', 
   '{"department": "HR", "company": "Tech Corp", "experience": "5 years"}')
ON CONFLICT (id) DO NOTHING;

-- Grant necessary permissions
GRANT ALL ON public.users TO authenticated;
GRANT ALL ON public.applications TO authenticated;
GRANT ALL ON public.feedback TO authenticated;
GRANT ALL ON public.learning_data TO authenticated;
GRANT ALL ON public.recommendation_history TO authenticated;
GRANT EXECUTE ON FUNCTION get_candidate_stats(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_recruiter_dashboard() TO authenticated;