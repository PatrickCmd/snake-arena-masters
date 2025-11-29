# 🐍 Snake Arena Masters

A modern, multiplayer snake game with real-time leaderboards, spectator mode, and competitive gameplay. Built with React + TypeScript frontend and FastAPI backend.

![Snake Arena Masters](https://img.shields.io/badge/Status-Active-success)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-96%25-brightgreen)

## 🎮 Features

- **Classic Snake Gameplay** - Two game modes: Pass-through and Walls
- **Multiplayer Leaderboards** - Compete globally and track high scores
- **Live Spectator Mode** - Watch other players in real-time
- **User Authentication** - Secure JWT-based authentication
- **Responsive Design** - Beautiful UI with smooth animations
- **Real-time Updates** - Live game state synchronization

## 📁 Project Structure

```
snake-arena-masters/
├── frontend/          # React + TypeScript frontend
├── backend/           # FastAPI backend
├── openapi.yaml       # API specification
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- **Frontend**: Node.js 18+ and npm
- **Backend**: Python 3.12+ and [uv](https://github.com/astral-sh/uv)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
cd backend
make install    # Install dependencies
make seed-info  # View demo credentials
make run        # Start server
```

The backend API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🎯 Demo Credentials

```bash
# View all demo users and mock data
cd backend && make seed-info
```

Quick login:
- Email: `demo@snake.game`
- Password: `demo123`

## 🏗️ Frontend

Built with modern web technologies for a smooth gaming experience.

### Tech Stack
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Tanstack Query** - Data fetching
- **Zustand** - State management

### Key Features
- Responsive game canvas with smooth animations
- Real-time score tracking
- Keyboard controls (Arrow keys, WASD)
- Pause/Resume functionality
- Game mode selection
- Leaderboard filtering

### Development

```bash
cd frontend
npm run dev        # Start dev server
npm test          # Run tests
npm run build     # Build for production
```

See [frontend/README.md](frontend/README.md) for detailed documentation.

## 🔧 Backend

Production-ready FastAPI backend with comprehensive testing.

### Tech Stack
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **JWT** - Authentication
- **Argon2** - Password hashing
- **pytest** - Testing (96% coverage)
- **ruff** - Linting and formatting

### API Endpoints

**Authentication**
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

**Leaderboard**
- `GET /api/v1/leaderboard` - Get leaderboard
- `POST /api/v1/leaderboard/scores` - Submit score

**Spectate**
- `GET /api/v1/spectate/players` - Get active players
- `GET /api/v1/spectate/players/{playerId}` - Get player game state

### Development

```bash
cd backend
make help          # Show all commands
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Check code quality
make format        # Format code
```

See [backend/README.md](backend/README.md) for detailed documentation.

## 📊 Testing

### Frontend Tests
```bash
cd frontend
npm test           # Run tests in watch mode
npm test -- run    # Run tests once
```

### Backend Tests
```bash
cd backend
make test          # Run all tests
make test-cov      # Run with coverage (96%)
```

## 🔒 Security

- **JWT Authentication** - Secure token-based auth
- **Argon2 Password Hashing** - Industry-standard password security
- **CORS Configuration** - Controlled cross-origin access
- **Input Validation** - Pydantic models ensure data integrity

## 📝 API Documentation

The backend provides interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Spec**: [openapi.yaml](openapi.yaml)

## 🛠️ Development Workflow

1. **Start Backend**:
   ```bash
   cd backend && make run
   ```

2. **Start Frontend**:
   ```bash
   cd frontend && npm run dev
   ```

3. **Run Tests**:
   ```bash
   # Backend
   cd backend && make test-cov
   
   # Frontend
   cd frontend && npm test
   ```

4. **Code Quality**:
   ```bash
   # Backend linting
   cd backend && make lint
   
   # Backend formatting
   cd backend && make format
   ```

## 🎨 Game Modes

### Pass-Through Mode
- Snake can pass through walls
- Appears on opposite side
- Easier for beginners

### Walls Mode
- Hitting walls ends the game
- More challenging
- Higher skill ceiling

## 📈 Future Enhancements

- [ ] Real-time multiplayer gameplay
- [ ] WebSocket support for live updates
- [ ] Persistent database (PostgreSQL/MongoDB)
- [ ] User profiles and statistics
- [ ] Achievement system
- [ ] Mobile app versions
- [ ] Tournament mode

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome!

## 📄 License

This project is part of the Snake Arena Masters game.

## 🙏 Acknowledgments

- Built with modern web technologies
- Inspired by classic Snake games
- Designed for competitive multiplayer gaming

---

**Happy Gaming! 🎮🐍**
