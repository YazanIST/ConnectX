# ConnectX
This project is an AI agent to play connectX game (a generalization of the well-known [Connect 4](https://en.wikipedia.org/wiki/Connect_Four) game).

It is based on [Kaggle](https://www.kaggle.com/) environment, and currently holds the rank ~20 worldwide in [Connect X Simulation Competition](https://www.kaggle.com/competitions/connectx/leaderboard).

# About Environment
Parameters used are:
- obs:
  - obs.board - the game board (a Python list with one item for each grid location)
  - obs.mark - the piece assigned to the agent (either 1 or 2)
- config
  - config.columns - number of columns in the game board (7 for Connect Four)
  - config.rows - number of rows in the game board (6 for Connect Four)
  - config.inarow - number of pieces a player needs to get in a row in order to win (4 for Connect Four)

You can find more information and details [here](https://www.kaggle.com/code/alexisbcook/play-the-game)

# The AI Agent
- The algorithm mainly used is minimax, minimax by itself can run into a depth = 3 at maximum.
- To speed up the algorithm, I used alpha-beta pruning to get rid of useless branches (This made the algorithm run up to depth = 4)
- To speed up the algorithm furthermore, I used memoization (Dynamic Programming) to avoid re-evaluating already evaluated positions, which made the algorithm run into depth up to 5!
- When having more than one move with the same evaluation, the agent picks the move closer to the middle of the board, this detail actually gained me ~200 extra points in the [Connect X Simulation Competition](https://www.kaggle.com/competitions/connectx/leaderboard).
- The next step is to edit the heuristic function to get better performance, then use reinforcement learning to improve the performance even more.

# Heuristic Function (Evaluation)
For each board we need to evaluate, we check all windows of size `config.inarow` (which is the number of disks player needs to get in a row to win) and find the evaluation of the board as the following:
- $10 ^ 6$ points for each windown that is full of agent's disks (agent wins) (4 in the case of Connect 4).
- $1$ point for each window that is missing only one disk for agent to win (3 in the case of Connect 4).
- $-100$ points for each window that is missing only one disk for opposite player to win (3 in the case of Connect 4).
- $10 ^ 4$ points for each windown that is full of opposite player's disks (agent loses) (4 in the case of Connect 4).

The heuristic function needs more work, changing some values would probably improve the performance of the agent.

# Memoization (Dynamic Programming)
To avoid re-evaluating already evaluated boards and positions, we use DP, which saves the results for already evaluated boards, and to speed up the process even more, we find a hash value for each board and store the evaluation for that board in a dictionary (Hash-Table) as a value to the hash used as a key value, so if we meet the same board again, we can simply check if it has already been calculated, and if so, we return its value without re-evaluating it or going deeper in its branch.

# Hashing (Encoding boards / positions)
To use dynamic programming efficiently as described before, we need to find a hash value for each board that holds a very small probability of collisions, the hashing process was the following:
- First, we picked a prime modulus value to perform modular arithmetic operations and avoid having large hash values, the chosen value is $10 ^ 9 + 7$.
- initially, the hash for an empty grid is 0
- For each cell that contains a disk of the first player, we add the value $5 ^ {index}$, where index is the index of the disk's cell if we flatten the board into a 1D list.
- For each cell that contains a disk of the second player, we add the value $13 ^ {index}$, where index is the index of the disk's cell if we flatten the board into a 1D list.

**Notes**:
- We used values (5, 13) to represent the first and the second player's disks as small prime random numbers to avoid collision.
- Power and add operations are performed under mod ($mod = 10 ^ 9 + 7$).
- To find the index of a cell after flattening, $index = row \cdot rowsize + col$.

# Running The Notebook
To run the notebook you will need to install kaggle-environments module first with the following command `!pip install kaggle-environments>=0.1.6`
