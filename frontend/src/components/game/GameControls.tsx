import React from 'react';
import { Button } from '@/components/ui/button';
import { GameMode } from '@/types/game';
import { Play, Pause, RotateCcw } from 'lucide-react';

interface GameControlsProps {
  score: number;
  bestScore: number | null;
  mode: GameMode;
  isPaused: boolean;
  isGameOver: boolean;
  onPause: () => void;
  onRestart: () => void;
  onModeChange: (mode: GameMode) => void;
}

const GameControls: React.FC<GameControlsProps> = ({
  score,
  bestScore,
  mode,
  isPaused,
  isGameOver,
  onPause,
  onRestart,
  onModeChange,
}) => {
  return (
    <div className="flex flex-col gap-4">
      {/* Score Display */}
      <div className="text-center space-y-2">
        <div>
          <p className="text-sm text-muted-foreground uppercase tracking-wider">Score</p>
          <p className="text-4xl font-bold text-primary neon-text">{score}</p>
        </div>
        {bestScore !== null && (
          <div className="pt-2 border-t border-border/50">
            <p className="text-xs text-muted-foreground uppercase tracking-wider">Best Score</p>
            <p className="text-2xl font-semibold text-primary/70">{bestScore}</p>
          </div>
        )}
      </div>

      {/* Mode Selection */}
      <div className="space-y-2">
        <p className="text-sm text-muted-foreground uppercase tracking-wider text-center">Mode</p>
        <div className="flex gap-2">
          <Button
            variant={mode === 'pass-through' ? 'default' : 'outline'}
            size="sm"
            onClick={() => onModeChange('pass-through')}
            className="flex-1"
            disabled={!isGameOver && !isPaused}
          >
            Pass-Through
          </Button>
          <Button
            variant={mode === 'walls' ? 'default' : 'outline'}
            size="sm"
            onClick={() => onModeChange('walls')}
            className="flex-1"
            disabled={!isGameOver && !isPaused}
          >
            Walls
          </Button>
        </div>
      </div>

      {/* Game Controls */}
      <div className="flex gap-2">
        <Button
          variant="outline"
          size="lg"
          onClick={onPause}
          className="flex-1"
          disabled={isGameOver}
        >
          {isPaused ? <Play className="w-5 h-5" /> : <Pause className="w-5 h-5" />}
        </Button>
        <Button
          variant="outline"
          size="lg"
          onClick={onRestart}
          className="flex-1"
        >
          <RotateCcw className="w-5 h-5" />
        </Button>
      </div>

      {/* Instructions */}
      <div className="text-center text-sm text-muted-foreground space-y-1">
        {isGameOver ? (
          <div className="space-y-2 p-3 bg-primary/5 rounded-lg border border-primary/20">
            <p className="text-primary font-semibold">Game Over!</p>
            <p className="text-xs">Click Restart to save your score</p>
            <p className="text-xs text-muted-foreground">(Login required to save scores)</p>
          </div>
        ) : (
          <>
            <p>Use Arrow Keys or WASD to move</p>
            <p>Press Space to pause</p>
          </>
        )}
      </div>
    </div>
  );
};

export default GameControls;
