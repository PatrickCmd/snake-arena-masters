import { useEffect, useRef, useCallback } from 'react';
import { GameState, Direction } from '@/types/game';
import { moveSnake, changeDirection } from '@/lib/gameLogic';

interface UseGameLoopOptions {
  gameState: GameState;
  setGameState: React.Dispatch<React.SetStateAction<GameState>>;
  isSpectator?: boolean;
  getAIDirection?: (state: GameState) => Direction;
}

export const useGameLoop = ({ 
  gameState, 
  setGameState, 
  isSpectator = false,
  getAIDirection 
}: UseGameLoopOptions) => {
  const gameLoopRef = useRef<number>();
  const lastMoveRef = useRef<number>(0);

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (isSpectator) return;
    
    const keyDirectionMap: Record<string, Direction> = {
      ArrowUp: 'UP',
      ArrowDown: 'DOWN',
      ArrowLeft: 'LEFT',
      ArrowRight: 'RIGHT',
      KeyW: 'UP',
      KeyS: 'DOWN',
      KeyA: 'LEFT',
      KeyD: 'RIGHT',
    };

    const direction = keyDirectionMap[e.code];
    if (direction) {
      e.preventDefault();
      setGameState(prev => changeDirection(prev, direction));
    }

    if (e.code === 'Space') {
      e.preventDefault();
      setGameState(prev => ({ ...prev, isPaused: !prev.isPaused }));
    }
  }, [setGameState, isSpectator]);

  useEffect(() => {
    if (!isSpectator) {
      window.addEventListener('keydown', handleKeyDown);
      return () => window.removeEventListener('keydown', handleKeyDown);
    }
  }, [handleKeyDown, isSpectator]);

  useEffect(() => {
    const gameLoop = (timestamp: number) => {
      if (timestamp - lastMoveRef.current >= gameState.speed) {
        lastMoveRef.current = timestamp;
        
        setGameState(prev => {
          if (isSpectator && getAIDirection && !prev.isGameOver && !prev.isPaused) {
            const aiDirection = getAIDirection(prev);
            const updatedState = changeDirection(prev, aiDirection);
            return moveSnake(updatedState);
          }
          return moveSnake(prev);
        });
      }
      gameLoopRef.current = requestAnimationFrame(gameLoop);
    };

    if (!gameState.isGameOver && !gameState.isPaused) {
      gameLoopRef.current = requestAnimationFrame(gameLoop);
    }

    return () => {
      if (gameLoopRef.current) {
        cancelAnimationFrame(gameLoopRef.current);
      }
    };
  }, [gameState.isGameOver, gameState.isPaused, gameState.speed, setGameState, isSpectator, getAIDirection]);

  return { handleKeyDown };
};
