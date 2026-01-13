# Python Breakout Game

## 🎮 Game Description
This game is a Python version of the classic arcade game 'Breakout', developed using the Pygame library. The player's goal is to control a paddle at the bottom of the screen, bounce a ball, and destroy all the bricks at the top. It offers a more immersive experience with various items, a level system, and spectacular graphic effects.

## 🕹️ Controls
*   **Left Arrow (←):** Move paddle left
*   **Right Arrow (→):** Move paddle right
*   **Spacebar (Space):**
    *   Start game (from the start screen)
    *   Restart game after game over
    *   Fire bullets when bullet item is acquired

## ✨ Key Features
*   **Basic Gameplay:** Classic Breakout mechanics with paddle, ball, and bricks.
*   **Scoring System:** Earn points by destroying bricks.
*   **Life System:** Lose a life when the ball falls off the bottom of the screen; game over when lives reach 0.
*   **Level System:** Progress to the next level after destroying all bricks, increasing ball speed and generating a new brick layout.
*   **Item System:**
    *   **Life Item:** Gain 1 life upon collection.
    *   **Bullet Item:** Gain 5 bullets upon collection, can be fired with the spacebar to destroy bricks.
*   **Object-Oriented Design:** Each element like `Game`, `Paddle`, `Ball`, `Brick` is implemented as a class for easy maintenance and extensibility.
*   **Optimization:** Smooth gameplay with a fixed 60 FPS.

## 💥 Effects
*   **Gradient Background:** Visually smooth background effect.
*   **3D Depth:** Simple 3D shading effect applied to the paddle, ball, and bricks.
*   **Collision Particles:** Spectacular particle effects upon collision of ball with bricks, ball with paddle, and bullet with bricks.
*   **Ball Trail:** Visual trail effect following the ball's movement path.
*   **Bottom Border Effect:** Visual feedback where the bottom border turns red when the ball goes off-screen.
*   **Sound Effects:** Appropriate sounds for brick destruction, paddle hits, bullet firing, and item collection.
*   **Virtual Keyboard Display:** A virtual keyboard displayed on the right side of the game screen, visually showing currently pressed keys.

## 📁 File Structure
```
.
├── game.py             # Main executable file for the game
├── gemini.md           # Conversation history and instructions with Gemini AI
├── history.md          # Project development history
├── narration.md        # Narration/subtitles for YouTube Shorts
├── readme_kr.md        # Korean README
├── readme_en.md        # (Current file) English README
├── assets/             # Resources used in the game, such as images and sounds
│   ├── brick_hit.wav
│   ├── bullet.wav
│   ├── item_collect.wav
│   └── paddle_hit.wav
└── src/                # Class files that constitute the game logic
    ├── ball.py         # Ball class
    ├── brick.py        # Brick class
    ├── bullet.py       # Bullet class
    ├── game.py         # Game class (main logic) managing the overall game
    ├── item.py         # Item class
    ├── keyboard.py     # Virtual Keyboard class
    ├── paddle.py       # Paddle class
    └── particle.py     # Particle class
```

## 📄 File Descriptions
*   **`game.py` (Root):** The entry point file that instantiates and runs the `Game` class from `src/game.py`.
*   **`src/game.py`:** Contains the `Game` class, which handles the overall game flow, initialization, game loop, collision detection, score/life/level management, item and bullet logic, and other core game logic.
*   **`src/paddle.py`:** Defines the `Paddle` class, which includes properties (size, color, speed) and behaviors (movement, drawing) of the player-controlled paddle.
*   **`src/ball.py`:** Defines the `Ball` class, which includes properties (radius, color, speed) and behaviors (movement, wall/paddle collision handling, drawing, trail effect) of the game ball.
*   **`src/brick.py`:** Defines the `Brick` class, which includes properties (position, size, color) and drawing (including 3D effect) of the in-game bricks.
*   **`src/item.py`:** Defines the `Item` class, which includes properties and behaviors of items (life, bullet) dropped when bricks are destroyed.
*   **`src/bullet.py`:** Defines the `Bullet` class, which includes properties and behaviors of bullets fired after acquiring a bullet item.
*   **`src/particle.py`:** Defines the `Particle` class, which includes properties and behaviors of particles for collision and other visual effects.
*   **`src/keyboard.py`:** Defines the `Keyboard` class, which displays a virtual keyboard on the screen and handles key input events.
*   **`assets/`:** This folder stores all sound files (`brick_hit.wav`, `bullet.wav`, `item_collect.wav`, `paddle_hit.wav`) used in the game.
