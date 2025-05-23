# Resume Generator API

AI-powered resume generator using FastAPI and Groq API with a beautiful frontend interface.

## Features
- 🎯 Beautiful, modern frontend interface
- 🤖 AI-powered resume generation using Groq API
- 🎨 Multiple resume styles (professional, modern, creative)
- ⚡ Lightning-fast generation (under 10 seconds)
- 📱 Mobile-responsive design
- 📋 One-click resume copying
- 🔧 RESTful API with FastAPI

## Try it yourself
### Clone my repo

Make your own directory and then do the following:

```bash
git clone https://github.com/Sheriff690/ResumeGennie.git
```

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROQ_API_KEY=your_api_key_here

# Run the server
uvicorn main:app --reload

# Visit http://localhost:8000
```

## Project Structure

<pre>resume-generator/
├── main.py              # FastAPI backend
├── requirements.txt     # Dependencies
├── vercel.json         # Vercel config
└── templates/
└── index.html      # Frontend template</pre>

## API Endpoints
- `GET /` - Frontend interface
- `GET /api` - API information
- `GET /health` - Health check
- `POST /generate-resume` - Generate resume

