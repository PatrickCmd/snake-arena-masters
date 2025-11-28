import { describe, it, expect } from 'vitest';
import {
  createInitialState,
  generateFood,
  getNextHead,
  checkWallCollision,
  checkSelfCollision,
  checkFoodCollision,
  isValidDirectionChange,
  moveSnake,
  changeDirection,
  getAIDirection,
  CELL_COUNT,
} from './gameLogic';
import { Position, Direction, GameState } from '@/types/game';

describe('createInitialState', () => {
  it('should create initial state with pass-through mode', () => {
    const state = createInitialState('pass-through');
    expect(state.mode).toBe('pass-through');
    expect(state.snake.length).toBe(3);
    expect(state.direction).toBe('RIGHT');
    expect(state.score).toBe(0);
    expect(state.isGameOver).toBe(false);
    expect(state.isPaused).toBe(false);
  });

  it('should create initial state with walls mode', () => {
    const state = createInitialState('walls');
    expect(state.mode).toBe('walls');
  });
});

describe('generateFood', () => {
  it('should generate food not on snake', () => {
    const snake: Position[] = [{ x: 10, y: 10 }, { x: 9, y: 10 }];
    const food = generateFood(snake);
    expect(snake.some(s => s.x === food.x && s.y === food.y)).toBe(false);
  });

  it('should generate food within grid bounds', () => {
    const snake: Position[] = [{ x: 0, y: 0 }];
    const food = generateFood(snake);
    expect(food.x).toBeGreaterThanOrEqual(0);
    expect(food.x).toBeLessThan(CELL_COUNT);
    expect(food.y).toBeGreaterThanOrEqual(0);
    expect(food.y).toBeLessThan(CELL_COUNT);
  });
});

describe('getNextHead', () => {
  it('should move UP correctly', () => {
    const head: Position = { x: 10, y: 10 };
    const next = getNextHead(head, 'UP', 'walls');
    expect(next).toEqual({ x: 10, y: 9 });
  });

  it('should move DOWN correctly', () => {
    const head: Position = { x: 10, y: 10 };
    const next = getNextHead(head, 'DOWN', 'walls');
    expect(next).toEqual({ x: 10, y: 11 });
  });

  it('should move LEFT correctly', () => {
    const head: Position = { x: 10, y: 10 };
    const next = getNextHead(head, 'LEFT', 'walls');
    expect(next).toEqual({ x: 9, y: 10 });
  });

  it('should move RIGHT correctly', () => {
    const head: Position = { x: 10, y: 10 };
    const next = getNextHead(head, 'RIGHT', 'walls');
    expect(next).toEqual({ x: 11, y: 10 });
  });

  it('should wrap around in pass-through mode (left edge)', () => {
    const head: Position = { x: 0, y: 10 };
    const next = getNextHead(head, 'LEFT', 'pass-through');
    expect(next).toEqual({ x: CELL_COUNT - 1, y: 10 });
  });

  it('should wrap around in pass-through mode (right edge)', () => {
    const head: Position = { x: CELL_COUNT - 1, y: 10 };
    const next = getNextHead(head, 'RIGHT', 'pass-through');
    expect(next).toEqual({ x: 0, y: 10 });
  });

  it('should wrap around in pass-through mode (top edge)', () => {
    const head: Position = { x: 10, y: 0 };
    const next = getNextHead(head, 'UP', 'pass-through');
    expect(next).toEqual({ x: 10, y: CELL_COUNT - 1 });
  });

  it('should wrap around in pass-through mode (bottom edge)', () => {
    const head: Position = { x: 10, y: CELL_COUNT - 1 };
    const next = getNextHead(head, 'DOWN', 'pass-through');
    expect(next).toEqual({ x: 10, y: 0 });
  });

  it('should NOT wrap in walls mode', () => {
    const head: Position = { x: 0, y: 10 };
    const next = getNextHead(head, 'LEFT', 'walls');
    expect(next).toEqual({ x: -1, y: 10 });
  });
});

describe('checkWallCollision', () => {
  it('should detect left wall collision', () => {
    expect(checkWallCollision({ x: -1, y: 10 })).toBe(true);
  });

  it('should detect right wall collision', () => {
    expect(checkWallCollision({ x: CELL_COUNT, y: 10 })).toBe(true);
  });

  it('should detect top wall collision', () => {
    expect(checkWallCollision({ x: 10, y: -1 })).toBe(true);
  });

  it('should detect bottom wall collision', () => {
    expect(checkWallCollision({ x: 10, y: CELL_COUNT })).toBe(true);
  });

  it('should return false for valid position', () => {
    expect(checkWallCollision({ x: 10, y: 10 })).toBe(false);
  });
});

describe('checkSelfCollision', () => {
  it('should detect self collision', () => {
    const snake: Position[] = [
      { x: 10, y: 10 },
      { x: 9, y: 10 },
      { x: 8, y: 10 },
      { x: 8, y: 9 },
      { x: 9, y: 9 },
      { x: 10, y: 9 },
    ];
    expect(checkSelfCollision({ x: 9, y: 10 }, snake)).toBe(true);
  });

  it('should not detect collision with head (self)', () => {
    const snake: Position[] = [
      { x: 10, y: 10 },
      { x: 9, y: 10 },
    ];
    expect(checkSelfCollision({ x: 10, y: 10 }, snake)).toBe(false);
  });

  it('should return false when no collision', () => {
    const snake: Position[] = [
      { x: 10, y: 10 },
      { x: 9, y: 10 },
    ];
    expect(checkSelfCollision({ x: 11, y: 10 }, snake)).toBe(false);
  });
});

describe('checkFoodCollision', () => {
  it('should detect food collision', () => {
    expect(checkFoodCollision({ x: 5, y: 5 }, { x: 5, y: 5 })).toBe(true);
  });

  it('should return false when no collision', () => {
    expect(checkFoodCollision({ x: 5, y: 5 }, { x: 6, y: 5 })).toBe(false);
  });
});

describe('isValidDirectionChange', () => {
  it('should allow perpendicular direction change', () => {
    expect(isValidDirectionChange('UP', 'LEFT')).toBe(true);
    expect(isValidDirectionChange('UP', 'RIGHT')).toBe(true);
    expect(isValidDirectionChange('LEFT', 'UP')).toBe(true);
    expect(isValidDirectionChange('LEFT', 'DOWN')).toBe(true);
  });

  it('should not allow opposite direction change', () => {
    expect(isValidDirectionChange('UP', 'DOWN')).toBe(false);
    expect(isValidDirectionChange('DOWN', 'UP')).toBe(false);
    expect(isValidDirectionChange('LEFT', 'RIGHT')).toBe(false);
    expect(isValidDirectionChange('RIGHT', 'LEFT')).toBe(false);
  });
});

describe('moveSnake', () => {
  it('should move snake forward', () => {
    const state = createInitialState('walls');
    const newState = moveSnake(state);
    expect(newState.snake[0].x).toBe(state.snake[0].x + 1);
  });

  it('should not move when paused', () => {
    const state = { ...createInitialState('walls'), isPaused: true };
    const newState = moveSnake(state);
    expect(newState).toEqual(state);
  });

  it('should not move when game over', () => {
    const state = { ...createInitialState('walls'), isGameOver: true };
    const newState = moveSnake(state);
    expect(newState).toEqual(state);
  });

  it('should grow snake when eating food', () => {
    const state = createInitialState('walls');
    state.food = { x: state.snake[0].x + 1, y: state.snake[0].y };
    const newState = moveSnake(state);
    expect(newState.snake.length).toBe(state.snake.length + 1);
    expect(newState.score).toBe(state.score + 10);
  });

  it('should end game on wall collision in walls mode', () => {
    const state = createInitialState('walls');
    state.snake[0] = { x: CELL_COUNT - 1, y: 10 };
    state.direction = 'RIGHT';
    const newState = moveSnake(state);
    expect(newState.isGameOver).toBe(true);
  });

  it('should not end game on wall collision in pass-through mode', () => {
    const state = createInitialState('pass-through');
    state.snake[0] = { x: CELL_COUNT - 1, y: 10 };
    state.direction = 'RIGHT';
    const newState = moveSnake(state);
    expect(newState.isGameOver).toBe(false);
    expect(newState.snake[0].x).toBe(0);
  });
});

describe('changeDirection', () => {
  it('should change to valid direction', () => {
    const state = createInitialState('walls');
    const newState = changeDirection(state, 'UP');
    expect(newState.direction).toBe('UP');
  });

  it('should not change to opposite direction', () => {
    const state = createInitialState('walls');
    state.direction = 'RIGHT';
    const newState = changeDirection(state, 'LEFT');
    expect(newState.direction).toBe('RIGHT');
  });
});

describe('getAIDirection', () => {
  it('should return a valid direction', () => {
    const state = createInitialState('walls');
    const direction = getAIDirection(state);
    const validDirections: Direction[] = ['UP', 'DOWN', 'LEFT', 'RIGHT'];
    expect(validDirections).toContain(direction);
  });

  it('should not return opposite direction', () => {
    const state = createInitialState('walls');
    state.direction = 'RIGHT';
    const direction = getAIDirection(state);
    expect(direction).not.toBe('LEFT');
  });
});
