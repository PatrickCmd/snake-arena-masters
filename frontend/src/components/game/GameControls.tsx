import React from 'react';
import { Button } from '@/components/ui/button';
import { GameMode } from '@/types/game';
import { Play, Pause, RotateCcw } from 'lucide-react';

interface GameControlsProps {
  score: number;
  mode: GameMode;
  isPaused: boolean;
  isGameOver: boolean;
  onPause: () => void;
  onRestart: () => void;
  onModeChange: (mode: GameMode) => void;
}

const GameControls: React.FC<GameControlsProps> = ({
  score,
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
      <div className="text-center">
        <p className="text-sm text-muted-foreground uppercase tracking-wider">Score</p>
        <p className="text-4xl font-bold text-primary neon-text">{score}</p>
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
        <p>Use Arrow Keys or WASD to move</p>
        <p>Press Space to pause</p>
      </div>
    </div>
  );
};

export default GameControls;
