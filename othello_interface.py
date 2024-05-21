import json
import numpy as np
import time
import math

class Othello:
    B:int = -1
    W:int = 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    def __init__(self):
        self.board = np.matrix([[0 for i in range(8)] for j in range(8)])
        self.point_board1 = np.matrix([[500, -150, 30, 10, 10, 30, -150, 500], 
                            [-150, -250, 0, 0, 0, 0, -250, -150], 
                            [30, 0, 1, 2, 2, 1, 0, 30],
                            [10, 0, 2, 16, 16, 2, 0, 10],
                            [10, 0, 2, 16, 16, 2, 0, 10],
                            [30, 0, 1, 2, 2, 1, 0, 30],
                            [-150, -250, 0, 0, 0, 0, -250, -150], 
                            [500, -150, 30, 10, 10, 30, -150, 500]])
        self.point_board2 = np.matrix([[100, -20, 10, 5, 5, 10, -20, 100],
                            [-20, -50, -2, -2, -2, -2, -50, -20],
                            [10, -2, -1, -1, -1, -1, -2, 10],
                            [5, -2, -1, -1, -1, -1, -2, 5],
                            [5, -2, -1, -1, -1, -1, -2, 5],
                            [10, -2, -1, -1, -1, -1, -2, 10],
                            [-20, -50, -2, -2, -2, -2, -50, -20],
                            [100, -20, 10, 5, 5, 10, -20, 100]])
        self.current_player:int
        self.opponent:int
        self.shadow_pawn = []
        self.go:bool = False
        self.memorization = {}
    
    # initialisation of the game
    def initialisation(self):
        self.board = np.matrix([[0 for i in range(8)] for j in range(8)])
        self.board[3, 3], self.board[4, 4] = self.W, self.W
        self.board[3, 4], self.board[4, 3] = self.B, self.B
        self.current_player = self.B 
        self.opponent = self.W
        self.shadow_pawn = [[2,3], [3,2], [4,5], [5,4]]
        self.go = False
        self.memorization = {}
    
    # find the valid moves 
    def valid_moves(self):
        temp_pawn = np.where(self.board == self.current_player)
        pawn = list(zip(temp_pawn[0], temp_pawn[1]))
        for x, y in pawn:
            for dx, dy in self.directions:
                X, Y = x + dx, y + dy
                
                if X < 0 or X >= 8 or Y < 0 or Y >= 8:
                    continue

                if self.board.item(X, Y) == self.opponent:
                    while X + dx >= 0 and X + dx < 8 and Y + dy >= 0 and Y + dy < 8 and self.board.item(X, Y) == self.opponent:
                        X, Y = X + dx, Y + dy
                        if self.board.item(X, Y) == 0 and [X, Y] not in self.shadow_pawn:
                            self.shadow_pawn.append([X, Y])
                            break
                        if self.board.item(X, Y) == self.current_player:
                            break
    
    # flip the pawns            
    def flip_pawn(self, x, y):
        for dx, dy in self.directions:
            X, Y = x + dx, y + dy
            temp = [[x, y]]
            while X + dx >= 0 and X + dx < 8 and Y + dy >= 0 and Y + dy < 8 and self.board.item(X, Y) == self.opponent:
                temp.append([X, Y])
                X, Y = X + dx, Y + dy
                if self.board.item(X, Y) == self.current_player:
                    for i, j in temp:
                        self.board[i, j] = self.current_player
                    break
    
    # make a move
    def make_move(self, x, y):
        if [x, y] in self.shadow_pawn:
            self.flip_pawn(x, y)
            self.shadow_pawn.clear()
            self.current_player, self.opponent = self.opponent, self.current_player
            self.valid_moves()
            if len(self.shadow_pawn) == 0:
                self.current_player, self.opponent = self.opponent, self.current_player
                self.valid_moves()
                if len(self.shadow_pawn) == 0:
                    self.gameover()  
                return True 
            return False          

    # check if the game is over
    def gameover(self):
        self.go = True
        black = np.where(self.board == self.B)
        white = np.where(self.board == self.W)
        if len(black[0]) > len(white[0]):
            return self.B
        elif len(black[0]) < len(white[0]):
            return self.W
        else:
            return 0
    
    # copy the game
    def copy(self):
        new_game = Othello()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.opponent = self.opponent
        new_game.shadow_pawn = self.shadow_pawn.copy()
        new_game.go = self.go
        return new_game
    
    # count the difference of pawn between the two players
    def count_pawn(self):
        black = np.where(self.board == self.B)
        white = np.where(self.board == self.W)
        
        return len(white[0]) - len(black[0])
    
    # comparison with the tactical values matrix 1
    def compare_point_board1(self):
        black = np.where(self.board == self.B)
        white = np.where(self.board == self.W)
        black_score = np.sum(self.point_board1[black[0], black[1]])
        white_score = np.sum(self.point_board1[white[0], white[1]])
        
        return white_score - black_score
    
    # comparison with the tactical values matrix 2
    def compare_point_board2(self):
        black = np.where(self.board == self.B)
        white = np.where(self.board == self.W)
        black_score = np.sum(self.point_board2[black[0], black[1]])
        white_score = np.sum(self.point_board2[white[0], white[1]])
            
        return white_score - black_score
    
    # choice of the heuristic
    def heuristic_choice(self, heuristic):
        if heuristic == 0:
            return self.count_pawn()
        elif heuristic == 1:
            return self.compare_point_board1()
        else:
            return self.compare_point_board2()
    
    # minimax algorithm
    def minimax(self, depth, time_left, maximizingPlayer, heuristic):
        if depth == 0 or time_left < 0 or self.go:
            return self.heuristic_choice(heuristic), []
        
        time_begin = time.perf_counter()
        
        if maximizingPlayer:
            best_value = -math.inf
            best_move = []
            for x, y in self.shadow_pawn:
                sim_board = self.copy()
                again = sim_board.make_move(x, y)
                if again:
                    child_value,_ = sim_board.minimax(depth - 1, time_left - (time.perf_counter() - time_begin), True, heuristic)
                else:
                    child_value,_ = sim_board.minimax(depth - 1, time_left - (time.perf_counter() - time_begin), False, heuristic)
                if child_value > best_value:
                    best_value = child_value
                    best_move = [x, y] 
            return best_value, best_move
        
        else:
            best_value = math.inf
            best_move = []
            for x, y in self.shadow_pawn:
                sim_board = self.copy()
                again = sim_board.make_move(x, y)
                if again:
                    child_value,_ = sim_board.minimax(depth - 1, time_left - (time.perf_counter() - time_begin), False, heuristic)
                else:
                    child_value,_ = sim_board.minimax(depth - 1, time_left - (time.perf_counter() - time_begin), True, heuristic)
                if child_value < best_value:
                    best_value = child_value
                    best_move = [x, y]    
            return best_value, best_move

    # negamax algorithm
    def negamax(self, depth, time_left, color, heuristic):
        if depth == 0 or time_left < 0 or self.go:
            return self.heuristic_choice(heuristic) * color, []
        
        best_value = -math.inf
        time_begin = time.perf_counter()
        best_move = []
        
        for x, y in self.shadow_pawn:
            sim_board = self.copy()
            sim_board.make_move(x, y)
            child_value,_ = sim_board.negamax(depth - 1, time_left - (time.perf_counter() - time_begin), -color, heuristic)
            if -child_value > best_value:
                best_value = -child_value
                best_move = [x, y]

        return best_value, best_move
    
    # minimax algorithm with alpha beta pruning
    def alphabeta_minimax(self, depth, time_left, maximizingPlayer, heuristic, alpha, beta):
        if depth == 0 or time_left < 0 or self.go:
            return self.heuristic_choice(heuristic), []
        
        if maximizingPlayer:
            best_value = -math.inf
            best_move = []
            time_begin = time.perf_counter()
            for x, y in self.shadow_pawn:
                sim_board = self.copy()
                sim_board.make_move(x, y)
                child_value,_ = sim_board.alphabeta_minimax(depth - 1, time_left - (time.perf_counter() - time_begin), False, heuristic, alpha, beta)
                if child_value > best_value:
                    best_value = child_value
                    best_move = [x, y]
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move
        else:
            best_value = math.inf
            best_move = []
            time_begin = time.perf_counter()
            for x, y in self.shadow_pawn:
                sim_board = self.copy()
                sim_board.make_move(x, y)
                child_value,_ = sim_board.alphabeta_minimax(depth - 1, time_left - (time.perf_counter() - time_begin), True, heuristic, alpha, beta)
                if child_value < best_value:
                    best_value = child_value
                    best_move = [x, y]
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move

    # negamax algorithm with alpha beta pruning
    def alphabeta_negamax(self, depth, time_left, color, heuristic, alpha, beta):
        if depth == 0 or time_left < 0 or self.go:
            return self.heuristic_choice(heuristic), []
        
        best_value = -math.inf
        time_begin = time.perf_counter()
        best_move = []
        
        for x, y in self.shadow_pawn:
            sim_board = self.copy()
            sim_board.make_move(x, y)
            child_value,_ = sim_board.alphabeta_negamax(depth - 1, time_left - (time.perf_counter() - time_begin), -color, heuristic, -beta, -alpha)
            if -child_value > best_value:
                best_value = -child_value
                best_move = [x, y]
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

        return best_value, best_move
        
    # ai move
    def ai_move(self, color, method, heuristic, depth, time_left):
        debut = time.perf_counter()
        if (self.current_player == color * -1):
            return self.board
        if method == 0:
            _,best_move = self.minimax(depth*2, time_left, True, heuristic)
        elif method == 1:
            _,best_move = self.negamax(depth*2, time_left, 1, heuristic)
        elif method == 2:
            _,best_move = self.alphabeta_minimax(depth*2, time_left, True, heuristic, -math.inf, math.inf)
        else:
            _,best_move = self.alphabeta_negamax(depth*2, time_left, 1, heuristic, -math.inf, math.inf)
        
        best_x, best_y = best_move[0], best_move[1]
        self.make_move(best_x, best_y)
        return self.board_json()
    
    # random ai move
    def random_ai(self, color):
        time.sleep(0.1)
        if (self.current_player == (-color)):
            return self.board_json()
        x, y = self.shadow_pawn[np.random.randint(len(self.shadow_pawn))]
        self.make_move(x, y)
        return self.board_json()

    def interface_handler(self, id):
        if self.current_player == self.B:
            x, y = int(id[0]), int(id[1])
            self.make_move(x, y)
            return self.board_json()
        
    def board_json(self):
        id_N, id_B, id_n, id_b = [], [], [], []
        for i in range (len(self.board)):
            for j in range (len(self.board)):
                if self.board.item(i, j) == 0:
                    continue
                elif self.board.item(i, j) == -1:
                    id_N.append(str(i) + str(j))
                elif self.board.item(i, j) == 1:
                    id_B.append(str(i) + str(j))
        if self.current_player == -1:
            for x, y in self.shadow_pawn:
                id_n.append(str(x) + str(y))
        else :
            for x, y in self.shadow_pawn:
                id_b.append(str(x) + str(y))
    
        
        if self.current_player == self.B:
            json_current_player = 1
        else:
            json_current_player = 2
        
        json_datas = {
            "pion_noir": id_N,
            "pion_blanc" : id_B,
            "outline_pion_noir": id_n,
            "outline_pion_blanc": id_b,
            "gameover": self.go,
            "player": json_current_player        
        }
        
        return json.dumps(json_datas)