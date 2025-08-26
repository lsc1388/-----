# AI Coding Agent Instructions - 敲磚塊遊戲 (Brick Breaker Game)

## Project Overview

This is a classic brick breaker game implemented in Python using Pygame. The project demonstrates clean modular architecture with clear separation of concerns across multiple modules.

## Architecture & Module Structure

### Core Module Pattern

The codebase follows a **config-driven, object-oriented architecture** with these key modules:

- **`config.py`** - Centralized constants and game parameters (colors, dimensions, speeds, timing)
- **`game_objects.py`** - Game entity classes (`Brick`, `Ball`, `Explosion`) with collision detection
- **`game_logic.py`** - Main game loop controller (`BrickBreakerGame` class)
- **`utils.py`** - Factory functions and helper utilities for object creation
- **`start_game.py`** - Clean entry point (use this, not `main.py`)

### Key Design Patterns

**Factory Pattern**: All game objects are created through factory functions in `utils.py`:

```python
# Always use these factories instead of direct instantiation
paddle = create_paddle()
balls = create_initial_balls(paddle)
bricks = create_bricks()
```

**State Management**: Game state is managed through the `BrickBreakerGame` class with clear lifecycle methods:

- `reset_game()` - Initialize/reset all game state
- `handle_events()` - Process input events
- `update_game_logic()` - Update game physics and state
- `render()` - Draw all game objects

## Development Workflows

### Running the Game

```bash
# Preferred entry point
python start_game.py

# Alternative (legacy)
python main.py
```

### Setup & Dependencies

```bash
pip install -r requirements.txt  # Only pygame==2.5.2 required
```

## Project-Specific Conventions

### Configuration-First Development

- **ALL magic numbers go in `config.py`** - never hardcode values in logic files
- Use ALL_CAPS constants: `WINDOW_WIDTH`, `BALL_SPEED`, `PADDLE_Y`
- Color tuples defined as constants: `RED = (255, 0, 0)`

### Chinese Documentation Standard

- **All docstrings and comments in Traditional Chinese**
- Method/variable names in English, documentation in Chinese
- Example: `def check_collision(self):  # 檢查碰撞`

### Collision Detection Pattern

Each game object implements its own collision methods:

```python
# Standard collision method signatures
ball.check_wall_collision(width, height)
ball.check_brick_collision(bricks)  # Returns hit brick for explosion
ball.check_paddle_collision(paddle)
```

### Multi-Ball System Architecture

- Balls stored in list, managed collectively in game loop
- Launch system: prepare batch → timed sequential launch
- Auto-generation: new balls added every `BALLS_ADD_INTERVAL` ms

## Critical Integration Points

### Game Object Lifecycle

1. **Creation**: Use factory functions from `utils.py`
2. **Update**: Objects update their own state (`ball.update()`)
3. **Collision**: Objects handle their own collision detection
4. **Rendering**: Objects render themselves (`obj.draw(surface)`)

### Explosion System

When modifying collision detection, remember:

```python
hit_brick = ball.check_brick_collision(self.bricks)
if hit_brick:
    # Create explosion at brick center
    explosion = Explosion(hit_brick.x + hit_brick.width/2,
                         hit_brick.y + hit_brick.height/2,
                         hit_brick.color)
```

### Event Handling Pattern

Input events are centralized in `BrickBreakerGame.handle_events()`:

- Space/Mouse → launch balls
- Arrow keys/WASD/Mouse → paddle control
- R key → restart, Q key → quit

## Common Pitfalls to Avoid

1. **Don't instantiate game objects directly** - use factory functions
2. **Don't hardcode coordinates/speeds** - use config constants
3. **Don't forget explosion effects** when adding new collision types
4. **Remember coordinate system**: Pygame uses top-left origin
5. **Ball physics**: Velocity reversal for collision response (`self.vx = -self.vx`)

## Testing & Debugging

- Use `python start_game.py` for testing changes
- Modify `config.py` values for quick gameplay tuning
- Add debug prints in `update_game_logic()` for state inspection
- Window automatically centers via `SDL_VIDEO_CENTERED` environment variable

## File Dependencies Map

```
start_game.py → game_logic.py → {game_objects.py, config.py, utils.py}
utils.py → {game_objects.py, config.py}
game_objects.py → config.py (colors only)
```
