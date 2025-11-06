# Port Configuration Change Summary

## Changes Made

The backend has been moved from port **3000** to port **5000** to avoid conflicts with other projects.

### Updated Files

1. **backend/app.py**
   - Default port changed from 3000 to 5000
   - CORS origins updated (removed localhost:3000)

2. **frontend/package.json**
   - Proxy updated from `http://localhost:3000` to `http://localhost:5000`

3. **backend/.env.example**
   - PORT changed from 3000 to 5000

4. **Documentation Updated**
   - README.md
   - CLAUDE.md
   - SETUP.md

### Port Configuration

- **Backend**: Port 5000 (http://localhost:5000)
- **Frontend**: Port 3001 (http://localhost:3001)
- **Proxy**: Frontend proxies `/api/*` requests to `http://localhost:5000`

### Starting the Servers

```bash
# Terminal 1 - Backend (port 5000)
cd backend
source venv/bin/activate
python3 app.py

# Terminal 2 - Frontend (port 3001)
cd frontend
npm start
```

### Verify It Works

```bash
# Test backend health
curl http://localhost:5000/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat/start \
  -H "Content-Type: application/json" \
  -d '{"category":"restaurant"}'
```

---

**Status**: Port configuration updated ✅
**Backend now runs on port 5000**

