# Backend Connection Issue - Fix Instructions

## Problem
The frontend can't connect to the backend. The backend routes exist but may not be running the latest code.

## Solution: Restart Backend

### Step 1: Stop Current Backend

```bash
# Find and kill the process on port 3000
lsof -ti:3000 | xargs kill -9
```

Or manually:
- Find the terminal running the backend
- Press `Ctrl+C` to stop it

### Step 2: Restart Backend

```bash
cd backend
source venv/bin/activate
python3 app.py
```

You should see:
```
Starting Flask app on port 3000
 * Running on http://0.0.0.0:3000
```

### Step 3: Verify Backend is Working

In a new terminal:
```bash
curl http://localhost:3000/health
```

Should return:
```json
{"status":"healthy","service":"small-business-marketing-tool"}
```

### Step 4: Test Chat Endpoint

```bash
curl -X POST http://localhost:3000/api/chat/start \
  -H "Content-Type: application/json" \
  -d '{"category":"restaurant"}'
```

Should return JSON with `session_id` and `first_question`.

### Step 5: Restart Frontend

The frontend API client has been updated to use the proxy correctly. Restart it:

```bash
cd frontend
npm start
```

### What Was Fixed

1. **API Client Updated**: Changed from absolute URLs (`http://localhost:3000/api/...`) to relative URLs (`/api/...`) which use the proxy in `package.json`

2. **Proxy Configuration**: The `package.json` has `"proxy": "http://localhost:3000"` which automatically forwards `/api/*` requests to the backend

3. **Development vs Production**: 
   - Development: Uses proxy (relative URLs)
   - Production: Uses `REACT_APP_API_URL` environment variable (absolute URLs)

---

**After restarting both servers, the connection should work!**

