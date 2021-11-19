import numpy as np
import copy
import random

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        def complete_game(self, board):
            player_num = self.player_number
            player_win_str = '{0}{0}{0}{0}'.format(player_num)
            to_str = lambda a: ''.join(a.astype(str))

            def check_horizontal(b):
                for row in b:
                    if player_win_str in to_str(row):
                        return True
                return False

            def check_verticle(b):
                return check_horizontal(b.T)

            def check_diagonal(b):
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b
                
                    root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                    if player_win_str in to_str(root_diag):
                        return True

                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(np.int))
                            if player_win_str in diag:
                                return True

                return False

            return (check_horizontal(board) or
                    check_verticle(board) or
                    check_diagonal(board))
                    
        def max_value(self, board, depth, alpha, beta, col):
            #gets all valid moves - 1/length of valid moves is probabilty of the path being taken
            
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            #depth of zero or terminal state check 
            if depth == 0 or len(valid_cols) == 0 or complete_game(self, board):
                if col not in valid_cols:
                    if len(valid_cols) != 1:
                        ran = random.randrange(0, len(valid_cols)-1)
                        return (self.evaluation_function(board), valid_cols[ran])
                    return (self.evaluation_function(board), valid_cols[0])
                return (self.evaluation_function(board), col)

            value = float('-inf')
            move = col
            for col in valid_cols:
                copyboard = copy.copy(board)
                #insert new value
                i = 5
                while i >= 0:
                    if copyboard[i][col] == 0:
                        copyboard[i][col] = self.player_number
                        i = -10000
                        break
                    i =- 1                

                alpha1 = min_value(self, copyboard, depth-1, alpha, beta, col)
                if (alpha1[0] > value):
                    value = alpha1[0]
                    move = alpha1[1]
                
                if value >= beta:
                    return (value, move)
                alpha = max(alpha, value)

            return (value, move)

        def min_value(self, board, depth, alpha, beta, col):
            #gets all valid moves - 1/length of valid moves is probabilty of the path being taken
            
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            #depth of zero or terminal state check 
            if depth == 0 or len(valid_cols) == 0 or complete_game(self, board):
                if col not in valid_cols:
                    if len(valid_cols) != 1:
                        ran = random.randrange(0, len(valid_cols)-1)
                        return (self.evaluation_function(board), valid_cols[ran])
                    return (self.evaluation_function(board), valid_cols[0])
                return (self.evaluation_function(board), col)

            value = float('inf')

            opponent_num = 1
            if self.player_number == 1:
                opponent_num = 2

            for col in valid_cols:
                
                copyboard = copy.copy(board)

                #insert new value
                i = 5
                while i >= 0:
                    if copyboard[i][col] == 0:
                        copyboard[i][col] = opponent_num
                        i = -10000
                        break
                    i =- 1
                
                beta1 = max_value(self, copyboard, depth-1, alpha, beta, col)
                if (beta1[0] < value):
                    value = beta1[0]
                    move = beta1[1]
                if value <= alpha:
                    return (value, move)
                beta = min(beta, value)
            return (value, move)

        depth = 5
        turn = max_value(self, board, depth, float('-inf'), float('inf'), -1)
        return turn[1]

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        def complete_game(self, board):
            player_num = self.player_number
            player_win_str = '{0}{0}{0}{0}'.format(player_num)
            to_str = lambda a: ''.join(a.astype(str))

            def check_horizontal(b):
                for row in b:
                    if player_win_str in to_str(row):
                        return True
                return False

            def check_verticle(b):
                return check_horizontal(b.T)

            def check_diagonal(b):
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b
                
                    root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                    if player_win_str in to_str(root_diag):
                        return True

                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(np.int))
                            if player_win_str in diag:
                                return True

                return False

            return (check_horizontal(board) or
                    check_verticle(board) or
                    check_diagonal(board))

        def max_value(self, depth, board, col):
            """
            Returns max value of successor of state and column
            """
            v = -1000000000000

            #gets all valid moves - 1/length of valid moves is probabilty of the path being taken
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            #depth of zero or terminal state check 
            if depth == 0 or len(valid_cols) == 0 or complete_game(self, board):
                return (self.evaluation_function(board), col)
            move = valid_cols[0]
            for col in valid_cols:
                #set up new copy of board 
                copyboard = copy.copy(board)

                #insert new value
                i = 5
                while i >= 0:
                    if copyboard[i][col] == 0:
                        copyboard[i][col] = self.player_number
                        i = -10000
                        break
                    i =- 1


                #recursive call to exp value

                newv = exp_value(self, depth-1, copyboard, col)
                if (newv > v):
                    v = newv
                    move = col

            return (v, move)

        def exp_value(self, depth, board, col):
            """
            Returns probability * value of all successors of the state and the column it put it in 
            """
            v = 0
            opp_number = 1
            if self.player_number == 1:
                opp_number = 2
            #gets all valid moves - 1/length of valid moves is probabilty of the path being taken
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            #depth of zero or terminal state check
            if depth == 0 or len(valid_cols) == 0:
                return (self.evaluation_function(board))

            for col in valid_cols:
                p = 1/(len(valid_cols))
                #set up new copy of board here with inserted value
                copyboard = copy.copy(board)
                #insert new value
                i = 5
                while i >= 0:
                    if copyboard[i][col] == 0:
                        copyboard[i][col] = opp_number
                        i = -10
                    i -= 1
                #recursive call to max_value
                value2 = max_value(self, depth-1, copyboard, col)
                v += p * value2[0]
            return v

        depth = 2
        vmove = max_value(self, depth, board, 0)
        return vmove[1]

    '''
    for each value that is true - 3 in a row, add 2
    if true for opposite, subtract 2
    if four in a row is found = 1000000 opposite is -100000

    horizontal case:
    find three in a row and see if next to it is 0 and below it isn't 0 - block it - likes 2221, or 1222
    find three in a row (for yourself) and see if next to it is 0 and below it isn't 0 - likes 0111 or 1110

    vertical case:
    three in a row - if top is open, block or take depending on what the values are - likes 2221, 1110 
    '''
    def evaluation_function(self, board):
        player_num = self.player_number
        opponent_num = 1
        if player_num == 1:
            opponent_num = 2
        
        value = 0

        player_three_str_left = '0{0}{0}{0}'.format(player_num)
        player_three_str_right = '{0}{0}{0}0'.format(player_num)
        opp_three_str_left = '0{0}{0}{0}'.format(opponent_num)
        opp_three_str_right = '{0}{0}{0}0'.format(opponent_num)

        player_three_b = str(player_num) + str(opponent_num) + str(opponent_num) + str(opponent_num)
        player_three_b2 = str(opponent_num) + str(opponent_num) + str(opponent_num) + str(player_num)
        player_three_b3 = str(opponent_num) + str(player_num) + str(opponent_num) + str(opponent_num)
        player_three_b4 = str(opponent_num) + str(opponent_num) + str(player_num) + str(opponent_num)

        player_two_str_left = '0{0}{0}'.format(player_num)
        player_two_str_right = '{0}{0}0'.format(player_num)

        opp_two_str_left = '0{0}{0}'.format(opponent_num)
        opp_two_str_right = '{0}{0}0'.format(opponent_num)

        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        player_los_str = '{0}{0}{0}{0}'.format(opponent_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal_two(b):
            for row in b:
                if player_two_str_left in to_str(row):
                    return True
                if player_two_str_right in to_str(row):
                    return True
            return False

        def check_horizontal_two_o(b):
            for row in b:
                if opp_two_str_left in to_str(row):
                    return True
                if opp_two_str_right in to_str(row):
                    return True
            return False

        def check_horizontal_three(b):
            for row in b:
                if player_three_str_left in to_str(row):
                    return True
                if player_three_str_right in to_str(row):
                    return True
            return False

        def check_vertical_three(b):
            return check_horizontal_three(b.T)   


        def check_horizontal_three_o(b):
            for row in b:
                if opp_three_str_left in to_str(row):
                    return True
                if opp_three_str_right in to_str(row):
                    return True
            return False

        def check_vertical_three_o(b):
            return check_horizontal_three_o(b.T) 

        def check_horizontal_three_b_vert(b):
            for row in b:
                if player_three_b in to_str(row):
                    return True
                if player_three_b2 in to_str(row):
                    return True
                if player_three_b3 in to_str(row):
                    return True
                if player_three_b4 in to_str(row):
                    return True
            return False

        def check_horizontal_three_b(b):
            for row in b:
                if player_three_b2 in to_str(row):
                    return True
            return False

        def check_vertical_three_b(b):
            return check_horizontal_three_b(b.T)  

        #checking for board with win in it 
        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True
            return False

        #checking board with lost in it 
        def check_horizontal_los(b):
            for row in b:
                if player_los_str in to_str(row):
                    return True
            return False

        def check_verticle_los(b):
            return check_horizontal_los(b.T)

        def check_diagonal_los(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_los_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_los_str in diag:
                            return True

            return False
        
        if (check_horizontal(board) or check_verticle(board) or check_diagonal(board)):
            value += 1000

        if (check_horizontal_los(board) or check_verticle_los(board) or check_diagonal_los(board)):
            value += -500

        if (check_horizontal_three(board) or check_vertical_three(board)):
            value += 25

        if (check_horizontal_three_o(board) or check_vertical_three_o(board)):
            value += -20

        if (check_horizontal_three_b_vert(board) or check_vertical_three_b(board)):
            value += 30

        if (check_horizontal_two):
            value += 20

        if (check_horizontal_two_o):
            value += -15

        #newval = check_three_horizontal(board, value)

        return value

        

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

