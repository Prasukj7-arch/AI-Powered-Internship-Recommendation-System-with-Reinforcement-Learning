# PM Internship Recommendation System - Frontend Integration

This document provides instructions for running the integrated PM Internship Recommendation System with the new React frontend.

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS + Shadcn/ui
- **Backend**: Flask + Python
- **AI Engine**: OpenRouter API (Mistral-7B) with ChromaDB + Ollama fallback
- **Data**: CSV-based internship database

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the complete setup and start the system
python setup_and_run.py
```

This will:
- Install all dependencies
- Build the React frontend
- Start the Flask backend
- Open your browser to http://localhost:5000

### Option 2: Development Mode

```bash
# For development with hot reload
python run_dev.py
```

This will:
- Start Flask backend on http://localhost:5000
- Start React dev server on http://localhost:8080
- Enable hot reload for frontend changes

### Option 3: Manual Setup

#### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the Flask backend
python app.py
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd twin-digital-copy-main/twin-digital-copy-main

# Install dependencies
npm install

# Build for production
npm run build

# Or run in development mode
npm run dev
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### API Configuration

The system automatically falls back to ChromaDB + Ollama if the OpenRouter API is not available.

## 📱 Features

### Frontend Features
- **Responsive Design**: Modern UI with Tailwind CSS
- **Real-time Filtering**: Filter internships by state, district, sector, field
- **AI Recommendations**: Get personalized internship recommendations
- **Application Management**: Apply for internships with one click
- **Profile Management**: View and update user profile
- **Search Functionality**: Search internships by keywords

### Backend Features
- **RESTful API**: Complete API for frontend integration
- **AI Integration**: OpenRouter API with automatic fallback
- **Data Management**: CSV-based internship database
- **CORS Support**: Cross-origin requests enabled
- **Error Handling**: Comprehensive error handling and logging

## 🛠️ API Endpoints

### Core Endpoints

- `GET /` - Serve React frontend
- `GET /api/health` - Health check
- `GET /api/system-status` - System status and configuration
- `GET /api/internships` - Get internships with filtering
- `POST /api/recommend` - Get AI recommendations
- `POST /api/apply` - Apply for internship
- `GET /api/user/profile` - Get user profile
- `POST /api/user/profile` - Update user profile

### Example API Usage

```javascript
// Get internships with filters
const response = await fetch('/api/internships?state=GUJARAT&sector=Technology');
const data = await response.json();

// Get recommendations
const recommendations = await fetch('/api/recommend', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: "John Doe",
    education: "B.Tech Computer Science",
    skills: "Python, React, Node.js"
  })
});
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Node.js Dependencies Issues**
   ```bash
   cd twin-digital-copy-main/twin-digital-copy-main
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Python Dependencies Issues**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

4. **Build Issues**
   ```bash
   # Clear build cache
   cd twin-digital-copy-main/twin-digital-copy-main
   rm -rf dist
   npm run build
   ```

### Logs and Debugging

- Backend logs are displayed in the terminal
- Frontend logs are in browser console
- API errors are returned as JSON responses

## 📁 Project Structure

```
SIH_2025/
├── app.py                          # Main Flask application
├── integrated_recommender.py       # AI recommendation engine
├── web_interface.py               # Original web interface
├── requirements.txt               # Python dependencies
├── setup_and_run.py              # Automated setup script
├── run_dev.py                    # Development run script
├── twin-digital-copy-main/        # React frontend
│   └── twin-digital-copy-main/
│       ├── src/
│       │   ├── components/        # React components
│       │   ├── services/         # API services
│       │   └── pages/            # Page components
│       ├── package.json          # Node.js dependencies
│       └── vite.config.ts        # Vite configuration
└── internships_all_streams_edited.csv  # Internship data
```

## 🔄 Development Workflow

1. **Backend Changes**: Edit Python files, restart Flask server
2. **Frontend Changes**: Edit React files, hot reload enabled in dev mode
3. **API Changes**: Update both backend endpoints and frontend API service
4. **Database Changes**: Update CSV file and restart backend

## 🚀 Production Deployment

1. Build the frontend: `npm run build`
2. Ensure all dependencies are installed
3. Set environment variables
4. Run the Flask app: `python app.py`

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are properly installed
4. Verify the CSV data file exists and is accessible

## 🎯 Next Steps

- [ ] Add user authentication
- [ ] Implement database persistence
- [ ] Add more AI models
- [ ] Enhance recommendation algorithms
- [ ] Add analytics and reporting
- [ ] Implement real-time notifications
