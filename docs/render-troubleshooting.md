# Render Deployment Troubleshooting

## Current Issue: Deployment Timeout

Build succeeds but deployment times out. Here's how to debug:

## Step 1: Check Render Logs

1. Go to Render Dashboard
2. Click on `snake-arena-backend` service
3. Click **"Logs"** tab
4. Look for:
   - `🚀 Snake Arena Masters API Starting...` (startup message)
   - `Application startup complete` (uvicorn message)
   - Any error messages

## Step 2: Common Issues & Solutions

### Issue 1: Port Binding
**Symptom:** App starts but Render can't connect

**Check logs for:**
```
Uvicorn running on http://0.0.0.0:XXXX
```

**Solution:** Ensure `$PORT` environment variable is used
- Already configured in `render.yaml`: `--port $PORT`

### Issue 2: Database Connection
**Symptom:** App crashes on startup

**Check logs for:**
```
sqlalchemy.exc.OperationalError
Connection refused
```

**Solution:** Verify `DATABASE_URL` is set correctly
- Check in Render Dashboard → Environment → `DATABASE_URL`
- Should start with `postgresql://`

### Issue 3: Missing Dependencies
**Symptom:** Import errors

**Check logs for:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Solution:** Rebuild with dependencies
- Already fixed: `psycopg2-binary` added

### Issue 4: Health Check Timeout
**Symptom:** App runs but deployment times out

**Solution:** Removed `healthCheckPath` from `render.yaml`
- Render will use default health check (HTTP 200 on any endpoint)

## Step 3: Manual Testing

Once deployed (even if timeout), test endpoints:

```bash
# Replace with your actual URL
BACKEND_URL="https://snake-arena-backend.onrender.com"

# Test root endpoint
curl $BACKEND_URL/

# Test health endpoint
curl $BACKEND_URL/health

# Test API docs
curl $BACKEND_URL/docs
```

## Step 4: Check Service Status

In Render Dashboard:
1. Go to service
2. Check **"Events"** tab for deployment history
3. Check **"Metrics"** tab for request/error rates

## Step 5: Force Redeploy

If needed:
1. Go to service settings
2. Click **"Manual Deploy"**
3. Select `main` branch
4. Click **"Deploy"**

## Expected Logs (Success)

```
==> Running 'uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT'
==================================================
🚀 Snake Arena Masters API Starting...
📊 Database URL: postgresql+asyncpg://...
🌐 CORS Origins: [...]
🔧 Port: 10000
==================================================
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
==> Your service is live 🎉
```

## Quick Fixes

### If database connection fails:
```bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:pass@host:port/db
```

### If port binding fails:
```bash
# Check PORT is set
echo $PORT
# Should be a number (usually 10000)
```

### If CORS errors:
- Already configured for `https://*.onrender.com`
- Frontend should work automatically

## Next Steps

1. Share the Render logs (last 50 lines)
2. Check if service shows as "Live" in dashboard
3. Try accessing the URL directly in browser
