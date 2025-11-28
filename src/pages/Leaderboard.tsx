import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { LeaderboardEntry, GameMode } from '@/types/game';
import api from '@/lib/api';
import { Trophy, Medal, Award, Loader2 } from 'lucide-react';

const Leaderboard: React.FC = () => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [mode, setMode] = useState<GameMode | 'all'>('all');

  useEffect(() => {
    const fetchLeaderboard = async () => {
      setIsLoading(true);
      const data = await api.leaderboard.getAll(mode === 'all' ? undefined : mode);
      setEntries(data);
      setIsLoading(false);
    };
    fetchLeaderboard();
  }, [mode]);

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Trophy className="w-5 h-5 text-yellow-500" />;
      case 2:
        return <Medal className="w-5 h-5 text-gray-400" />;
      case 3:
        return <Award className="w-5 h-5 text-amber-600" />;
      default:
        return <span className="w-5 text-center text-muted-foreground">{rank}</span>;
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="text-center mb-8 animate-fade-in">
        <h1 className="text-4xl font-bold mb-2">
          <span className="text-primary neon-text">Leaderboard</span>
        </h1>
        <p className="text-muted-foreground">Top snake players worldwide</p>
      </div>

      <Tabs defaultValue="all" className="animate-fade-in">
        <TabsList className="grid w-full grid-cols-3 mb-6">
          <TabsTrigger value="all" onClick={() => setMode('all')}>All Modes</TabsTrigger>
          <TabsTrigger value="pass-through" onClick={() => setMode('pass-through')}>Pass-Through</TabsTrigger>
          <TabsTrigger value="walls" onClick={() => setMode('walls')}>Walls</TabsTrigger>
        </TabsList>

        {['all', 'pass-through', 'walls'].map((tabValue) => (
          <TabsContent key={tabValue} value={tabValue}>
            <Card className="neon-border">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Trophy className="w-5 h-5 text-primary" />
                  Top Players
                </CardTitle>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                  </div>
                ) : (
                  <div className="space-y-2">
                    {entries.map((entry, index) => (
                      <div
                        key={entry.id}
                        className={`flex items-center gap-4 p-3 rounded-lg transition-colors ${
                          index < 3 ? 'bg-primary/10' : 'bg-secondary/50 hover:bg-secondary'
                        }`}
                      >
                        <div className="flex items-center justify-center w-8">
                          {getRankIcon(index + 1)}
                        </div>
                        <div className="flex-1">
                          <p className="font-medium">{entry.username}</p>
                          <p className="text-xs text-muted-foreground">{entry.date}</p>
                        </div>
                        <Badge variant={entry.mode === 'walls' ? 'default' : 'secondary'}>
                          {entry.mode}
                        </Badge>
                        <div className="text-right">
                          <p className="font-bold text-primary">{entry.score.toLocaleString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
};

export default Leaderboard;
