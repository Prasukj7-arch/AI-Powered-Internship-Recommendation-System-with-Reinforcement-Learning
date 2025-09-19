# PM Internship Recommendation System with Reinforcement Learning

A comprehensive internship recommendation system that uses AI-powered recommendations, recruiter feedback, and reinforcement learning to continuously improve job matching for candidates.

## 🚀 Features

### For Candidates

- **AI-Powered Recommendations**: Get personalized internship recommendations using RAG (Retrieval-Augmented Generation)
- **Apply Functionality**: Apply to internships with one click
- **Feedback Learning**: View detailed feedback from recruiters and learn from rejections
- **AI-Enhanced Recommendations**: Get improved recommendations based on previous feedback
- **Learning Dashboard**: Track your progress and skill improvements over time

### For Recruiters

- **Application Management**: Review and manage all internship applications
- **Feedback System**: Provide detailed feedback with strengths, areas for improvement, and skill gaps
- **Analytics Dashboard**: View application statistics and trends
- **Decision Tracking**: Accept or reject applications with comprehensive feedback

### AI & Learning System

- **Reinforcement Learning**: System learns from recruiter feedback to improve future recommendations
- **Skill Gap Analysis**: Identifies common skill gaps and suggests improvements
- **Recommendation Optimization**: Continuously improves recommendation accuracy based on feedback
- **Learning Insights**: Provides detailed analytics on candidate progress

## 🏗️ System Architecture

```
Frontend (React + TypeScript)
├── Candidate View
├── Recruiter Dashboard
└── Feedback & Learning Dashboard

Backend (Flask + Python)
├── API Endpoints
├── RAG Recommendation System
├── Reinforcement Learning Engine
└── Supabase Integration

Database (Supabase PostgreSQL)
├── Internships Table
├── Applications Table
├── Users Table
├── Feedback Table
├── Learning Data Table
└── Recommendation History Table
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Supabase account
- OpenAI API key (for RAG system)

### 1. Clone and Setup Backend

```bash
# Clone the repository
git clone <repository-url>
cd SIH_2025

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your actual values
```

### 2. Database Setup

```bash
# Run the database setup script
python setup_database.py
```

### 3. Frontend Setup

```bash
cd twin-digital-copy-main/twin-digital-copy-main

# Install dependencies
npm install

# Build the frontend
npm run build
```

### 4. Start the Application

```bash
# Start the Flask backend
python app.py

# The application will be available at http://localhost:8000
```

## 📊 Database Schema

### Core Tables

1. **Internships**: Stores all available internship opportunities
2. **Users**: Stores candidate and recruiter information
3. **Applications**: Tracks all job applications
4. **Feedback**: Stores recruiter feedback and decisions
5. **Learning Data**: Stores reinforcement learning data
6. **Recommendation History**: Tracks recommendation sessions

### Key Functions

- `get_candidate_stats(candidate_uuid)`: Get candidate statistics
- `get_recruiter_dashboard()`: Get recruiter dashboard data
- `exec_sql(sql)`: Execute custom SQL (for setup)

## 🔄 Reinforcement Learning Flow

1. **Candidate applies** to an internship
2. **Recruiter reviews** the application and provides feedback
3. **Feedback is processed** by the reinforcement learning system
4. **Model is updated** based on the feedback (reward/penalty)
5. **Future recommendations** are improved using the learned patterns
6. **Candidate profile** is updated with skill improvements
7. **Learning insights** are generated for the candidate

## 🎯 API Endpoints

### Candidate Endpoints

- `POST /api/apply` - Apply for an internship
- `POST /api/recommend` - Get AI recommendations
- `POST /api/improved-recommendations` - Get AI-enhanced recommendations
- `GET /api/candidate/applications/<candidate_id>` - Get candidate applications
- `GET /api/candidate/feedback-history/<candidate_id>` - Get feedback history
- `GET /api/learning-summary/<candidate_id>` - Get learning summary

### Recruiter Endpoints

- `GET /api/recruiter/applications` - Get all applications
- `GET /api/recruiter/dashboard` - Get dashboard data
- `POST /api/recruiter/application/<id>/review` - Review application

### System Endpoints

- `GET /api/internships` - Get internships with filters
- `GET /api/health` - Health check
- `GET /api/system-status` - System status

## 🧠 Reinforcement Learning Details

### Learning Algorithm

- **Q-Learning inspired approach** for recommendation optimization
- **Reward calculation** based on recruiter decisions and feedback scores
- **Feature learning** for skills, companies, locations, and sectors
- **Continuous improvement** through feedback loops

### Key Components

- **Skill Weight Learning**: Adjusts skill importance based on feedback
- **Company Preference Learning**: Learns company preferences from outcomes
- **Location Preference Learning**: Adapts to location preferences
- **Sector Preference Learning**: Learns sector-specific patterns

### Learning Metrics

- **Recommendation Accuracy**: How well recommendations match recruiter preferences
- **Skill Gap Identification**: Accuracy in identifying skill gaps
- **Improvement Suggestions**: Quality of improvement recommendations
- **Learning Consistency**: How consistently the system learns from feedback

## 🎨 Frontend Components

### Main Components

- **Index.tsx**: Main navigation and routing
- **MainContent.tsx**: Internship browsing and recommendations
- **InternshipCard.tsx**: Individual internship display with apply functionality
- **RecruiterDashboard.tsx**: Recruiter interface for application management
- **CandidateFeedbackView.tsx**: Candidate feedback and learning dashboard

### Key Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live application status updates
- **Interactive Feedback**: Rich feedback collection interface
- **Learning Visualizations**: Progress tracking and insights

## 🔧 Configuration

### Environment Variables

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

### System Configuration

- **Learning Rate**: 0.1 (adjustable in reinforcement_learning.py)
- **Discount Factor**: 0.9 (adjustable)
- **Exploration Rate**: 0.1 (adjustable)
- **Recommendation Count**: 5 (adjustable)

## 📈 Usage Examples

### For Candidates

1. **Browse internships** using filters
2. **Get AI recommendations** based on your profile
3. **Apply to internships** with one click
4. **View feedback** from recruiters
5. **Get improved recommendations** based on learning
6. **Track progress** in the learning dashboard

### For Recruiters

1. **View all applications** in the dashboard
2. **Review applications** with candidate details
3. **Provide detailed feedback** with strengths and areas for improvement
4. **Accept or reject** applications
5. **View analytics** and trends

## 🚀 Future Enhancements

- **Multi-language Support**: Support for multiple languages
- **Advanced Analytics**: More detailed analytics and reporting
- **Mobile App**: Native mobile application
- **Integration APIs**: Integration with other job platforms
- **Advanced ML**: More sophisticated machine learning models
- **Real-time Notifications**: Push notifications for updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎉 Acknowledgments

- PM Internship Scheme, MCA
- Technical Collaboration with BISAG-N
- OpenAI for AI capabilities
- Supabase for database services
- React and TypeScript communities
