# Project Setup Guide

Complete setup instructions for local development.

---

## Prerequisites

- Python 3.9+ (check with `python3 --version`)
- Node.js 16+ (check with `node --version`)
- OpenAI API key

---

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Create .env file
# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Verify Setup

```bash
# Check that Flask is installed
python3 -c "import flask; print(flask.__version__)"

# Check that OpenAI is installed
python3 -c "from openai import OpenAI; print('OpenAI installed')"
```

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment (Optional)

Create `frontend/.env` if you need to override the default API URL:

```bash
REACT_APP_API_URL=http://localhost:5000
```

(Default is already set in `package.json` proxy)

### 3. Verify Setup

```bash
# Check that React is installed
npm list react

# Check that Chatscope UI Kit is installed
npm list @chatscope/chat-ui-kit-react
```

---

## Running Locally

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python3 app.py
```

Backend should start on `http://localhost:5000`

### Terminal 2 - Frontend

```bash
cd frontend
npm start
```

Frontend should start on `http://localhost:3001`

### Verify It Works

1. Visit `http://localhost:3001`
2. Select a business category
3. Start answering questions in the chat
4. Generate a marketing plan

---

## Troubleshooting

### Backend Issues

**"Module not found"**
```bash
# Make sure venv is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**"OPENAI_API_KEY not found"**
- Check that `.env` file exists in `backend/` directory
- Verify key format: `OPENAI_API_KEY=sk-...`
- No quotes around the key value
- Restart Flask server after changes

**"Port already in use"**
- Change PORT in `.env` file
- Or kill the process using port 5000

### Frontend Issues

**"Module not found"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**"Cannot connect to backend"**
- Verify backend is running on port 5000
- Check `REACT_APP_API_URL` in `.env` or `package.json` proxy
- Check browser console for CORS errors

**"Port 3001 already in use"**
- Change PORT in `package.json` scripts
- Or kill the process using port 3001

---

## Quick Setup Script

For a fresh setup, use the automated script from the project root:

```bash
./setup.sh
```

Or manually:

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env file and add your OPENAI_API_KEY
# OPENAI_API_KEY=sk-your-actual-key-here

# Frontend
cd ../frontend
npm install
```

---

## Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Backend venv created and activated
- [ ] Backend dependencies installed
- [ ] Backend .env file configured with API key
- [ ] Frontend dependencies installed
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access frontend at http://localhost:3001
- [ ] Can select category and start chat

---

**Last Updated**: 2025-01-XX

