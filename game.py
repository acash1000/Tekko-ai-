import copy
import math
import random
class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    boardweight = [
                            [2, 2, 1, 2, 2],
                            [2, 4, 3, 4, 2],
                            [1, 3, 5, 3, 1],
                            [2, 4, 3, 4, 2],
                            [2, 2, 1, 2, 2]
                            ]
    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        pieceamm =0
        for i in range(5):
            for j in range(5):
                if(self.board[i][j] == self.my_piece):
                    pieceamm+=1

        drop_phase = (pieceamm!=4)   # TODO: detect drop phase



        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better

        # ensure the destination (row,col) tuple is at the beginning of the move list
        if not drop_phase:
            suc = self.succ(state)
            mov = 0
            ind = 0
            for s in suc:
                tempstate = copy.deepcopy(state)
                boardatsuc = self.place_piece2(tempstate, s, self.my_piece)
                move = self.max_value(boardatsuc, 2)
                if(move>mov):
                    mov = move
                    ind = suc.index(s)
            move = suc[ind]
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            i,j =move
            # self.board[j[0]][j[1]] =' '
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
        else:
            move = self.findstart(state)
        return move
    def heuristic_game_value(self, state):
        myPiece = self.my_piece
        ai_h = 0
        op_h = 0
        if (self.game_value(state) == 1):
            return 1
        if (self.game_value(state) == -1):
            print(state)
        for i in range(len(state)):
            for j in range(len(state[0])):
                if (state[i][j] == myPiece):
                    p = (i,j)
                    distance = self.distpt(state,p,myPiece)
                    if(distance!=0):
                        ai_h+= (1*self.boardweight[i][j])/5**distance
                    else:
                        ai_h += (1 * self.boardweight[i][j])
                elif(state[i][j] != ' '):
                    p = (i, j)
                    distance = self.distpt(state, p, self.opp)
                    if (distance != 0):
                        op_h +=(1*self.boardweight[i][j])/2**distance
                    else:
                        ai_h += (1 * self.boardweight[i][j])
        return math.sqrt(ai_h)-math.sqrt(op_h)
    def euclidan(self,p1,p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    def distpt(self,state,pt,peice):
        di =0.0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if(state[i][j] == peice):
                    di+=self.euclidan(pt,(i,j))
        return math.ceil(di)
    def huros(self,state):
        myPiece = self.my_piece
        ai_h = 0
        op_h = 0
        if (self.game_value(state) == 1):
            return 1
        if (self.game_value(state) == -1):
            print(state)
        for i in range(len(state)):
            for j in range(len(state[0])):
                if (state[i][j] == myPiece):
                    ai_h += (1 * self.boardweight[i][j])
                elif (state[i][j] != ' '):

                    op_h += (1 * self.boardweight[i][j])

        return math.sqrt(ai_h) - math.sqrt(op_h)
    def findstart(self,state):
        best = 0
        move = []
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == ' ':
                    temp = copy.deepcopy(state)
                    mov = [(i,j),(i,j)]
                    tempstate = self.place_piece2(temp,mov,self.my_piece)
                    h = self.huros(tempstate)
                    if h>=best:
                        best = h
                        move = mov
        res = []
        res.append(move[0])
        return res
    def max_value(self, state, depth):
        maxSize = float("inf")
        alpha = -maxSize
        beta = maxSize
        best =self.heuristic_game_value(state)
        tempstate = copy.deepcopy(state)
        if self.game_value(tempstate) !=0:
            return best
        elif depth ==0:
            return self.heuristic_game_value(state)
        else:
            states = self.succ(tempstate)
            indexOfbestMove = 0
            for s in states:
                boardatsuc = self.place_piece2(tempstate,s,self.my_piece)
                tempscore=self.max_value(boardatsuc,depth-1)
                alpha = self.max(alpha,tempscore)
                if(best <=tempscore):
                    best = tempscore
                    tempstate = boardatsuc
                if beta<=alpha:
                    break
            return best
    def max(self,a,b):
        if(a>=b):
            return a
        return b
    def succ(self, state):
        myPiece = self.my_piece
        listofmoves=[]
        if(self.game_value(state) != 0):
            return self.game_value(state)
        for i in range(len(state)):
            for j in range(len(state[0])):
                if(state[i][j] == myPiece):
                    current = (i,j)
                    paths =self.generatepath(i,j,state)
                    for p in paths:
                        add = []
                        add.append(p)
                        add.append(current)
                        listofmoves.append(add)
        return listofmoves
    def generatepath(self,i,j,state):
        k =0
        moves = []
        while(k !=8):
            if(k ==0 and i<4and(state[i+1][j] == ' ') ):
                mv =(i+1,j)
                moves.append(mv)
            elif(k ==1 and i>0and(state[i-1][j] == ' ')):
                mv = (i - 1, j)
                moves.append(mv)
            elif (k ==2 and j>0and(state[i][j-1] == ' ') ):
                mv = (i, j-1)
                moves.append(mv)
            elif (k ==3 and j<4 and (state[i][j+1] == ' ')):
                mv = (i, j +1)
                moves.append(mv)
            elif (k ==4and(i<4 and j<4)and(state[i+1][j+1] == ' ') ):
                mv = (i+1, j + 1)
                moves.append(mv)
            elif (k ==5and(i>0 and j<4)and(state[i-1][j+1] == ' ')):
                mv = (i-1, j + 1)
                moves.append(mv)
            elif (k ==6and(i<4 and j>0)and(state[i+1][j-1] == ' ')):
                mv = (i+1, j - 1)
                moves.append(mv)
            elif (k ==7and(i>0 and j>0)and(state[i-1][j-1] == ' ')):
                mv = (i-1, j -1)
                moves.append(mv)
            k+=1
        return moves
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
    def place_piece2(self,state, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        state[move[1][0]][move[1][1]] = ' '
        state[move[0][0]][move[0][1]] = piece
        return state

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for col in range(3,5):
            for i in range(3,5):
                if state[i][col] != ' ' and state[i][col] == state[i - 1][col-1] == state[i - 2][col-2] == state[i - 3][col-3]:
                    return 1 if state[i][col] == self.my_piece else -1
        # TODO: check / diagonal wins
        for col in range(2):
            for i in range(3, 5):
                if state[i][col] != ' ' and state[i][col] == state[i - 1][col + 1] == state[i - 2][col + 2] == state[i - 3][col + 3]:
                    return 1 if state[i][col] == self.my_piece else -1
        # TODO: check diamond wins
        for col in range(4):
            for i in range(1,5):
                # print(str(i)+" "+str(col))
                if state[i][col] != ' ' and state[i][col] == state[i - 1][col] == state[i -1][col+1] == state[i][col +1]:
                    return 1 if state[i][col] == self.my_piece else -1
        for col in range(4):
            for i in range(4):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 1][col + 1] == state[i][ col + 1]:
                    return 1 if state[i][col] == self.my_piece else -1
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
