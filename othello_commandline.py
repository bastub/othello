import numpy as np
import time
import math
from itertools import zip_longest
from chart import method_result_to_chart, depth_result_to_chart, heuristic_result_to_chart, mixed_result_to_chart, memory_result_to_chart, method_alpha_beta_result_to_chart
import os

class Memorization:
        def __init__(self):
            self.table = {}

        def lookup(self, key):
            return self.table.get(str(key))

        def store(self, key, value, alpha, beta):
            self.table[key] = (value, alpha, beta)

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
        self.memorization = Memorization()
    
    # initialisation of the game
    def initialisation(self):
        self.board = np.matrix([[0 for i in range(8)] for j in range(8)])
        self.board[3, 3], self.board[4, 4] = self.W, self.W
        self.board[3, 4], self.board[4, 3] = self.B, self.B
        self.current_player = self.B 
        self.opponent = self.W
        self.shadow_pawn = [[2,3], [3,2], [4,5], [5,4]]
        self.go = False
        self.memorization = Memorization()
    
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
    
    # alpha-beta minimax algorithm
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

    # alpha-beta negamax algorithm
    def alphabeta_negamax(self, depth, time_left, color, heuristic, alpha, beta):
        if depth == 0 or time_left < 0 or self.go:
            return self.heuristic_choice(heuristic) * color, []
        
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
                if alpha >= beta:
                    break

        return best_value, best_move
    
    # generate a key for the memorization
    def generate_key(self):
        board_tuple = tuple(tuple(row) for row in self.board)
        return (board_tuple, self.current_player)

    # alpha-beta negamax algorithm with memorization
    def alphabeta_negamax2(self, depth, time_left, color, heuristic, alpha, beta):
        if depth == 0 or time_left < 0 or self.go:
            return self.heuristic_choice(heuristic) * color, []
        
        key = self.generate_key()
        stored_value = self.memorization.lookup(key)
        if stored_value is not None:
            value, stored_alpha, stored_beta = stored_value
            if stored_alpha <= alpha and stored_beta >= beta:
                return value, None

        best_value = -math.inf
        time_begin = time.perf_counter()
        best_move = []
        
        for x, y in self.shadow_pawn:
            sim_board = self.copy()
            sim_board.make_move(x, y)
            child_value,_ = sim_board.alphabeta_negamax2(depth - 1, time_left - (time.perf_counter() - time_begin), -color, heuristic, -beta, -alpha)
            if -child_value > best_value:
                best_value = -child_value
                best_move = [x, y]
                alpha = max(alpha, best_value)
                if alpha >= beta:
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
        elif method == 3:
            _,best_move = self.alphabeta_negamax(depth*2, time_left, 1, heuristic, -math.inf, math.inf)
        else:
            _,best_move = self.alphabeta_negamax2(depth*2, time_left, 1, heuristic, -math.inf, math.inf)
        
        best_x, best_y = best_move[0], best_move[1]
        self.make_move(best_x, best_y)
        return time.perf_counter() - debut
    
    # random move
    def random_ai(self, color):
        if (self.current_player == (-color)):
            return self.board
        x, y = self.shadow_pawn[np.random.randint(len(self.shadow_pawn))]
        self.make_move(x, y)
        return self.board
    
    def print_board(self):
        print("-"*20)
        print("  ", end="")
        for k in range(8):
            print(k, end=" ")
        print()
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                if self.board[i, j] == 0:
                    print(".", end=" ")
                elif self.board[i, j] == -1:
                    print("B", end=" ")
                else:
                    print("W", end=" ")
            print()

# simulation of the game
def ai_simulation(depth, method, heuristic, mixed_heuristic):
    game = Othello()
    game.initialisation()
    time_list = []
    cpt = 0
    heuristic = 1
    while(not game.go):
        if cpt == 40 and mixed_heuristic == 1:
            heuristic = 0
        if game.current_player == game.B:
            game.random_ai(game.B)
        else:
            time_list.append(game.ai_move(game.W, method, heuristic, depth, 100))
        cpt += 1
    winner = game.gameover()

    return winner, time_list

# simulation of multiple games
def ai_simulations(n, depth, method, heuristic, mixed_heuristic):
    list_play_time = []
    list_game_time = []        
    results = []
    
    for i in range(n):
        game_time = time.perf_counter()
        winner, time_list = ai_simulation(depth, method, heuristic, mixed_heuristic)
        game_time = time.perf_counter() - game_time
        list_game_time.append(game_time)
        results.append(winner)
        list_play_time.append(time_list)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str(method+1) + "/4 : " + str(i+1) + "/" + str(n))
    print("Fin de la simulation")

    list_means_play_time = [sum(filter(None, col)) / sum(1 for item in col if item is not None) for col in zip_longest(*list_play_time)]

    win = 0
    los = 0
    eq = 0
    for i in results:
        if i == -1:
            los += 1
        elif i == 1:
            win += 1
        else:
            eq += 1
    
    methods = ["Minimax", "Negamax", "Alpha-beta Minimax", "Alpha-beta Negamax", "Alpha-beta Negamax avec memoire"]
    heuristics = ["Nombre de pions", "Matrice de valeurs tactiques 1", "Matrice de valeurs tactiques 2"]
    mixed_heuristics = ["Non", "Oui"]
    
    method = methods[method]
    heuristic = heuristics[heuristic]
    if mixed_heuristic == 1:
        heuristic += " puis Nombre de pions (mixte)"
    mixed_heuristic = mixed_heuristics[mixed_heuristic]
    
    list_play_time_means = []
    for i in range(n):
        list_play_time_means.append(np.mean(list_play_time[i]))

    return list_game_time, list_means_play_time, win, los, eq


# USED FOR TESTING

# if __name__ == "__main__":
#     with open("results.txt", "w") as f:
#         f.write("RESULTATS DES SIMULATIONS\n\n") 
#     with open("results.csv", "w") as f:
#         f.write("Nombre de parties;Profondeur de recherche;Methode;Heuristique;Nombre de victoires;Nombre de defaites;Nombre d'egalites;Temps moyen d'une partie;Temps moyen d'un coup\n")
#     cpt = 1  
    
#     list_all_game_time_depth = []
#     list_all_play_time_depth = []
#     list_win_depth = []
#     list_los_depth = []
#     list_eq_depth = []
#     list_all_game_time_depth_mean = []
    
#     list_all_game_time_heuristic = []
#     list_all_play_time_heuristic = []
#     list_win_heuristic = []
#     list_los_heuristic = []
#     list_eq_heuristic = []
#     list_all_game_time_heuristic_mean = []
    
#     list_all_game_time_mixed = []
#     list_all_play_time_mixed = []
#     list_win_mixed = []
#     list_los_mixed = []
#     list_eq_mixed = []
#     list_all_game_time_mixed_mean = []
    
#     list_all_game_time_memory = []
#     list_all_play_time_memory = []
#     list_win_memory = []
#     list_los_memory = []
#     list_eq_memory = [] 
#     list_all_game_time_memory_mean = []
    
#     max_plays = 0
#     n_simulations = 20
#     # depth = 1
#     heuristic = 1
#     mixed = 1
    
#     # for heuristic in range(3):
#     #     for mixed in range(2):
#     for depth in range(3, 4):
        
#         list_all_game_time_method = []
#         list_all_play_time_method = []
#         list_win_method = []
#         list_los_method = []
#         list_eq_method = []
#         list_all_game_time_method_mean = []
        
#         for method in range (2,4):
#             if heuristic == 0 and mixed == 1:
#                 continue
#             with open("results.txt", "a") as f:
#                 f.write("-"*20 + "\n\nSIMULATION " + str(cpt) + "\n\n")
#             list_game_time, list_means_play_time, win, los, eq = ai_simulations(n_simulations, depth, method, heuristic, mixed)
#             if len(list_means_play_time) > max_plays:
#                 max_plays = len(list_means_play_time)
            
#             list_all_game_time_method.append(list_game_time)
#             list_all_game_time_method_mean.append(np.mean(list_game_time))
#             list_all_play_time_method.append(list_means_play_time)
#             list_win_method.append(win)
#             list_los_method.append(los)
#             list_eq_method.append(eq)
            
#             if method == 3:
#                 list_all_game_time_depth.append(list_game_time)
#                 list_all_game_time_depth_mean.append(np.mean(list_game_time))
#                 list_all_play_time_depth.append(list_means_play_time)
#                 list_win_depth.append(win)
#                 list_los_depth.append(los)
#                 list_eq_depth.append(eq)
                
#                 if depth == 2:
#                     list_all_game_time_heuristic.append(list_game_time)
#                     list_all_game_time_heuristic_mean.append(np.mean(list_game_time))
#                     list_all_play_time_heuristic.append(list_means_play_time)
#                     list_win_heuristic.append(win)
#                     list_los_heuristic.append(los)
#                     list_eq_heuristic.append(eq)
                    
#                     list_all_game_time_mixed.append(list_game_time)
#                     list_all_game_time_mixed_mean.append(np.mean(list_game_time))
#                     list_all_play_time_mixed.append(list_means_play_time)
#                     list_win_mixed.append(win)
#                     list_los_mixed.append(los)
#                     list_eq_mixed.append(eq)
            
#             cpt += 1
        
#         method_alpha_beta_result_to_chart(n_simulations, depth, list_all_game_time_method_mean, list_all_play_time_method, max_plays, list_win_method, list_los_method, list_eq_method)
    
    
#     # with open("results.txt", "a") as f:
#     #     f.write("-"*20 + "\n\nSIMULATION " + str(cpt) + "\n\n")
#     # cpt += 1
#     # list_game_time, list_means_play_time, win, los, eq = ai_simulations(n_simulations, 3, 3, 1, 1)
#     # if len(list_means_play_time) > max_plays:
#     #     max_plays = len(list_means_play_time)

#     # list_all_game_time_depth.append(list_game_time)
#     # list_all_game_time_depth_mean.append(np.mean(list_game_time))
#     # list_all_play_time_depth.append(list_means_play_time)
#     # list_win_depth.append(win)
#     # list_los_depth.append(los)
#     # list_eq_depth.append(eq)
    
#     # list_all_game_time_memory.append(list_game_time)
#     # list_all_game_time_memory_mean.append(np.mean(list_game_time))
#     # list_all_play_time_memory.append(list_means_play_time)
#     # list_win_memory.append(win)
#     # list_los_memory.append(los)
#     # list_eq_memory.append(eq)
    
    
#     # for heuristic in range(3):
#     #     if heuristic == 1:
#     #         continue
#     #     with open("results.txt", "a") as f:
#     #         f.write("-"*20 + "\n\nSIMULATION " + str(cpt) + "\n\n")
#     #     cpt += 1
#     #     list_game_time, list_means_play_time, win, los, eq = ai_simulations(n_simulations, 3, 3, heuristic, 1)
#     #     if len(list_means_play_time) > max_plays:
#     #         max_plays = len(list_means_play_time)
        
#     #     list_all_game_time_heuristic.append(list_game_time)
#     #     list_all_game_time_heuristic_mean.append(np.mean(list_game_time))
#     #     list_all_play_time_heuristic.append(list_means_play_time)
#     #     list_win_heuristic.append(win)
#     #     list_los_heuristic.append(los)
#     #     list_eq_heuristic.append(eq)
    
#     # with open("results.txt", "a") as f:
#     #     f.write("-"*20 + "\n\nSIMULATION " + str(cpt) + "\n\n")
#     # cpt += 1
#     # list_game_time, list_means_play_time, win, los, eq = ai_simulations(n_simulations, 3, 3, 1, 0)
#     # if len(list_means_play_time) > max_plays:
#     #     max_plays = len(list_means_play_time)
    
#     # list_all_game_time_mixed.append(list_game_time)
#     # list_all_game_time_mixed_mean.append(np.mean(list_game_time))
#     # list_all_play_time_mixed.append(list_means_play_time)
#     # list_win_mixed.append(win)
#     # list_los_mixed.append(los)
#     # list_eq_mixed.append(eq)
    
#     # with open("results.txt", "a") as f:
#     #     f.write("-"*20 + "\n\nSIMULATION " + str(cpt) + "\n\n")
#     # cpt += 1
#     # list_game_time, list_means_play_time, win, los, eq = ai_simulations(n_simulations, 3, 4, 1, 1)
    
#     # list_all_game_time_memory.append(list_game_time)
#     # list_all_game_time_memory_mean.append(np.mean(list_game_time))
#     # list_all_play_time_memory.append(list_means_play_time)
#     # list_win_memory.append(win)
#     # list_los_memory.append(los)
#     # list_eq_memory.append(eq)
    

#     # depth_result_to_chart(n_simulations, list_all_game_time_depth_mean, list_all_play_time_depth, max_plays, list_win_depth, list_los_depth, list_eq_depth)
#     # heuristic_result_to_chart(n_simulations, list_all_game_time_heuristic_mean, list_all_play_time_heuristic, max_plays, list_win_heuristic, list_los_heuristic, list_eq_heuristic)
#     # mixed_result_to_chart(n_simulations, list_all_game_time_mixed_mean, list_all_play_time_mixed, max_plays, list_win_mixed, list_los_mixed, list_eq_mixed)
#     # memory_result_to_chart(n_simulations, list_all_game_time_memory_mean, list_all_play_time_memory, max_plays, list_win_memory, list_los_memory, list_eq_memory)