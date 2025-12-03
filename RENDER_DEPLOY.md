# Render Deployment - Quick Reference

## 🚀 Quick Deploy (5 Minutes)

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Render configuration"
git push origin main
```

### 2. Deploy on Render
1. Go to https://dashboard.render.com
2. Click **"New"** → **"Blueprint"**
3. Connect repository: `snake-arena-masters`
4. Click **"Apply"**

### 3. Configure Environment Variables

**Backend** (snake-arena-backend):
```bash
SECRET_KEY=$(openssl rand -hex 32)  # Generate this!
```

**Frontend** (snake-arena-frontend):
```bash
VITE_API_BASE_URL=https://snake-arena-backend.onrender.com
```

### 4. Wait for Deployment
- Database: ~2 minutes
- Backend: ~5 minutes (first build)
- Frontend: ~3 minutes

### 5. Test
```bash
# Backend health
curl https://snake-arena-backend.onrender.com/health

# Frontend
open https://snake-arena-frontend.onrender.com
```

## 📋 Service URLs

After deployment, you'll have:
- **Frontend**: `https://snake-arena-frontend.onrender.com`
- **Backend**: `https://snake-arena-backend.onrender.com`
- **API Docs**: `https://snake-arena-backend.onrender.com/docs`
- **Database**: Internal URL (auto-configured)

## ⚙️ Environment Variables Checklist

### Backend (Required)
- [x] `DATABASE_URL` - Auto-set by Render
- [x] `SECRET_KEY` - **YOU MUST SET THIS!**

### Backend (Optional)
- [ ] `ALGORITHM` - Default: HS256
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` - Default: 30

### Frontend (Required)
- [x] `VITE_API_BASE_URL` - Set to backend URL

## 🔧 Common Issues

### Build Fails
```bash
# Check: render-build.sh has execute permissions
chmod +x backend/render-build.sh frontend/render-build.sh
git add . && git commit -m "Fix permissions" && git push
```

### CORS Errors
```bash
# Already configured! Backend accepts: https://*.onrender.com
# Just ensure frontend URL matches pattern
```

### Service Sleeps (Free Tier)
```bash
# Use UptimeRobot or similar to ping every 10 minutes
# Ping URL: https://snake-arena-backend.onrender.com/health
```

## 📊 Free Tier Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| Database | 1GB, 90 days | Backup before expiry! |
| Backend | 750 hrs/month | ~31 days if always on |
| Frontend | 100GB bandwidth | Usually sufficient |
| Cold Start | ~30 seconds | After 15min inactivity |

## 🔐 Security Checklist

Before going live:
- [ ] Generate unique `SECRET_KEY`
- [ ] Verify CORS settings
- [ ] Test authentication flow
- [ ] Set up database backups
- [ ] Review environment variables

## 📚 Full Documentation

See [docs/render-deployment.md](./render-deployment.md) for complete guide.

## 🆘 Need Help?

1. Check Render logs (Dashboard → Service → Logs)
2. Review [docs/render-deployment.md](./render-deployment.md)
3. Check Render status: https://status.render.com
