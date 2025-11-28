import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import GameBoard from '@/components/game/GameBoard';
import { useGameLoop } from '@/hooks/useGameLoop';
import { ActivePlayer, GameState } from '@/types/game';
import { createInitialState, getAIDirection } from '@/lib/gameLogic';
import api from '@/lib/api';
import { Eye, Users, ArrowLeft, Loader2 } from 'lucide-react';

const Spectate: React.FC = () => {
  const [activePlayers, setActivePlayers] = useState<ActivePlayer[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<ActivePlayer | null>(null);
  const [gameState, setGameState] = useState<GameState>(() => createInitialState('walls'));
  const [isLoading, setIsLoading] = useState(true);

  // AI-controlled game loop for spectator mode
  useGameLoop({ 
    gameState, 
    setGameState, 
    isSpectator: true,
    getAIDirection: getAIDirection
  });

  useEffect(() => {
    const fetchPlayers = async () => {
      setIsLoading(true);
      const players = await api.spectate.getActivePlayers();
      setActivePlayers(players);
      setIsLoading(false);
    };
    fetchPlayers();
  }, []);

  const handleSelectPlayer = (player: ActivePlayer) => {
    setSelectedPlayer(player);
    setGameState(createInitialState(player.mode));
  };

  const handleBackToList = () => {
    setSelectedPlayer(null);
  };

  // Auto-restart when game over in spectator mode
  useEffect(() => {
    if (selectedPlayer && gameState.isGameOver) {
      const timer = setTimeout(() => {
        setGameState(createInitialState(selectedPlayer.mode));
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [gameState.isGameOver, selectedPlayer]);

  if (selectedPlayer) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Button variant="ghost" onClick={handleBackToList} className="mb-6">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Players
        </Button>

        <div className="flex flex-col lg:flex-row gap-8 items-center lg:items-start animate-fade-in">
          <div className="relative">
            <div className="absolute -inset-4 bg-primary/5 rounded-xl blur-xl" />
            <GameBoard gameState={gameState} size={400} />
          </div>

          <Card className="w-64 neon-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="w-5 h-5 text-primary" />
                Watching
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-2xl font-bold">{selectedPlayer.username}</p>
                <Badge variant="secondary">{selectedPlayer.mode}</Badge>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Current Score</p>
                <p className="text-3xl font-bold text-primary neon-text">{gameState.score}</p>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                Live Game
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="text-center mb-8 animate-fade-in">
        <h1 className="text-4xl font-bold mb-2">
          <span className="text-primary neon-text">Spectate</span>
        </h1>
        <p className="text-muted-foreground">Watch other players live</p>
      </div>

      <Card className="neon-border animate-fade-in">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="w-5 h-5 text-primary" />
            Active Players
            <Badge variant="secondary">{activePlayers.length} online</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
          ) : activePlayers.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <Eye className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>No active players right now</p>
              <p className="text-sm">Check back later!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {activePlayers.map((player) => (
                <div
                  key={player.id}
                  className="flex items-center gap-4 p-4 rounded-lg bg-secondary/50 hover:bg-secondary transition-colors cursor-pointer"
                  onClick={() => handleSelectPlayer(player)}
                >
                  <div className="w-3 h-3 rounded-full bg-primary animate-pulse" />
                  <div className="flex-1">
                    <p className="font-medium">{player.username}</p>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="text-xs">
                        {player.mode}
                      </Badge>
                      <span className="text-xs text-muted-foreground">
                        Score: {player.score}
                      </span>
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    <Eye className="w-4 h-4 mr-1" />
                    Watch
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Spectate;
