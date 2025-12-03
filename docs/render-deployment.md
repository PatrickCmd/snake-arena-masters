# Render Deployment Guide

## Overview

This guide walks you through deploying Snake Arena Masters to Render using the free tier.

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- Git repository with your code pushed

## Architecture

```
Render Platform
├── PostgreSQL Database (Free tier)
├── Backend Web Service (Free tier - Python)
└── Frontend Static Site (Free tier)
```

## Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Prepare for Render deployment"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/snake-arena-masters.git
git push -u origin main
```

### 2. Sign Up for Render

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 3. Deploy Using render.yaml

#### Option A: Automatic (Recommended)

1. Go to https://dashboard.render.com
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select `snake-arena-masters` repository
5. Render will automatically detect `render.yaml`
6. Click **"Apply"**

Render will create all three services automatically!

#### Option B: Manual

If automatic doesn't work, create services manually:

**Step 1: Create PostgreSQL Database**
1. Dashboard → **"New"** → **"PostgreSQL"**
2. Name: `snake-arena-db`
3. Database: `snake_arena`
4. User: `snake_arena_user`
5. Region: `Oregon` (or closest to you)
6. Plan: **Free**
7. Click **"Create Database"**

**Step 2: Create Backend Service**
1. Dashboard → **"New"** → **"Web Service"**
2. Connect your repository
3. Configure:
   - Name: `snake-arena-backend`
   - Region: `Oregon`
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `chmod +x ./render-build.sh && ./render-build.sh`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**

4. Add Environment Variables:
   ```
   PYTHON_VERSION=3.12.0
   DATABASE_URL=[Copy from PostgreSQL service]
   SECRET_KEY=[Generate with: openssl rand -hex 32]
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Advanced Settings:
   - Health Check Path: `/health`
   - Auto-Deploy: `Yes`

6. Click **"Create Web Service"**

**Step 3: Create Frontend Service**
1. Dashboard → **"New"** → **"Static Site"**
2. Connect your repository
3. Configure:
   - Name: `snake-arena-frontend`
   - Region: `Oregon`
   - Branch: `main`
   - Root Directory: `frontend`
   - Build Command: `chmod +x ./render-build.sh && ./render-build.sh`
   - Publish Directory: `dist`
   - Plan: **Free**

4. Add Environment Variables:
   ```
   NODE_VERSION=20.11.0
   VITE_API_BASE_URL=[Copy backend URL from step 2]
   ```

5. Add Rewrite Rule:
   - Source: `/*`
   - Destination: `/index.html`
   - Action: `Rewrite`

6. Click **"Create Static Site"**

### 4. Configure Environment Variables

#### Backend Environment Variables

Go to backend service → **Environment** tab:

```bash
# Required
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=your-generated-secret-key-min-32-chars

# Optional (with defaults)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PYTHON_VERSION=3.12.0
```

**Generate SECRET_KEY:**
```bash
openssl rand -hex 32
```

#### Frontend Environment Variables

Go to frontend service → **Environment** tab:

```bash
NODE_VERSION=20.11.0
VITE_API_BASE_URL=https://your-backend-name.onrender.com
```

### 5. Update CORS Settings

After deployment, update backend CORS to include your frontend URL:

1. Note your frontend URL: `https://your-frontend-name.onrender.com`
2. Backend already includes `https://*.onrender.com` in CORS
3. No changes needed if using `.onrender.com` domains

### 6. Verify Deployment

#### Check Backend
```bash
# Health check
curl https://your-backend-name.onrender.com/health

# API docs
open https://your-backend-name.onrender.com/docs
```

#### Check Frontend
```bash
open https://your-frontend-name.onrender.com
```

#### Test Full Flow
1. Visit frontend URL
2. Click "Sign Up" and create account
3. Login with credentials
4. Play the game
5. Submit score
6. Check leaderboard

## Environment Variables Reference

### Backend Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | JWT signing key (32+ chars) | `openssl rand -hex 32` |

### Backend Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiry time |
| `PYTHON_VERSION` | `3.12.0` | Python version |

### Frontend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `https://backend.onrender.com` |
| `NODE_VERSION` | Node.js version | `20.11.0` |

## Free Tier Limitations

### What You Get
✅ PostgreSQL database (1GB storage, 90-day expiry)
✅ Backend web service (750 hours/month)
✅ Frontend static site (100GB bandwidth/month)
✅ Automatic HTTPS
✅ Auto-deploy on git push

### Limitations
⚠️ Services sleep after 15 minutes of inactivity
⚠️ Cold start time: ~30 seconds
⚠️ PostgreSQL expires after 90 days (backup required)
⚠️ 750 hours/month = ~31 days (one service always on)

### Workarounds

**Keep Services Awake:**
```bash
# Use a cron job or service like UptimeRobot
# Ping every 10 minutes
*/10 * * * * curl https://your-backend.onrender.com/health
```

**Database Backup:**
```bash
# Backup before 90-day expiry
pg_dump $DATABASE_URL > backup.sql

# Restore to new database
psql $NEW_DATABASE_URL < backup.sql
```

## Troubleshooting

### Build Fails

**Issue**: Build command fails
```bash
# Check build logs in Render dashboard
# Common fixes:
1. Verify render-build.sh has execute permissions
2. Check Python/Node version compatibility
3. Review dependency installation logs
```

**Issue**: Migration fails
```bash
# Check DATABASE_URL is set correctly
# Verify database is accessible
# Check Alembic migration files
```

### Service Won't Start

**Issue**: Backend health check fails
```bash
# Check logs for errors
# Verify PORT environment variable is used
# Confirm health endpoint returns 200
```

**Issue**: Frontend shows blank page
```bash
# Check browser console for errors
# Verify VITE_API_BASE_URL is correct
# Check API CORS settings
```

### CORS Errors

**Issue**: Frontend can't connect to backend
```bash
# Verify backend CORS includes frontend URL
# Check browser console for exact error
# Ensure HTTPS is used (not HTTP)
```

### Database Connection Issues

**Issue**: Can't connect to database
```bash
# Verify DATABASE_URL format:
# postgresql://user:password@host:port/database

# Check database status in Render dashboard
# Verify database is in same region as backend
```

## Monitoring

### Health Checks

**Backend:**
```bash
curl https://your-backend.onrender.com/health
# Expected: {"status":"healthy"}
```

**Frontend:**
```bash
curl -I https://your-frontend.onrender.com
# Expected: HTTP/2 200
```

### Logs

View logs in Render dashboard:
1. Go to service
2. Click **"Logs"** tab
3. Filter by time range
4. Search for errors

### Metrics

Render provides:
- Request count
- Response times
- Error rates
- Bandwidth usage

Access via dashboard → service → **"Metrics"** tab

## Updating Deployment

### Automatic Updates

Push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push
```

Render auto-deploys on push!

### Manual Deploy

In Render dashboard:
1. Go to service
2. Click **"Manual Deploy"**
3. Select branch
4. Click **"Deploy"**

### Rollback

1. Go to service
2. Click **"Events"** tab
3. Find previous successful deploy
4. Click **"Rollback"**

## Custom Domain (Optional)

### Add Custom Domain

1. Go to frontend service
2. Click **"Settings"** → **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `yourdomain.com`
5. Add DNS records as shown
6. Wait for SSL certificate (automatic)

### DNS Configuration

Add these records to your DNS provider:

```
Type: CNAME
Name: www (or @)
Value: your-frontend.onrender.com
```

## Cost Optimization

### Free Tier Strategy

**For Testing:**
- Use all free tier services
- Accept cold starts
- Backup database monthly

**For Light Production:**
- Upgrade database to Starter ($7/month)
- Keep backend/frontend on free tier
- Use UptimeRobot to prevent sleep

**For Production:**
- Upgrade all to Starter tier ($21/month total)
- Always-on services
- No cold starts
- Persistent database

## Security Checklist

Before going live:

- [ ] Change default SECRET_KEY
- [ ] Use strong database password
- [ ] Enable HTTPS only (automatic on Render)
- [ ] Review CORS settings
- [ ] Set up database backups
- [ ] Configure rate limiting (if needed)
- [ ] Review environment variables
- [ ] Test authentication flow
- [ ] Verify API endpoints are secured

## Support

### Render Support
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Project Issues
- GitHub Issues: Your repository issues page
- Check logs in Render dashboard
- Review this documentation

## Next Steps

1. ✅ Deploy to Render
2. ✅ Verify all services are running
3. ✅ Test full application flow
4. 📊 Monitor performance
5. 🔄 Set up database backups
6. 🌐 (Optional) Add custom domain
7. 📈 (Optional) Upgrade to paid tier
