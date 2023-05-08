# ConnectX
This project is an AI agent to play connectX game (a generalization of the well known [Connect 4](https://en.wikipedia.org/wiki/Connect_Four) game).

It is based on [Kaggle](https://www.kaggle.com/) enviroments, and currently holds the rank ~20 worldwide in [Connect X Simulation Competition](https://www.kaggle.com/competitions/connectx/leaderboard).

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
- Algorithm mainly used is minimax, minimax by itself can run into a depth = 3 at maximum.
- To speed-up the algorithm, I used alpha-beta pruning to get rid of usless branches (This made the algorithim run up to depth = 4)
- To speed-up the algorithm further more, I used memoization (Dynamic Programming) to avoid re-evaluating already evaluated position, which made the algorithm run into depth up to 5!
- The next step is to edit the heuristic function to get a better performance, then to use reinforcement learning to improve the performance even more.

# Heuristic Function (Evaluation)
For each board we need to evaluate, we check all windows of size `config.inarow` (which is the number of disks player needs to get in a row to win) and find the evaluation of the board as the following:
- $10 ^ 6$ points for each windown that is full of agent's disks (agent wins) (4 in the case of Connect 4).
- $1$ point for each window that is missing only one disk for agent to win (3 in the case of Connect 4).
- $-100$ points for each window that is missing only one disk for opposite player to win (3 in the case of Connect 4).
- $10 ^ 4$ points for each windown that is full of opposite player's disks (agent loses) (4 in the case of Connect 4).

The heuristic function needs more work, changing some values would probably improve the performance of the agent.

# Memoization (Dynamic Programming)
To avoid re-evaluating already evalutaed boards and positions, we use DP, which save the results for already evaluated boards, and to speed-up the process even more, we find a hash value for each board and store the evaluation for that board in a dictionary (Hash-Table) as a value for the hash used as a key value, so if we meet the same board again, we can simply check if it is already calculated, and if so, we return its value without re-evaluating it or going deeper in it's branch.

**Note**: To run the notebook you will need to install kaggle-environments module first with the following command `!pip install kaggle-environments>=0.1.6`
