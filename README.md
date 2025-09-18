# RAG Internship Recommendation System

AI-powered internship recommendation engine with automatic fallback system. Uses OpenRouter API (Mistral-7B) as primary method and TF-IDF similarity as backup when API limits are reached.

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

**Integrated System (Recommended):**
```bash
python integrated_recommender.py
```

**Web Interface:**
```bash
python web_interface.py
# Then open: http://localhost:5000
```

**Individual Systems:**
```bash
# Primary system only
python rag_internship_recommender.py

# Backup system only
python simple_backup_recommender.py
```

## 📁 Files

- `integrated_recommender.py` - **Main integrated system (recommended)**
- `rag_internship_recommender.py` - Primary recommendation engine (OpenRouter API)
- `simple_backup_recommender.py` - Backup system (TF-IDF only)
- `web_interface.py` - Web interface with integrated system
- `config.py` - Configuration settings
- `internships_all_streams_edited.csv` - Dataset (200 internships)
- `requirements.txt` - Python dependencies

## 🎯 Features

- **200 Internships**: Real internship data
- **Dual System**: OpenRouter API + TF-IDF backup
- **Automatic Fallback**: Seamlessly switches to backup when API fails
- **Smart Matching**: AI reasoning + similarity matching
- **Web Interface**: User-friendly form with system status
- **Detailed Analysis**: Match scores (75-95%) and reasoning
- **No External Dependencies**: Backup system works without Ollama/ChromaDB

## 📊 Dataset

The system uses `internships_all_streams_edited.csv` with 200 real internship opportunities including:
- Company names (Apple, Microsoft, TCS, etc.)
- Various sectors and specializations
- Location data across India
- Detailed requirements and benefits

## 🔧 Usage

### Command Line
```python
from integrated_recommender import IntegratedRecommender

# Initialize integrated system
recommender = IntegratedRecommender("internships_all_streams_edited.csv")

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