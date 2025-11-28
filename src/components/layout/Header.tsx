import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { Gamepad2, Trophy, Eye, LogOut, User } from 'lucide-react';

const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Play', icon: Gamepad2 },
    { path: '/leaderboard', label: 'Leaderboard', icon: Trophy },
    { path: '/spectate', label: 'Watch', icon: Eye },
  ];

  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center neon-box">
            <Gamepad2 className="w-6 h-6 text-primary-foreground" />
          </div>
          <span className="text-xl font-bold text-foreground group-hover:text-primary transition-colors">
            Snake<span className="text-primary">Game</span>
          </span>
        </Link>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-1">
          {navItems.map(({ path, label, icon: Icon }) => (
            <Link key={path} to={path}>
              <Button
                variant={location.pathname === path ? 'default' : 'ghost'}
                size="sm"
                className="gap-2"
              >
                <Icon className="w-4 h-4" />
                {label}
              </Button>
            </Link>
          ))}
        </nav>

        {/* Auth Section */}
        <div className="flex items-center gap-2">
          {isAuthenticated ? (
            <>
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary">
                <User className="w-4 h-4 text-primary" />
                <span className="text-sm font-medium">{user?.username}</span>
              </div>
              <Button variant="ghost" size="sm" onClick={logout}>
                <LogOut className="w-4 h-4" />
              </Button>
            </>
          ) : (
            <Link to="/login">
              <Button variant="default" size="sm">
                Sign In
              </Button>
            </Link>
          )}
        </div>
      </div>

      {/* Mobile Navigation */}
      <nav className="md:hidden flex items-center justify-center gap-1 pb-3">
        {navItems.map(({ path, label, icon: Icon }) => (
          <Link key={path} to={path}>
            <Button
              variant={location.pathname === path ? 'default' : 'ghost'}
              size="sm"
              className="gap-1"
            >
              <Icon className="w-4 h-4" />
              {label}
            </Button>
          </Link>
        ))}
      </nav>
    </header>
  );
};

export default Header;
