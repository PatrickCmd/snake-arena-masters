import { Direction, Position, GameState, GameMode } from '@/types/game';

export const GRID_SIZE = 20;
export const CELL_COUNT = 20;

export const createInitialState = (mode: GameMode): GameState => ({
  snake: [
    { x: 10, y: 10 },
    { x: 9, y: 10 },
    { x: 8, y: 10 },
  ],
  food: generateFood([{ x: 10, y: 10 }, { x: 9, y: 10 }, { x: 8, y: 10 }]),
  direction: 'RIGHT',
  score: 0,
  isGameOver: false,
  isPaused: false,
  mode,
  speed: 150,
});

export const generateFood = (snake: Position[]): Position => {
  let food: Position;
  do {
    food = {
      x: Math.floor(Math.random() * CELL_COUNT),
      y: Math.floor(Math.random() * CELL_COUNT),
    };
  } while (snake.some(segment => segment.x === food.x && segment.y === food.y));
  return food;
};

export const getNextHead = (head: Position, direction: Direction, mode: GameMode): Position => {
  let newHead: Position;
  
  switch (direction) {
    case 'UP':
      newHead = { x: head.x, y: head.y - 1 };
      break;
    case 'DOWN':
      newHead = { x: head.x, y: head.y + 1 };
      break;
    case 'LEFT':
      newHead = { x: head.x - 1, y: head.y };
      break;
    case 'RIGHT':
      newHead = { x: head.x + 1, y: head.y };
      break;
  }

  if (mode === 'pass-through') {
    if (newHead.x < 0) newHead.x = CELL_COUNT - 1;
    if (newHead.x >= CELL_COUNT) newHead.x = 0;
    if (newHead.y < 0) newHead.y = CELL_COUNT - 1;
    if (newHead.y >= CELL_COUNT) newHead.y = 0;
  }

  return newHead;
};

export const checkWallCollision = (head: Position): boolean => {
  return head.x < 0 || head.x >= CELL_COUNT || head.y < 0 || head.y >= CELL_COUNT;
};

export const checkSelfCollision = (head: Position, snake: Position[]): boolean => {
  return snake.slice(1).some(segment => segment.x === head.x && segment.y === head.y);
};

export const checkFoodCollision = (head: Position, food: Position): boolean => {
  return head.x === food.x && head.y === food.y;
};

export const getOppositeDirection = (direction: Direction): Direction => {
  const opposites: Record<Direction, Direction> = {
    UP: 'DOWN',
    DOWN: 'UP',
    LEFT: 'RIGHT',
    RIGHT: 'LEFT',
  };
  return opposites[direction];
};

export const isValidDirectionChange = (current: Direction, next: Direction): boolean => {
  return next !== getOppositeDirection(current);
};

export const moveSnake = (state: GameState): GameState => {
  if (state.isGameOver || state.isPaused) return state;

  const head = state.snake[0];
  const newHead = getNextHead(head, state.direction, state.mode);

  // Check wall collision in walls mode
  if (state.mode === 'walls' && checkWallCollision(newHead)) {
    return { ...state, isGameOver: true };
  }

  // Check self collision
  if (checkSelfCollision(newHead, state.snake)) {
    return { ...state, isGameOver: true };
  }

  const ateFood = checkFoodCollision(newHead, state.food);
  const newSnake = [newHead, ...state.snake];
  
  if (!ateFood) {
    newSnake.pop();
  }

  return {
    ...state,
    snake: newSnake,
    food: ateFood ? generateFood(newSnake) : state.food,
    score: ateFood ? state.score + 10 : state.score,
    speed: ateFood ? Math.max(50, state.speed - 2) : state.speed,
  };
};

export const changeDirection = (state: GameState, newDirection: Direction): GameState => {
  if (!isValidDirectionChange(state.direction, newDirection)) {
    return state;
  }
  return { ...state, direction: newDirection };
};

// AI logic for spectator mode
export const getAIDirection = (state: GameState): Direction => {
  const head = state.snake[0];
  const food = state.food;
  const possibleDirections: Direction[] = ['UP', 'DOWN', 'LEFT', 'RIGHT'];
  
  // Filter out invalid directions (opposite of current)
  const validDirections = possibleDirections.filter(
    dir => isValidDirectionChange(state.direction, dir)
  );

  // Filter out directions that would cause collision
  const safeDirections = validDirections.filter(dir => {
    const nextHead = getNextHead(head, dir, state.mode);
    if (state.mode === 'walls' && checkWallCollision(nextHead)) return false;
    if (checkSelfCollision(nextHead, state.snake)) return false;
    return true;
  });

  if (safeDirections.length === 0) return state.direction;

  // Prioritize directions that move towards food
  const towardsFoodDirections = safeDirections.filter(dir => {
    const nextHead = getNextHead(head, dir, state.mode);
    const currentDist = Math.abs(head.x - food.x) + Math.abs(head.y - food.y);
    const nextDist = Math.abs(nextHead.x - food.x) + Math.abs(nextHead.y - food.y);
    return nextDist < currentDist;
  });

  if (towardsFoodDirections.length > 0) {
    return towardsFoodDirections[Math.floor(Math.random() * towardsFoodDirections.length)];
  }

  return safeDirections[Math.floor(Math.random() * safeDirections.length)];
};
