# Troubleshooting Guide

## "Cannot Connect to Server" Error

### Issue
Frontend shows error: "Unable to connect to the server. Please check if the backend is running."

### Solutions

#### 1. Check if Backend is Running

```bash
# Check if backend is running on port 3000
lsof -ti:3000

# If not running, start it:
cd backend
source venv/bin/activate
python3 app.py
```

#### 2. Verify Backend is Responding

```bash
# Test health endpoint
curl http://localhost:3000/health

# Should return: {"status":"healthy","service":"small-business-marketing-tool"}
```

#### 3. Check Frontend Proxy Configuration

The frontend uses a proxy in `package.json`:
```json
"proxy": "http://localhost:3000"
```

This means:
- In development, frontend requests to `/api/*` are proxied to `http://localhost:3000/api/*`
- The API client now uses relative URLs (e.g., `/api/chat/start`) which use the proxy
- No need to set `REACT_APP_API_URL` in development

#### 4. Restart Frontend After Changes

If you just fixed the API URL issue:
```bash
# Stop frontend (Ctrl+C)
# Restart it
cd frontend
npm start
```

#### 5. Check Browser Console

Open browser DevTools (F12) and check:
- Network tab: Are requests going to `/api/chat/start` or `http://localhost:3000/api/chat/start`?
- Console tab: Any CORS errors?
- Errors: What's the exact error message?

### Common Issues

**Backend not running:**
- Start backend: `cd backend && source venv/bin/activate && python3 app.py`
- Should see: "Starting Flask app on port 3000"

**Port conflict:**
- Backend needs port 3000
- Frontend needs port 3001
- Check: `lsof -ti:3000` and `lsof -ti:3001`

**CORS errors:**
- Backend CORS is configured for localhost:3001
- If using different port, update `backend/app.py` CORS origins

**Proxy not working:**
- Restart frontend after changing `package.json`
- Clear browser cache
- Check that `proxy` field exists in `package.json`

### Quick Test

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python3 app.py

# Terminal 2 - Test backend
curl http://localhost:3000/health

# Terminal 3 - Frontend
cd frontend
npm start
```

Then visit `http://localhost:3001` and check browser console for errors.

---

**Last Updated**: 2025-01-XX

