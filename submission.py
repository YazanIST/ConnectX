def my_agent(obs, config):
    import numpy as np
    import random
    import sys
    
    SEARCH_DEPTH = 5
    MOD = int(1e9) + 7
    memo = {}
    freq = {}
    
    def add_undermod(a, b):
        return (a + b) % MOD
    
    def hash_board(board, config):
        index = 0
        ret = 0
        for row in range(config.rows):
            for col in range(config.columns):
                if board[row][col] == 1:
                    ret = add_undermod(ret, pow(5, index, MOD))
                elif board[row][col] == 2:
                    ret = add_undermod(ret, pow(13, index, MOD))
                index += 1
        return ret
                    
    def get_next_board(board, col, mark, config):
        next_board = board.copy()
        for row in range(config.rows - 1, -1, -1):
            if next_board[row][col] == 0:
                next_board[row][col] = mark
                return next_board
        assert False, "The given move is invalid, the column is full!"
    
    def check_window(window, disk_count, mark, config):
        return window.count(mark) == disk_count and window.count(0) == config.inarow - disk_count
    
    def count_horizontal(board, disk_count, mark, config):
        ret = 0
        for row in range(config.rows):
            for col in range(config.columns - config.inarow + 1):
                window = list(board[row, col : col + config.inarow])
                if check_window(window, disk_count, mark, config):
                    ret += 1
        return ret
    
    def count_vertical(board, disk_count, mark, config):
        ret = 0
        for row in range(config.rows - config.inarow + 1):
            for col in range(config.columns):
                window = list(board[row : row + config.inarow, col])
                if check_window(window, disk_count, mark, config):
                    ret += 1
        return ret
    
    def count_diagonal(board, disk_count, mark, config):
        ret = 0
        for row in range(config.rows - config.inarow + 1):
            for col in range(config.columns - config.inarow + 1):
                window = list(board[range(row, row + config.inarow), range(col, col + config.inarow)])
                if check_window(window, disk_count, mark, config):
                    ret += 1
        return ret
    
    def count_antidiagonal(board, disk_count, mark, config):
        ret = 0
        for row in range(config.rows - config.inarow + 1):
            for col in range(config.columns - config.inarow + 1):
                window = list(board[range(row + config.inarow - 1, row - 1, -1), range(col, col + config.inarow)])
                if check_window(window, disk_count, mark, config):
                    ret += 1
        return ret
    
    def count_matches(board, disk_count, mark, config):
        return count_horizontal(board, disk_count, mark, config) + \
                count_vertical(board, disk_count, mark, config) + \
                count_diagonal(board, disk_count, mark, config) + \
                count_antidiagonal(board, disk_count, mark, config)
    
    def is_terminal(board, config):
        if list(board[0]).count(0) == 0:
            return True
        for mark in [1, 2]:
            if count_matches(board, config.inarow, mark, config) > 0:
                return True
        return False
    
    def evaluate(board, agent_mark, config):
        a = count_matches(board, 3, agent_mark, config)
        b = count_matches(board, 4, agent_mark, config)
        c = count_matches(board, 3, agent_mark % 2 + 1, config)
        d = count_matches(board, 4, agent_mark % 2 + 1, config)
#         original_stdout = sys.stdout
#         with open('debug.txt', 'a') as f:
#             sys.stdout = f
#             for y in board:
#                 for x in y:
#                     print(x, end = ' ')
#             print()
#             print(a, b, c, d)
#             sys.stdout = original_stdout
        return a + b * 1e6 - c * 1e2 - d * 1e4
    
    def minimax(board, depth, agent_mark, is_maximizing, alpha, beta, config):
        if depth == 0 or is_terminal(board, config):
            return evaluate(board, obs.mark, config)
        
        hash = hash_board(board, config)
        if hash in memo:
            freq[hash] += 1
            return memo[hash]
        
        valid_moves = [col for col in range(config.columns) if board[0][col] == 0]
        ret = 0
        if is_maximizing:
            ret = -np.Inf
            for col in valid_moves:
                next_board = get_next_board(board, col, agent_mark % 2 + 1, config)
                ret = max(ret, minimax(next_board, depth - 1, agent_mark, False, alpha, beta, config))
                if ret >= beta:
                    return ret
                alpha = max(alpha, ret)
        else:
            ret = np.Inf
            for col in valid_moves:
                next_board = get_next_board(board, col, agent_mark, config)
                ret = min(ret, minimax(next_board, depth - 1, agent_mark, True, alpha, beta, config))
                if alpha >= ret:
                    return ret
                beta = min(beta, ret)
        
        memo[hash] = ret
        freq[hash] = 1
        return ret
    
    # make sure about this method tmw
    def get_best_move(obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        board = np.asarray(obs.board).reshape(config.rows, config.columns)
        scores = [minimax(get_next_board(board, col, obs.mark, config), SEARCH_DEPTH - 1, obs.mark % 2 + 1, False, -1e18, 1e18, config) for col in valid_moves]
        max_score = max(scores)
        best_moves = [valid_moves[index] for index in range(len(valid_moves)) if scores[index] == max_score]
        dis = [abs(3 - index) for index in best_moves]
        minDis = min(dis)
        for i in range(len(best_moves)):
            if minDis == dis[i]:
                return best_moves[i]
#         return random.choice(best_moves)
    
    return get_best_move(obs, config)
