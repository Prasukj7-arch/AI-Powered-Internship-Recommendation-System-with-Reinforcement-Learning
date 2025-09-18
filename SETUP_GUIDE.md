# 🚀 PM Internship Recommendation System - Setup Guide

A full-stack application that combines a React frontend with a Python Flask backend featuring RAG (Retrieval-Augmented Generation) for intelligent internship recommendations.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** (Recommended: Python 3.11 or 3.12)
- **Node.js 16+** and **npm**
- **Git**

## 🛠️ Quick Setup (Automated)

### Option 1: One-Command Setup (Recommended)

```bash
# Clone the repository
git clone <your-github-repo-url>
cd SIH_2025

# Run the automated setup script
python setup_complete.py
```

This script will:
- Create a Python virtual environment
- Install all Python dependencies
- Install Node.js dependencies
- Build the React frontend
- Start the application

## 🔧 Manual Setup

### Step 1: Clone and Navigate

```bash
git clone <your-github-repo-url>
cd SIH_2025
```

### Step 2: Python Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements_rag.txt
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory
cd twin-digital-copy-main/twin-digital-copy-main

# Install Node.js dependencies
npm install

# Build the frontend for production
npm run build

# Return to root directory
cd ../..
```

### Step 4: Environment Configuration

Create a `.env` file in the root directory:

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free

# Optional: Ollama Configuration (for local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Application Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 5: Run the Application

```bash
# Make sure you're in the root directory and virtual environment is activated
python app_with_rag.py
```

The application will be available at:
- **Frontend**: http://localhost:5000
- **API**: http://localhost:5000/api/

## 🎯 Usage

1. **Open your browser** and go to `http://localhost:5000`
2. **Browse internships** using the search and filter options
3. **Get AI recommendations** by clicking "Your top recommendations"
4. **Apply for internships** directly through the interface

## 🔍 Features

### Frontend Features
- ✅ Modern React UI with TypeScript
- ✅ Responsive design with Tailwind CSS
- ✅ Real-time search and filtering
- ✅ AI-powered recommendations
- ✅ Application tracking
- ✅ Beautiful internship cards

### Backend Features
- ✅ RAG-based recommendation system
- ✅ OpenRouter API integration (Mistral-7B)
- ✅ ChromaDB vector storage
- ✅ TF-IDF fallback system
- ✅ RESTful API endpoints
- ✅ CORS support

## 📁 Project Structure

```
SIH_2025/
├── app_with_rag.py              # Main Flask application
├── requirements_rag.txt         # Python dependencies
├── integrated_recommender.py    # RAG recommendation system
├── rag_internship_recommender.py # Core RAG implementation
├── simple_backup_recommender.py # TF-IDF fallback
├── config.py                    # Configuration settings
├── internships_all_streams_edited.csv # Internship data
├── chroma_storage/              # Vector database storage
├── twin-digital-copy-main/      # React frontend
│   └── twin-digital-copy-main/
│       ├── src/
│       │   ├── components/      # React components
│       │   ├── services/        # API services
│       │   └── ...
│       ├── package.json
│       └── ...
└── README.md
```

## 🚨 Troubleshooting

### Common Issues

1. **"No module named 'dotenv'"**
   ```bash
   pip install python-dotenv
   ```

2. **"vite is not recognized"**
   ```bash
   cd twin-digital-copy-main/twin-digital-copy-main
   npm install
   npm run build
   ```

3. **"RAG System: Not Available"**
   - Check your `.env` file has correct API keys
   - Ensure all dependencies are installed: `pip install -r requirements_rag.txt`

4. **Frontend not loading (404 errors)**
   - Make sure you've built the frontend: `npm run build`
   - Check that the `dist` folder exists in the frontend directory

5. **Python 3.13 compatibility issues**
   - Use Python 3.11 or 3.12 instead
   - Or install the minimal version: `pip install -r requirements_minimal.txt`

### Port Conflicts

If port 5000 is in use:
```bash
# Kill processes on port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# On macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

## 🔧 Development

### Running in Development Mode

```bash
# Terminal 1: Backend
python app_with_rag.py

# Terminal 2: Frontend (with hot reload)
cd twin-digital-copy-main/twin-digital-copy-main
npm run dev
```

### API Endpoints

- `GET /api/internships` - Get all internships
- `GET /api/internships?search=query` - Search internships
- `POST /api/recommend` - Get AI recommendations
- `POST /api/apply` - Apply for internship
- `GET /api/health` - Health check
- `GET /api/system-status` - System status

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |
| `OPENROUTER_BASE_URL` | OpenRouter API base URL | No (default provided) |
| `OPENROUTER_MODEL` | Model to use for recommendations | No (default provided) |
| `OLLAMA_BASE_URL` | Ollama server URL (for local LLM) | No |
| `OLLAMA_MODEL` | Ollama model name | No |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are installed
3. Verify your API keys are correct
4. Check the console logs for error messages

## 🎉 Success!

Once everything is set up, you should see:

```
🚀 Starting PM Internship Recommendation System with RAG
============================================================
📱 Frontend: http://localhost:5000
🔧 API: http://localhost:5000/api/
🤖 RAG System: Available
============================================================
✅ RAG recommender ready
✅ Backup recommender ready
```

Open your browser to `http://localhost:5000` and start exploring internships!
