# Render Deployment Guide

## Overview
This project is configured for deployment on Render with separate backend and frontend services. The application is a chat-based small business marketing plan generator.

## Services Configuration

### Backend Service
- **Type**: Web Service (Python)
- **Name**: small-business-marketing-tool-backend (or your preferred name)
- **Environment**: Python 3.9+
- **Plan**: Free (upgrade as needed)
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
- **Health Check**: `/health`

### Frontend Service
- **Type**: Static Site
- **Name**: small-business-marketing-tool-frontend (or your preferred name)
- **Environment**: Static
- **Plan**: Free
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `./frontend/build`

## Environment Variables

### Backend Service
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Set to `production`
- `PORT`: Set to `10000` (Render's default, or use environment variable)

### Frontend Service
- `REACT_APP_API_URL`: Backend service URL (e.g., `https://small-business-marketing-tool-backend.onrender.com`)

## Deployment Steps

1. **Push to GitHub**: Ensure all code is committed and pushed to your repository
2. **Connect to Render**: Link your GitHub repository to Render
3. **Create Services**: 
   - Create backend service (Web Service)
   - Create frontend service (Static Site)
   - Or use `render.yaml` if available for automatic setup
4. **Set Environment Variables**: Add your OpenAI API key and other variables in the Render dashboard
5. **Deploy**: Services will automatically deploy

## URLs

After deployment, you'll have:
- Backend: `https://your-backend-name.onrender.com`
- Frontend: `https://your-frontend-name.onrender.com`

Update the frontend's `REACT_APP_API_URL` environment variable to point to your backend URL.

## CORS Configuration

The backend is configured to accept requests from:
- Local development: `http://localhost:3001`, `http://localhost:3000`
- Production: Your frontend URL (update in `backend/app.py` if needed)

To update CORS origins, edit `backend/app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3001",
            "http://localhost:3000",
            "https://your-frontend-name.onrender.com",  # Add your production URL
        ],
        # ...
    }
})
```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure frontend URL is added to backend CORS origins in `app.py`
   - Restart backend service after changes
   - Clear browser cache

2. **API Key Issues**
   - Verify `OPENAI_API_KEY` is set in backend environment variables
   - Check that key starts with `sk-`
   - Ensure no extra quotes or spaces

3. **Build Failures**
   - Check that all dependencies are in `requirements.txt` and `package.json`
   - Verify Python and Node.js versions are compatible
   - Check build logs for specific errors

4. **Session Issues**
   - Sessions are stored in-memory (lost on restart)
   - This is expected behavior for MVP
   - Can be upgraded to database later

5. **Chat Not Working**
   - Verify backend is running and accessible
   - Check `REACT_APP_API_URL` is set correctly in frontend
   - Check browser console for errors
   - Verify OpenAI API key is valid

### Health Checks

- **Backend health check**: `GET /health`
  - Should return: `{"status": "healthy", "service": "small-business-marketing-tool"}`
- **Frontend**: Static files should be served from `/build` directory

### Testing Deployment

1. **Test Backend**:
   ```bash
   curl https://your-backend-name.onrender.com/health
   ```

2. **Test Chat Start**:
   ```bash
   curl -X POST https://your-backend-name.onrender.com/api/chat/start \
     -H "Content-Type: application/json" \
     -d '{"category": "restaurant"}'
   ```

3. **Test Frontend**: Visit your frontend URL and try the full flow

## Free Tier Limitations

- Services may sleep after 15 minutes of inactivity
- Cold starts may take 30-60 seconds
- Limited to 750 hours per month per service
- Sessions stored in-memory (lost on service restart)

## Upgrading from Free Tier

When ready to upgrade:
1. **Backend**: Upgrade to paid plan for always-on service
2. **Database**: Add PostgreSQL service for session persistence
3. **Frontend**: Usually fine on free tier (static hosting)

## Monitoring

- **Backend Logs**: Render Dashboard → Service → Logs tab
- **Frontend Logs**: Build logs in Render Dashboard
- **Health Checks**: Monitor `/health` endpoint
- **Error Tracking**: Check logs for OpenAI API errors, session issues

## Performance Tips

- Sessions are in-memory (fast but not persistent)
- Consider adding Redis for session storage if needed
- Frontend is static (very fast)
- Backend uses GPT-4o (optimize prompts to reduce token usage)

---

**Last Updated**: 2025-01-XX
**Version**: 2.0
