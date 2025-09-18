# RAG Internship Recommendation System

AI-powered internship recommendation engine using RAG (Retrieval-Augmented Generation) architecture.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
# Set your OpenRouter API key
set OPENROUTER_API_KEY=your_api_key_here
```

### 3. Run the System

**Command Line:**
```bash
python rag_internship_recommender.py
```

**Web Interface:**
```bash
python web_interface.py
# Then open: http://localhost:5000
```

## 📁 Files

- `rag_internship_recommender.py` - Main recommendation engine
- `web_interface.py` - Web interface
- `config.py` - Configuration settings
- `internships_all_streams_edited.csv` - Dataset (200 internships)
- `requirements.txt` - Python dependencies

## 🎯 Features

- **200 Internships**: Real internship data
- **AI Recommendations**: Uses Mistral-7B model
- **Smart Matching**: TF-IDF + LLM reasoning
- **Web Interface**: User-friendly form
- **Detailed Analysis**: Match scores and reasoning

## 📊 Dataset

The system uses `internships_all_streams_edited.csv` with 200 real internship opportunities including:
- Company names (Apple, Microsoft, TCS, etc.)
- Various sectors and specializations
- Location data across India
- Detailed requirements and benefits

## 🔧 Usage

### Command Line
```python
from rag_internship_recommender import InternshipRecommender

# Initialize
recommender = InternshipRecommender("internships_all_streams_edited.csv", "your_api_key")

# Sample candidate
candidate = {
    "name": "John Doe",
    "education": "B.Tech Computer Science, 2024",
    "skills": "Python, Machine Learning, Data Analysis",
    "experience": "1 year coding experience",
    "interests": "AI/ML, Data Science",
    "location_preference": "Bangalore, Delhi",
    "career_goals": "Become a data scientist"
}

# Get recommendations
result = recommender.recommend_internships(candidate)
recommender.display_recommendations(result)
```

### Web Interface
1. Run: `python web_interface.py`
2. Open: http://localhost:5000
3. Fill in candidate details
4. Get instant recommendations

## 🎉 Ready to Use!

Your RAG-based internship recommendation system is ready with 200 real internships and AI-powered matching!