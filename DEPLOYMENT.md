# Render Deployment Guide

## Overview
This project is configured for deployment on Render with separate backend and frontend services.

## Services Configuration

### Backend Service
- **Type**: Web Service (Python)
- **Name**: meta-prompt-generator-backend
- **Environment**: Python
- **Plan**: Free
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python3 app.py`
- **Health Check**: `/health`

### Frontend Service
- **Type**: Static Site
- **Name**: meta-prompt-generator-frontend
- **Environment**: Static
- **Plan**: Free
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `./frontend/build`

## Environment Variables

### Backend Service
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Set to `production`
- `PORT`: Set to `10000` (Render's default)

### Frontend Service
- `REACT_APP_API_URL`: Backend service URL (e.g., `https://meta-prompt-generator-backend.onrender.com`)

## Deployment Steps

1. **Push to GitHub**: Ensure all code is committed and pushed to your repository
2. **Connect to Render**: Link your GitHub repository to Render
3. **Create Services**: Render will automatically detect and create services from `render.yaml`
4. **Set Environment Variables**: Add your OpenAI API key in the Render dashboard
5. **Deploy**: Services will automatically deploy

## URLs
- Backend: `https://meta-prompt-generator-backend.onrender.com`
- Frontend: `https://meta-prompt-generator-frontend.onrender.com`

## CORS Configuration
The backend is configured to accept requests from:
- Local development: `http://localhost:3001`, `http://localhost:3000`
- Production: `https://meta-prompt-generator-frontend.onrender.com`

## Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure frontend URL is added to backend CORS origins
2. **API Key Issues**: Verify `OPENAI_API_KEY` is set in backend environment
3. **Build Failures**: Check that all dependencies are in `requirements.txt` and `package.json`

### Health Checks
- Backend health check: `GET /health`
- Frontend: Static files should be served from `/build` directory

## Free Tier Limitations
- Services may sleep after 15 minutes of inactivity
- Cold starts may take 30-60 seconds
- Limited to 750 hours per month per service
