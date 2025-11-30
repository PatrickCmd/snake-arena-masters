import React, { useState, useCallback, useEffect } from 'react';
import GameBoard from '@/components/game/GameBoard';
import GameControls from '@/components/game/GameControls';
import { useGameLoop } from '@/hooks/useGameLoop';
import { createInitialState } from '@/lib/gameLogic';
import { GameMode } from '@/types/game';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

const Index: React.FC = () => {
  const [mode, setMode] = useState<GameMode>('pass-through');
  const [gameState, setGameState] = useState(() => createInitialState(mode));
  const [bestScore, setBestScore] = useState<number | null>(null);
  const { isAuthenticated } = useAuth();
  const { toast } = useToast();

  useGameLoop({ gameState, setGameState });

  // Fetch best score when mode changes or user logs in
  useEffect(() => {
    const fetchBestScore = async () => {
      if (isAuthenticated) {
        const score = await api.leaderboard.getBestScore(mode);
        setBestScore(score);
      } else {
        setBestScore(null);
      }
    };
    fetchBestScore();
  }, [mode, isAuthenticated]);

  const handlePause = useCallback(() => {
    setGameState(prev => ({ ...prev, isPaused: !prev.isPaused }));
  }, []);

  const handleRestart = useCallback(async () => {
    // Submit score if authenticated and game is over
    if (isAuthenticated && gameState.isGameOver && gameState.score > 0) {
      console.log('Submitting score:', { score: gameState.score, mode: gameState.mode });

      try {
        const result = await api.leaderboard.submitScore(gameState.score, gameState.mode);
        console.log('Score submission result:', result);

        if (result.success) {
          // Update best score in state
          setBestScore(gameState.score);

          toast({
            title: '🎉 New Best Score!',
            description: `Score saved! You ranked #${result.rank} on the leaderboard!`,
          });
        } else {
          // Score was not saved (either not a new best or other error)
          console.error('Score submission failed:', result.error);

          // Check if it's because score wasn't high enough (has "best score" in message)
          const isNotBestScore = result.error && result.error.toLowerCase().includes('best score');

          toast({
            title: isNotBestScore ? '📊 Score Not Saved' : 'Score Submission Failed',
            description: result.error || 'Unable to submit score. Please try again.',
            variant: isNotBestScore ? 'default' : 'destructive',
          });
        }
      } catch (error) {
        console.error('Error submitting score:', error);
        toast({
          title: 'Error',
          description: 'An unexpected error occurred while submitting your score.',
          variant: 'destructive',
        });
      }
    } else {
      console.log('Score not submitted:', {
        isAuthenticated,
        isGameOver: gameState.isGameOver,
        score: gameState.score
      });

      // Show message if user is not authenticated
      if (!isAuthenticated && gameState.isGameOver && gameState.score > 0) {
        toast({
          title: 'Login Required',
          description: 'Please login to save your scores to the leaderboard.',
          variant: 'default',
        });
      }
    }
    setGameState(createInitialState(mode));
  }, [mode, isAuthenticated, gameState.isGameOver, gameState.score, gameState.mode, toast]);

  const handleModeChange = useCallback((newMode: GameMode) => {
    setMode(newMode);
    setGameState(createInitialState(newMode));
  }, []);

  return (
    <div className="min-h-[calc(100vh-140px)] flex items-center justify-center p-4">
      <div className="flex flex-col lg:flex-row gap-8 items-center lg:items-start animate-fade-in">
        <div className="relative">
          <div className="absolute -inset-4 bg-primary/5 rounded-xl blur-xl" />
          <GameBoard gameState={gameState} size={400} />
        </div>

        <div className="w-64">
          <GameControls
            score={gameState.score}
            bestScore={bestScore}
            mode={mode}
            isPaused={gameState.isPaused}
            isGameOver={gameState.isGameOver}
            onPause={handlePause}
            onRestart={handleRestart}
            onModeChange={handleModeChange}
          />
        </div>
      </div>
    </div>
  );
};

export default Index;
