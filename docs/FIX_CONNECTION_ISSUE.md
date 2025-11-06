# Fix: Cannot Connect to Server

## Problem Identified

Port 3000 is being used by another application (likely a different React project). The backend can't start because the port is already in use.

## Solution Options

### Option 1: Stop the Other Process (Recommended)

```bash
# Find what's using port 3000
lsof -ti:3000

# Kill it (replace PID with actual process ID)
kill -9 <PID>

# Or kill all processes on port 3000
lsof -ti:3000 | xargs kill -9
```

Then start your backend:
```bash
cd backend
source venv/bin/activate
python3 app.py
```

### Option 2: Use a Different Port for Backend

If you want to keep the other app running, change the backend port:

1. **Update backend/.env:**
```bash
PORT=3002
```

2. **Update frontend/package.json proxy:**
```json
"proxy": "http://localhost:3002"
```

3. **Restart both servers**

### Option 3: Use a Different Port for Frontend

Keep backend on 3000, use different port for frontend:

1. **Update frontend/package.json:**
```json
"scripts": {
  "start": "PORT=3002 react-scripts start"
}
```

2. **Update backend CORS in app.py** to include port 3002

## Quick Fix (Recommended)

```bash
# 1. Kill whatever is on port 3000
lsof -ti:3000 | xargs kill -9

# 2. Start backend
cd backend
source venv/bin/activate
python3 app.py

# 3. In another terminal, start frontend
cd frontend
npm start
```

## Verify It Works

After restarting:

1. **Backend health check:**
```bash
curl http://localhost:3000/health
```

2. **Test chat endpoint:**
```bash
curl -X POST http://localhost:3000/api/chat/start \
  -H "Content-Type: application/json" \
  -d '{"category":"restaurant"}'
```

3. **Visit frontend:**
Open `http://localhost:3001` in browser

## What Was Already Fixed

✅ **API Client Updated**: Changed to use relative URLs that work with the proxy
✅ **Proxy Configuration**: `package.json` has correct proxy setting
✅ **Routes Verified**: All chat endpoints exist in backend

The only issue is the port conflict!

---

**After fixing the port conflict, everything should work!**

