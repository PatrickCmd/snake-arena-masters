# CI/CD Setup Guide

## Overview

This project uses GitHub Actions for continuous integration and deployment to Render.

## Workflow Overview

### Main CI/CD Workflow (`ci-cd.yml`)

**Triggers:**
- Push to `main` branch
- Pull requests to `main`
- Manual trigger via GitHub UI

**Jobs:**
1. **Frontend Tests** (parallel)
   - Install dependencies
   - Run unit tests
   - Build check

2. **Backend Unit Tests** (parallel)
   - Install dependencies with uv
   - Run pytest unit tests

3. **Backend Integration Tests** (sequential)
   - Depends on unit tests passing
   - Run pytest integration tests with SQLite

4. **Deploy to Render** (sequential)
   - Only runs on `main` branch pushes
   - Depends on all tests passing
   - Triggers Render deployments

### Test-Only Workflow (`test-only.yml`)

**Triggers:**
- Pull requests to any branch

**Jobs:**
- Runs all tests but skips deployment

## Setup Instructions

### 1. Get Render Deploy Hooks

#### Backend Deploy Hook
1. Go to https://dashboard.render.com
2. Select `snake-arena-backend` service
3. Go to **Settings** → **Deploy Hook**
4. Copy the deploy hook URL
5. It looks like: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`

#### Frontend Deploy Hook
1. Go to https://dashboard.render.com
2. Select `snake-arena-frontend` service
3. Go to **Settings** → **Deploy Hook**
4. Copy the deploy hook URL

### 2. Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these secrets:

**RENDER_DEPLOY_HOOK_BACKEND**
- Name: `RENDER_DEPLOY_HOOK_BACKEND`
- Value: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy` (backend hook)

**RENDER_DEPLOY_HOOK_FRONTEND**
- Name: `RENDER_DEPLOY_HOOK_FRONTEND`
- Value: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy` (frontend hook)

### 3. Test the Pipeline

#### Test on a Branch
```bash
# Create a test branch
git checkout -b test-ci-cd

# Make a small change
echo "# CI/CD Test" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin test-ci-cd
```

#### Check GitHub Actions
1. Go to your repository on GitHub
2. Click **Actions** tab
3. You should see the workflow running
4. Click on the workflow to see details

#### Create Pull Request
1. Create a PR from your test branch to `main`
2. GitHub will run tests automatically
3. You'll see test results in the PR

#### Merge to Main
1. Once tests pass, merge the PR
2. GitHub will run tests again
3. If tests pass, it will deploy to Render
4. Check Render dashboard for deployment progress

## Workflow Details

### Frontend Tests

**What it does:**
- Installs Node.js 20
- Installs npm dependencies
- Runs `npm test`
- Runs `npm run build` to verify build works

**Duration:** ~30 seconds

### Backend Unit Tests

**What it does:**
- Installs Python 3.12
- Installs uv package manager
- Installs dependencies with `uv sync`
- Runs `pytest tests/` (unit tests only)

**Duration:** ~20 seconds

### Backend Integration Tests

**What it does:**
- Runs after unit tests pass
- Uses in-memory SQLite database
- Runs `pytest tests_integration/`
- Tests end-to-end functionality

**Duration:** ~30 seconds

### Deploy to Render

**What it does:**
- Only runs on `main` branch
- Triggers backend deployment via webhook
- Triggers frontend deployment via webhook
- Deployments happen in parallel on Render

**Duration:** 3-5 minutes (on Render side)

## Understanding the Pipeline

### Parallel vs Sequential

**Parallel Jobs:**
```
Frontend Tests ─┐
                ├─→ Integration Tests → Deploy
Backend Tests ──┘
```

- Frontend and backend unit tests run simultaneously
- Integration tests wait for unit tests
- Deployment waits for all tests

### Deployment Conditions

Deployment only happens when:
- ✅ All tests pass
- ✅ Push is to `main` branch
- ✅ Event is a `push` (not PR)

### Manual Deployment

You can manually trigger the workflow:
1. Go to **Actions** tab
2. Select **CI/CD Pipeline**
3. Click **Run workflow**
4. Select branch
5. Click **Run workflow**

## Monitoring

### GitHub Actions

**View Workflow Runs:**
1. Repository → **Actions** tab
2. Click on a workflow run
3. View job details and logs

**Check Test Results:**
- Green checkmark = passed
- Red X = failed
- Yellow circle = running

### Render Deployment

**Monitor Deployment:**
1. Go to Render dashboard
2. Select service
3. View **Logs** tab
4. Check deployment progress

**Verify Deployment:**
```bash
# Check backend
curl https://snake-arena-backend.onrender.com/health

# Check frontend
curl https://snake-arena-frontend.onrender.com
```

## Troubleshooting

### Tests Fail in CI but Pass Locally

**Common causes:**
- Environment differences
- Missing environment variables
- Dependency version mismatches

**Solutions:**
1. Check GitHub Actions logs
2. Ensure all dependencies are in `package.json` / `pyproject.toml`
3. Test with same Node/Python versions locally

### Deployment Doesn't Trigger

**Check:**
- Are you pushing to `main` branch?
- Did all tests pass?
- Are deploy hooks configured in GitHub Secrets?

**Verify:**
```bash
# Check current branch
git branch

# Check GitHub Secrets are set
# Go to Settings → Secrets → Actions
```

### Deploy Hook Returns Error

**Possible issues:**
- Invalid deploy hook URL
- Service doesn't exist
- Render API issues

**Solutions:**
1. Regenerate deploy hook in Render
2. Update GitHub Secret
3. Check Render status page

### Tests Take Too Long

**Current durations:**
- Frontend: ~30s
- Backend unit: ~20s
- Backend integration: ~30s
- Total: ~1-2 minutes

**If slower:**
- Check GitHub Actions runner status
- Review test efficiency
- Consider caching dependencies

## Best Practices

### Branch Protection

Recommended settings for `main` branch:
1. Go to **Settings** → **Branches**
2. Add rule for `main`
3. Enable:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Select: frontend-tests, backend-unit-tests, backend-integration-tests

### Pull Request Workflow

1. Create feature branch
2. Make changes
3. Push and create PR
4. Wait for tests to pass
5. Request review
6. Merge to `main`
7. Automatic deployment

### Emergency Rollback

If deployment breaks production:

**Option 1: Revert commit**
```bash
git revert HEAD
git push origin main
```
CI/CD will deploy the reverted version

**Option 2: Manual rollback on Render**
1. Go to Render dashboard
2. Select service
3. **Events** → Find previous deploy
4. Click **Rollback**

## Workflow Files

### `.github/workflows/ci-cd.yml`
Main workflow with tests and deployment

### `.github/workflows/test-only.yml`
Test-only workflow for PRs

## Environment Variables

### GitHub Actions
- `NODE_VERSION`: 20
- `PYTHON_VERSION`: 3.12

### Secrets (Required)
- `RENDER_DEPLOY_HOOK_BACKEND`
- `RENDER_DEPLOY_HOOK_FRONTEND`

## Next Steps

1. ✅ Set up GitHub Secrets
2. ✅ Test the pipeline
3. 📊 Monitor first deployment
4. 🔒 Configure branch protection
5. 📈 Add code coverage (optional)

## Support

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Render Deploy Hooks**: https://render.com/docs/deploy-hooks
- **Project Issues**: GitHub Issues tab
