# Score Submission Debugging Guide

## Issue Report
User reported that scores are not being saved to the database when playing the game.

## Investigation Results

### Backend Status: ✅ WORKING
The backend API is functioning correctly:
- Score submission endpoint works as expected
- Scores are properly saved to the database
- Database transactions commit successfully

**Test Results:**
```bash
# Test performed with demo user
Login: ✅ Success
Submit Score (9999): ✅ Success (Rank #1)
Fetch Leaderboard: ✅ Success (score appears)
Database Verification: ✅ Score persisted
```

### Frontend Improvements Made

**Added to `frontend/src/pages/Index.tsx`:**
1. **Console Logging**: Added detailed logs for debugging
   - Logs when score submission is attempted
   - Logs the submission result
   - Logs why score was NOT submitted (if applicable)

2. **Error Handling**: Added try-catch block
   - Catches any unexpected errors
   - Shows user-friendly error messages

3. **Error Notifications**: Added toast notifications for failures
   - Shows specific error message from backend
   - Shows generic error for unexpected failures

## How to Debug

### Step 1: Open Browser Console
1. Open the game in your browser
2. Press `F12` to open Developer Tools
3. Go to the "Console" tab

### Step 2: Play and Check Logs
When you click "Restart" after game over, you should see:

**If authenticated and score > 0:**
```
Submitting score: { score: 1234, mode: "walls" }
Score submission result: { success: true, rank: 5 }
```

**If not authenticated:**
```
Score not submitted: { 
  isAuthenticated: false, 
  isGameOver: true, 
  score: 1234 
}
```

### Step 3: Common Issues

#### Issue: "Score not submitted" logged
**Cause**: User is not logged in
**Solution**: 
1. Click "Login" in the header
2. Use credentials: `demo@snake.game` / `demo123`
3. Play again

#### Issue: "Score submission failed" toast
**Cause**: Backend returned an error
**Solution**: Check the console for the specific error message

#### Issue: Network error
**Cause**: Backend server not running
**Solution**: 
```bash
cd backend
make run
```

## Verification Steps

1. **Start Backend**:
   ```bash
   cd backend
   make run
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Flow**:
   - Open `http://localhost:5173`
   - Login with `demo@snake.game` / `demo123`
   - Play the game until game over
   - Click "Restart"
   - Check console logs
   - Check if toast notification appears
   - Go to Leaderboard page to verify score

4. **Verify Database**:
   ```bash
   cd backend
   sqlite3 snake_arena.db "SELECT * FROM leaderboard ORDER BY created_at DESC LIMIT 5;"
   ```

## Expected Behavior

✅ **Correct Flow:**
1. User logs in
2. User plays game
3. Game ends (game over)
4. User clicks "Restart"
5. Console shows: "Submitting score: ..."
6. Toast shows: "Score Submitted! You ranked #X"
7. Score appears in leaderboard
8. Score is in database

## Notes

- Scores are only submitted when clicking "Restart" after game over
- User MUST be authenticated (logged in)
- Score must be greater than 0
- The score from the CURRENT game state is submitted (not a previous game)
