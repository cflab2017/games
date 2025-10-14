# Snake Online

## Game Description
Snake Online is a multiplayer online game based on the classic Snake game. Players control their own snake, moving it across a game grid to eat food and grow. The objective is to survive the longest or reach a specific target length without colliding with other players' snakes or your own body.

## Game Features
*   **Multiplayer:** Multiple players can enjoy the game simultaneously in one room.
*   **Lobby System:** Log in with a username, create new game rooms, or join existing ones.
*   **Growth and Scoring:** Eating food increases the snake's length, and the snake's length is its score.
*   **Collision Detection:** Colliding with your own body or other snakes results in a game over.
*   **Wall Wrapping:** When the snake reaches the edge of the screen, it reappears on the opposite side.
*   **Win Condition:** The player who first reaches the set target length or is the last one remaining wins.
*   **Sound Effects:** Sound effects are played for movement and collisions.
*   **UI Panel:** A UI panel is provided during the game to visually display players' scores and snake lengths.

## Game Rules
1.  **Login:** Before starting the game, you must log in by entering a username.
2.  **Join/Create Room:** In the lobby, you can join an existing game room or create a new one.
3.  **Snake Control:** Use the keyboard arrow keys (or WASD keys) to change the snake's movement direction.
    *   `W` or `↑`: Move Up
    *   `A` or `←`: Move Left
    *   `S` or `↓`: Move Down
    *   `D` or `→`: Move Right
4.  **Eat Food:** Eating food that appears on the grid will increase the snake's length.
5.  **Avoid Collisions:** You lose the game if your snake's body collides with itself or with another player's snake.
6.  **Winning:**
    *   The player who first reaches the target length (`WIN_LENGTH`) wins.
    *   The player who is the last one remaining after all other players are game over wins.
7.  **After Game Over:** After the game over screen, you can click the 'Back to Lobby' button to return to the lobby.

## How to Get Started
1.  **Run Server:** Navigate to the `server` folder and run the `run.bat` file to start the game server.
2.  **Run Client:** Navigate to the `client` folder and run the `run.bat` file to start the game client.
3.  **Login:** In the client window, enter your username and log in.
4.  **Select Room:** In the lobby, join a desired game room or create a new one to start playing.
