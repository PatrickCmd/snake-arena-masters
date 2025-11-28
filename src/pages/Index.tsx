import React, { useState, useCallback } from 'react';
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
  const { isAuthenticated } = useAuth();
  const { toast } = useToast();

  useGameLoop({ gameState, setGameState });

  const handlePause = useCallback(() => {
    setGameState(prev => ({ ...prev, isPaused: !prev.isPaused }));
  }, []);

  const handleRestart = useCallback(async () => {
    // Submit score if authenticated and game is over
    if (isAuthenticated && gameState.isGameOver && gameState.score > 0) {
      const result = await api.leaderboard.submitScore(gameState.score, gameState.mode);
      if (result.success) {
        toast({
          title: 'Score Submitted!',
          description: `You ranked #${result.rank} on the leaderboard!`,
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
