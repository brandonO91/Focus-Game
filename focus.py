#  Brandon Alan Oyama
#  12/03/2020
#  Focus game for portfolio project.  Class will initialize game with player and colors
#  and keep track of game process until completion.  Players are created using a Player
#  class that keeps track of color, reserved, anc captured pieces and returns their values
#  if called from the FocusGame class.

class Player:

    '''class to create player objects for game class FocusGame'''

    def __init__(self, player):
        self._player = player[0]
        self._color = player[1]
        self._reserved = 0
        self._captured = 0

    def get_player(self):

        '''will return player objects title'''

        return self._player

    def get_color(self):

        '''will return player objects color'''

        return self._color

    def get_reserved(self):

        '''will return amount of reserved pieces by player object'''

        return self._reserved

    def get_captured(self):

        ''' will return amount of pieces captured by player object'''

        return self._captured

    def add_captured(self):

        ''' will add a captured piece to user object'''

        self._captured += 1

    def add_reserved(self):

        ''' will add a reserved piece to player object'''

        self._reserved += 1

    def use_reserved(self):

        '''will take away one reserved available piece for player object'''

        self._reserved -= 1


class FocusGame:

    ''' class will create game and handle all play with two users
        an init method to initialize give players and colors, and board with
            positions marked for each individual, data member for each player
            board will be created using six lists within a list
        players will be their own object with personal get and check mothods to return
            info back to main game class
        will keep track of status whether still at play or finished
        keep track of whos turn it is
        '''

    def __init__(self, first, second):

        ''' initializes players, turn, status of game, and board'''

        self._players = []
        self._turn = None  # first move sets game up
        self._status = True
        self._start = False
        self._board =  [[first[1],first[1],second[1],second[1], first[1],first[1]],
                        [second[1],second[1],first[1],first[1],second[1],second[1]],
                        [first[1],first[1],second[1],second[1],first[1],first[1]],
                        [second[1],second[1],first[1],first[1],second[1],second[1]],
                        [first[1],first[1],second[1],second[1],first[1],first[1]],
                        [second[1],second[1],first[1],first[1],second[1],second[1]]]

        while self._start is False:
            p1 = Player(first)
            p2 = Player(second)
            self.add_player(p1)
            self.add_player(p2)
            self._start = True

    def get_players(self):

        ''' returns player objects that are currently in use'''

        return self._players

    def add_player(self, player):

        '''adds player objects to use in game'''

        self._players.append(player)

    def get_start(self):

        ''' returns whether game has started'''

        return self._start

    def get_status(self):

        ''' returns status of game, if completed or still in play'''

        return self._status


    def get_board(self):

        '''method to return the current board'''

        return self._board

    def print_board(self):

        ''' method to print board for visual
            will use get_board method and print
            out each list with positions within'''

        board = self.get_board()
        for i in board:
            print(i)
        return

    def check_color(self, player):

        ''' will return color of player object with given player name'''

        for p in self._players:
            if p.get_player() == player:
                return p.get_color()

    def check_player(self, name):

        ''' will return players objects name '''

        players = self.get_players()
        for p in players:
            if p.get_player() == name:
                return p.get_player()

    def move_piece(self, player, piece, move, pieces):

        ''' method will determine if correct turn, correct piece, valid move and pieces, and whether game has concluded'''

        stack = self.check_stack(piece)
        turn = self.get_turn()
        if turn is None or turn == player:
            if self.check_position(player, piece) is True:
                if self.check_move(piece, move) is True:
                    if stack >= pieces:
                        self.make_move(piece, move, pieces)
                        stack = self.check_stack(move)
                        if stack > 5:
                            self.capt_res(player, move)
                        self.end_game(player)
                        if self.get_status() is not True:
                            return 'Win'
                        self.next(player)
                        return 'successfully moved'
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def capt_res(self, player, move):

        ''' after each turn the method will determine if there are greater than 5 pieces on stack
            and whether pieces are to be captured or reserved, starting at index 0 '''

        players = self.get_players()
        color = self.check_color(player)
        (y, x) = move
        board = self.get_board()
        current_pieces = board[y][x]
        pawns = len(current_pieces) - 1
        amount = pawns - 5
        store = board[y][x][:amount]
        for p in players:
            if p.get_player() == player:
                for pawn in store:
                    if pawn == color:
                        p.add_reserved()
                    else:
                        p.add_captured()
        board[y][x] = board[y][x][amount:]
        return
        #print(board[new_y][new_x])
        #board[new_y][new_x] = board[new_y][new_x] + str(to_move)
        #board[y][x] = board[y][x][:amount]

    def make_move(self, piece, move, pieces):

        ''' will take the stack to be moved and add total amount of pawns to the new space,
            and will modify previous and current space to reflect stack for pawns moved'''

        (y, x) = piece
        (new_y, new_x) = move
        board = self.get_board()
        current_pieces = board[y][x]
        pawns = len(current_pieces) - 1
        amount = pawns - pieces
        to_move = board[y][x][amount:]
        board[new_y][new_x] = board[new_y][new_x] + str(to_move)
        board[y][x] = board[y][x][:amount]

    def next(self, player):

        ''' will change the current turn to next player'''

        if player == 'PlayerA':
            self._turn = 'PlayerB'
            return
        if player == 'PlayerB':
            self._turn = 'PlayerA'
            return


        #  need to make change to turn every time a good move is completed

    def end_game(self, player):

        ''' will be called upon completion of each turn to determine if any one of players is unable to
            play a move...if found that no pawns are available to a player, that player loses and status of
            game is updated to false to complete game'''

        user = self.get_a_player(player)
        prisoners = user.get_captured()
        if prisoners == 6:
            self._status = False
        return

    def get_turn(self):

        ''' method will return whos turn it currently is'''

        return self._turn

    def check_position(self, player, coordinate):

        '''method that will use get board and see if coordinates given, current or
        destination, are valid and return True or False if available or not'''

        color = self.check_color(player)
        top_pawn = self.top_piece(coordinate)
        (y, x) = coordinate
        board = self.get_board()
        if board[y][x] == '':
            return False
        if 0 <= y <= 5 and 0 <= x <= 5:
            if top_pawn == color:
                return True
            else:
                return False
        else:
            return False

    def check_move(self, current, move):

        '''take in two coordinates to make sure valid move on board check if enough on stack
            to move given amount and that not diagonal'''

        jump = self.check_stack(current)
        (cy, cx) = current              #  cy and cx are current y and current x
        (y, x) = move
        if 0 <= y <= 5 and 0 <= x <= 5:
            if y != cy and x != cx:
                return False
            if y == cy:
                attempt = cx - x
                abs(attempt)
                if attempt <= jump:
                    return True
                else:
                    return False
            elif x == cx:
                attempt = cy - y
                abs(attempt)
                if attempt <= jump:
                    return True
                else:
                    return False
        else:
            return False


    def check_stack(self, coordinate):  #  (y,x)

        '''will return how many pawns are currently on that space'''

        (y, x) = coordinate
        board = self.get_board()
        stack = board[y][x]
        count = 0

        for i in stack:
            count += 1
        return count


    def show_pieces(self, coordinate):  #  (y,x)

        ''' takes a given coordinate on board and returns stack of pawns on that space'''

        pawns = []
        (y, x) = coordinate
        board = self.get_board()
        pieces = board[y][x]
        for p in pieces:
            pawns.append(p)
        return pawns

    def top_piece(self, coordinate):

        '''will return what the last piece on top of stack is'''

        stack = self.show_pieces(coordinate)
        if stack == '':
            return ''
        last = len(stack) - 1
        return stack[last]

    def show_reserve(self, player):

        ''' will check the player object and return number reserve pieces'''

        players = self.get_players()
        for p in players:
            if p.get_player() == player:
                return p.get_reserved()

    def show_captured(self, player):

        ''' will return the number of captured pawns for player object'''

        players = self.get_players()
        for p in players:
            if p.get_player() == player:
                return p.get_captured()

    def reserved_move(self, player, coordinate):

        ''' will first check if player object has reserved pawns and if they do will play at
            given space'''

        user = self.get_a_player(player)
        color = self.check_color(player)
        turn = self.get_turn()

        if turn is None or turn == player:
            if user.get_reserved() > 0:
                (y, x) = coordinate
                board = self.get_board()
                board[y][x] = board[y][x] + str(color)
                user.use_reserved()
            else:
                return False

            self.next(player)
        else:
            return False


    def get_a_player(self, player):

        ''' will check player objects and return one matching player name'''

        players = self.get_players()
        for p in players:
            if p.get_player() == player:
                return p

'''
game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))
game.print_board()
print(game.move_piece('PlayerA',(0,0), (0,1), 1))  #Returns message "successfully moved"
print(game.show_pieces((0,1))) #Returns ['R','R']
print(game.show_captured('PlayerA')) # Returns 0
print(game.reserved_move('PlayerA', (0,0))) # Returns message "No pieces in reserve"
print(game.show_reserve('PlayerA')) # Returns 0
#print(game.move_piece('PlayerB', (0,0), (0,1), 1))
'''






#game = FocusGame(('PlayerA', 'R'),('PlayerB', 'G'))
#game.print_board()
#game.capt_res('PlayerB', (0, 0))
#game.print_board()
#print(game.get_turn())
#print(game.show_reserve('PlayerB'))
#print(game.reserved_move('PlayerB', (5,5)))
#print(game.reserved_move('PlayerA', (5,5)))
#game.make_move((1,2), (1,3), 1)
#game.print_board()
#print(game.move_piece('PlayerB', (1,4), (1,5), 1))
#print(game.get_turn())
#print(game.move_piece('PlayerB', (1,1), (2,1), 5))
#print(game.show_reserve('PlayerA'))












#print(game.show_pieces((1,3)))
#print(game.top_piece((1,3)))
#print(game.check_position(('PlayerA'), (1,4)))
#print(game.top_piece((1,4)))
#print(game.check_stack((1, 3)))  #  method to see how many are in stack
#print(game.check_position((-5,20)))  #  method to check valid start location
#print(game.get_players())
#print(game.check_color('PlayerA'))
#print(game.get_start())
#print(game.get_status())
#print(game.check_player('PlayerA'))
#print(game.check_move((1,3),(2,4)))
