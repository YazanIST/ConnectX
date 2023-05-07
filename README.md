# ConnectX
This project is an AI agent to play connectX game (a generalization of the well known [Connect 4](https://en.wikipedia.org/wiki/Connect_Four) game).

It is based on [Kaggle](https://www.kaggle.com/) enviroments, and currently holds the rank 29-33 in [Connect X Simulation Competition](https://www.kaggle.com/competitions/connectx/leaderboard).

# The AI Agent
- Algorithm mainly used is minimax, minimax by itself can run into a depth = 3 at maximum.
- To speed-up the algorithm, I used alpha-beta pruning to get rid of usless branches (This made the algorithim run up to depth = 4)
- To speed-up the algorithm further more, I used memoization (Dynamic Programming) to avoid re-evaluating already evaluated position, which made the algorithm run into depth up to 5!
- The next step is to use reinforcement learning to improve the performance even more.

**Note**: To run the notebook you will need to install kaggle-environments module first with the following command `!pip install kaggle-environments>=0.1.6`
