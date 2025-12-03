# CI/CD Quick Reference

## 🚀 Quick Setup (5 Minutes)

### 1. Get Render Deploy Hooks

**Backend:**
1. https://dashboard.render.com → `snake-arena-backend`
2. Settings → Deploy Hook → Copy URL

**Frontend:**
1. https://dashboard.render.com → `snake-arena-frontend`
2. Settings → Deploy Hook → Copy URL

### 2. Add GitHub Secrets

1. GitHub repo → Settings → Secrets → Actions
2. Add secrets:
   - `RENDER_DEPLOY_HOOK_BACKEND` = backend hook URL
   - `RENDER_DEPLOY_HOOK_FRONTEND` = frontend hook URL

### 3. Push to Main

```bash
git add .
git commit -m "Add CI/CD pipeline"
git push origin main
```

GitHub Actions will automatically run!

## 📊 Pipeline Flow

```
Push to main
    ↓
┌───────────────────────────┐
│   Run Tests (Parallel)    │
│  • Frontend Tests         │
│  • Backend Unit Tests     │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│ Backend Integration Tests │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│   Deploy to Render        │
│  • Backend Service        │
│  • Frontend Service       │
└───────────────────────────┘
```

## ⏱️ Timing

- Frontend tests: ~30s
- Backend unit tests: ~20s
- Backend integration tests: ~30s
- **Total test time**: ~1-2 min
- Deployment: ~3-5 min
- **Total pipeline**: ~4-7 min

## 🔍 Monitoring

### GitHub Actions
- Repo → **Actions** tab
- View workflow runs
- Check test results

### Render Deployment
- Dashboard → Service → Logs
- Monitor deployment progress

## ✅ What Runs When

### On Push to Main
- ✅ Frontend tests
- ✅ Backend unit tests
- ✅ Backend integration tests
- ✅ **Deploy to Render** (if tests pass)

### On Pull Request
- ✅ Frontend tests
- ✅ Backend unit tests
- ✅ Backend integration tests
- ❌ No deployment

### Manual Trigger
- Actions → CI/CD Pipeline → Run workflow

## 🚨 Troubleshooting

### Tests fail in CI
```bash
# Check logs in GitHub Actions
# Run tests locally:
cd frontend && npm test
cd backend && make test && make test-integration
```

### Deployment doesn't trigger
- ✅ Pushed to `main` branch?
- ✅ All tests passed?
- ✅ Deploy hooks in GitHub Secrets?

### Deploy hook error
1. Regenerate hook in Render
2. Update GitHub Secret
3. Try again

## 📚 Full Documentation

See [docs/ci-cd-setup.md](./ci-cd-setup.md) for complete guide.

## 🎯 Next Steps

1. Set up GitHub Secrets
2. Push to main
3. Watch pipeline run
4. Configure branch protection (optional)
