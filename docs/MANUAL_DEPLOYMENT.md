# Manual Render Deployment (No Blueprint)

This guide shows you how to manually configure services in Render without using the `render.yaml` blueprint.

## Step 1: Create Backend Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

### Backend Configuration

**Basic Settings:**
- **Name**: `small-business-marketing-tool-backend` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty (or set to `backend` if needed)

**Build & Deploy:**
- **Build Command**: 
  ```bash
  cd backend && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  cd backend && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
  ```

**Advanced Settings:**
- **Health Check Path**: `/health`
- **Auto-Deploy**: ✅ Yes

**Environment Variables:**
Add these in the "Environment" section:
- `OPENAI_API_KEY` = `sk-your-actual-key-here` (your OpenAI API key)
- `FLASK_ENV` = `production`
- `PORT` = `10000` (Render sets this automatically, but you can specify)

Click **"Create Web Service"** and wait for the first deployment.

---

## Step 2: Create Frontend Service

1. In Render Dashboard, click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Configure the service:

### Frontend Configuration

**Basic Settings:**
- **Name**: `small-business-marketing-tool-frontend` (or your preferred name)
- **Branch**: `main`
- **Root Directory**: Leave empty

**Build & Deploy:**
- **Build Command**: 
  ```bash
  cd frontend && npm install && npm run build
  ```
- **Publish Directory**: 
  ```
  frontend/build
  ```

**Environment Variables:**
- `REACT_APP_API_URL` = `https://your-backend-name.onrender.com`
  - ⚠️ **Important**: Replace `your-backend-name` with your actual backend service name from Step 1
  - Example: `https://small-business-marketing-tool-backend.onrender.com`

Click **"Create Static Site"** and wait for the first deployment.

---

## Step 3: Update CORS (If Needed)

After both services are deployed, you may need to update CORS settings in your backend:

1. Go to your backend service in Render
2. Check the service URL (e.g., `https://small-business-marketing-tool-backend.onrender.com`)
3. Update `backend/app.py` CORS configuration to include your frontend URL:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3001",
            "http://localhost:3000",
            "https://your-frontend-name.onrender.com",  # Add your frontend URL here
        ],
        "supports_credentials": True
    }
})
```

4. Commit and push the change
5. Render will auto-deploy

---

## Step 4: Verify Deployment

### Test Backend:
```bash
curl https://your-backend-name.onrender.com/health
```
Should return: `{"status": "healthy", "service": "small-business-marketing-tool"}`

### Test Frontend:
Visit your frontend URL and try the full flow:
1. Select a marketing goal
2. Click on a question
3. Start chatting with Zansei
4. Generate a marketing plan

---

## Important Notes

### render.yaml
- You can **delete** `render.yaml` if you want, or just leave it (it won't be used if you're not using blueprints)
- If you delete it, you might want to add it to `.gitignore` or just leave it

### Environment Variables
- **Backend**: Must have `OPENAI_API_KEY` set or the app won't work
- **Frontend**: Must have `REACT_APP_API_URL` pointing to your backend URL
- Update frontend's `REACT_APP_API_URL` if you change the backend service name

### Service URLs
- Backend URL format: `https://[service-name].onrender.com`
- Frontend URL format: `https://[service-name].onrender.com`
- These are set automatically based on your service names

### Auto-Deploy
- Both services are set to auto-deploy on push to `main`
- You can disable this in service settings if needed

---

## Troubleshooting

### Backend won't start
- Check that `OPENAI_API_KEY` is set correctly
- Verify build command runs successfully
- Check logs in Render dashboard

### Frontend can't connect to backend
- Verify `REACT_APP_API_URL` matches your backend URL exactly
- Check CORS settings in `backend/app.py`
- Ensure backend service is running (check health endpoint)

### Build fails
- Check that all dependencies are in `requirements.txt` and `package.json`
- Verify Python/Node versions are compatible
- Check build logs for specific errors

---

**Last Updated**: 2025-11-10
**Version**: Manual Setup Guide

