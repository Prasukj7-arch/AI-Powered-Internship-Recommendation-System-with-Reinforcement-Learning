# PM Internship Recommendation System

A fully functional AI-powered internship recommendation system with RAG (Retrieval-Augmented Generation) technology.

## 🚀 Features

- **AI-Powered Recommendations**: Uses OpenRouter API with Mistral-7B model
- **RAG System**: Intelligent matching based on skills, interests, and profile
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- **Real-time Search**: Filter internships by location, sector, and skills
- **Smart Fallback**: TF-IDF backup system if AI fails

## 🛠️ Tech Stack

- **Backend**: Python, Flask, RAG, OpenRouter API
- **Frontend**: React, TypeScript, Tailwind CSS, Shadcn/ui
- **AI**: Mistral-7B via OpenRouter API
- **Data**: CSV-based internship database

## 📦 Quick Start

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy environment template
copy env.example .env

# Edit .env file with your OpenRouter API key
OPENROUTER_API_KEY=your_api_key_here
```

### 3. Build Frontend
```bash
cd twin-digital-copy-main/twin-digital-copy-main
npm install
npm run build
cd ../..
```

### 4. Run Application
```bash
python app.py
```

### 5. Access Application
- **Frontend**: http://localhost:5000
- **API**: http://localhost:5000/api/

## 🎯 How to Use

1. **Browse Internships**: View all available internships with filters
2. **Get AI Recommendations**: Click "Your top recommendations" for personalized suggestions
3. **Apply**: Click "Apply" on any internship you're interested in
4. **Search**: Use the search bar to find specific internships

## 📱 Responsive Design

- **Mobile**: Single column layout, touch-friendly buttons
- **Tablet**: 2-column grids, optimized spacing
- **Desktop**: Full multi-column layout with all features

## 🔧 API Endpoints

- `GET /api/internships` - Get internships with filters
- `POST /api/recommend` - Get AI recommendations
- `POST /api/apply` - Apply for internship
- `GET /api/health` - Health check
- `GET /api/system-status` - System status

## 📊 Data Source

The system uses `internships_all_streams_edited.csv` containing 200+ internship opportunities across various sectors and locations.

## 🤖 AI Recommendation System

The RAG system analyzes:
- **Skills**: Python, Machine Learning, Web Development, etc.
- **Interests**: AI/ML, Data Science, Technology, etc.
- **Location**: State and district preferences
- **Education**: Qualification level matching
- **Experience**: Previous internships and projects

## 🎉 Success!

Your PM Internship Recommendation System is now:
- ✅ Fully functional with AI recommendations
- ✅ Responsive across all devices
- ✅ Clean and organized codebase
- ✅ Ready for production use

**Happy interning!** 🎓