import React from 'react';
import { GameState } from '@/types/game';
import { GRID_SIZE, CELL_COUNT } from '@/lib/gameLogic';

interface GameBoardProps {
  gameState: GameState;
  size?: number;
}

const GameBoard: React.FC<GameBoardProps> = ({ gameState, size = 400 }) => {
  const cellSize = size / CELL_COUNT;
  const { snake, food } = gameState;

  return (
    <div 
      className="relative neon-border rounded-lg overflow-hidden game-grid-bg"
      style={{ width: size, height: size }}
    >
      {/* Food */}
      <div
        className="absolute rounded-full bg-food animate-pulse-glow"
        style={{
          width: cellSize - 4,
          height: cellSize - 4,
          left: food.x * cellSize + 2,
          top: food.y * cellSize + 2,
          boxShadow: '0 0 10px hsl(var(--food-glow)), 0 0 20px hsl(var(--food-glow) / 0.5)',
        }}
      />
      
      {/* Snake */}
      {snake.map((segment, index) => (
        <div
          key={index}
          className="absolute rounded-sm transition-all duration-75"
          style={{
            width: cellSize - 2,
            height: cellSize - 2,
            left: segment.x * cellSize + 1,
            top: segment.y * cellSize + 1,
            backgroundColor: `hsl(var(--snake) / ${1 - index * 0.03})`,
            boxShadow: index === 0 
              ? '0 0 10px hsl(var(--snake-glow)), 0 0 20px hsl(var(--snake-glow) / 0.5)'
              : 'none',
          }}
        />
      ))}

      {/* Game Over Overlay */}
      {gameState.isGameOver && (
        <div className="absolute inset-0 bg-background/80 flex items-center justify-center">
          <div className="text-center animate-scale-in">
            <h2 className="text-3xl font-bold text-destructive mb-2">Game Over</h2>
            <p className="text-xl text-foreground">Score: {gameState.score}</p>
          </div>
        </div>
      )}

      {/* Paused Overlay */}
      {gameState.isPaused && !gameState.isGameOver && (
        <div className="absolute inset-0 bg-background/80 flex items-center justify-center">
          <div className="text-center animate-scale-in">
            <h2 className="text-3xl font-bold text-primary neon-text">Paused</h2>
            <p className="text-muted-foreground mt-2">Press Space to resume</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameBoard;
