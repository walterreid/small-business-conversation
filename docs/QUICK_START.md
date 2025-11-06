# Quick Start Guide

## ✅ Current Configuration

- **Backend**: Port 5001 (http://localhost:5001)
- **Frontend**: Port 3001 (http://localhost:3001)
- **Proxy**: Frontend automatically proxies API calls to backend

## 🚀 Starting the Servers

### Option 1: Manual Start (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Option 2: Background Start

```bash
# Backend
cd backend
source venv/bin/activate
python3 app.py > /tmp/backend.log 2>&1 &
echo $! > /tmp/backend.pid

# Frontend
cd frontend
BROWSER=none npm start > /tmp/frontend.log 2>&1 &
echo $! > /tmp/frontend.pid
```

## 🛑 Stopping the Servers

```bash
# Stop by PID
kill $(cat /tmp/backend.pid 2>/dev/null)
kill $(cat /tmp/frontend.pid 2>/dev/null)

# Or stop by port
lsof -ti:5001 | xargs kill -9
lsof -ti:3001 | xargs kill -9
```

## ✅ Verify Everything Works

1. **Backend Health Check:**
```bash
curl http://localhost:5001/health
```

Should return: `{"status":"healthy","service":"small-business-marketing-tool"}`

2. **Visit Frontend:**
Open http://localhost:3001 in your browser

3. **Test the Flow:**
- Select a business category
- Answer questions in chat
- Generate marketing plan

## 🔧 Troubleshooting

### Backend Not Starting
- Check if port 5001 is free: `lsof -ti:5001`
- Verify .env has correct PORT: `cat backend/.env | grep PORT`
- Check backend logs: `tail -f /tmp/backend.log`

### Frontend Not Starting
- Check if port 3001 is free: `lsof -ti:3001`
- Clear node_modules and reinstall: `cd frontend && rm -rf node_modules && npm install`
- Check frontend logs: `tail -f /tmp/frontend.log`

### Black Screen
- Open browser console (F12) and check for errors
- Verify backend is running: `curl http://localhost:5001/health`
- Check that proxy is configured: `cat frontend/package.json | grep proxy`

### Connection Errors
- Verify backend is on port 5001
- Verify frontend proxy points to port 5001: `cat frontend/package.json | grep proxy`
- Check CORS in backend: `grep -A 5 "origins" backend/app.py`

## 📝 Current Port Configuration

- **Backend**: 5001 (changed from 5000 due to macOS AirPlay)
- **Frontend**: 3001
- **Proxy**: Frontend → Backend (automatic in development)

---

**Last Updated**: 2025-11-06
**Status**: ✅ Working

