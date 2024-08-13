import pygame
from Globals import PieceColor

# shortened enums
WHITE = __import__('Globals').PieceColor.WHITE
BLACK = __import__('Globals').PieceColor.BLACK
class piece:
    def __init__(self, path):
        self.path = path
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (128, 128))

    @staticmethod
    def escapesCheck(checker: 'piece', x: int, y: int, color: PieceColor, board: 'board') -> bool: #type: ignore
        if (piece.causesCheck(checker, x, y, color, board) == False):
            return True
        return False

    @staticmethod
    def inCheck(color: PieceColor, board: 'board', pieceList: list): #type: ignore
        targetKing = None
        for currentPiece in pieceList:
            if (currentPiece.color == color and isinstance(currentPiece, king)):
                targetKing = currentPiece
                break

        # iterate through pieces that are opposite color
        # if this piece's legal moves contain opposite king, king is in check 
        for currentPiece in pieceList:
            if (color == WHITE and currentPiece.color == BLACK) or (color == BLACK and currentPiece.color == WHITE):
                currentPiece.generateMoves(board)
                if ( (targetKing.x, targetKing.y) in currentPiece.legalMoves ):
                    return True
        return False
            
    @staticmethod
    def causesCheck(checker: 'piece', x: int, y: int, color: PieceColor, board: 'board', enPessant: bool = False): #type: ignore
        ''' Simulates move to see if it causes check. Assumes (x, y) is a legal move barring
            check related conditions. '''
        pieceListCopy = board.pieceList.copy()

        tempTake = None

        oldX = checker.x
        oldY = checker.y

        board.piecesOnBoard[oldX][oldY] = None
        checker.x = x
        checker.y = y

        # simulate non-enPessant capture
        if (board.piecesOnBoard[x][y] != None):
            if (board.piecesOnBoard[x][y].color != color):
                tempTake = board.piecesOnBoard[x][y]
                pieceListCopy.remove(tempTake)
            else:
                checker.x = oldX
                checker.y = oldY
                board.piecesOnBoard[oldX][oldY] = checker
                return False
        
        #simulate en pessant capture
        if (enPessant):
            tempTake = board.piecesOnBoard[x][y - 1] if board.piecesOnBoard[x][y - 1] != None else board.piecesOnBoard[x][y + 1]
            board.piecesOnBoard[tempTake.x][tempTake.y] = None
            pieceListCopy.remove(tempTake)

        board.piecesOnBoard[x][y] = checker
        if piece.inCheck(color, board, pieceListCopy):
            # undo simulated move
            checker.x = oldX
            checker.y = oldY

            board.piecesOnBoard[x][y] = None
            board.piecesOnBoard[oldX][oldY] = checker

            # undo simulated capture if applicable
            if (tempTake != None):
                if (not enPessant):
                    board.piecesOnBoard[x][y] = tempTake
                    pieceListCopy.append(tempTake)
                    tempTake = None
                elif (enPessant):
                    board.piecesOnBoard[tempTake.x][tempTake.y] = tempTake
                    pieceListCopy.append(tempTake)
                    tempTake = None

            return True
        
        # undo simulated move
        checker.x = oldX
        checker.y = oldY

        board.piecesOnBoard[x][y] = None
        board.piecesOnBoard[oldX][oldY] = checker

        # undo simulated capture if applicable
        if (tempTake != None):
            if (not enPessant):
                board.piecesOnBoard[x][y] = tempTake
                pieceListCopy.append(tempTake)
                tempTake = None
            elif (enPessant):
                board.piecesOnBoard[tempTake.x][tempTake.y] = tempTake
                pieceListCopy.append(tempTake)
                tempTake = None

        return False
    
    def generateLegalMoves(self, board: 'board'): #type: ignore
        self.generateMoves(board)

        for i in range(len(self.legalMoves) - 1, -1, -1):
            if (type(self) is pawn and self.legalMoves[i] == board.enPessantSquare):
                if (self.causesCheck(self, self.legalMoves[i][0], self.legalMoves[i][1], self.color, board, True)):
                    self.legalMoves.remove( (self.legalMoves[i][0], self.legalMoves[i][1]) )

            elif self.causesCheck(self, self.legalMoves[i][0], self.legalMoves[i][1], self.color, board):
                self.legalMoves.remove( (self.legalMoves[i][0], self.legalMoves[i][1]) )

class king(piece):
    def __init__(self, x: int, y: int, color: PieceColor, board: 'board'): #type: ignore
        self.color = color
        self.x = x
        self.y = y
        self.legalMoves = []
        self.firstMove = True

        board.piecesOnBoard[self.x][self.y] = self

        if (color == BLACK):
            super().__init__("../res/blackKing.png")
        else:
            super().__init__("../res/whiteKing.png")

        board.pieceList.append(self)

    # moves w/ check
    def generateMoves(self, board: 'board'): #type: ignore
        self.legalMoves = []

        # i, j as offsets
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0) and (self.x + i < 8 and self.x + i >= 0 and self.y + j < 8 and self.y + j >= 0):
                    if (board.piecesOnBoard[self.x + i][self.y + j] != None):
                        if (board.piecesOnBoard[self.x + i][self.y + j].color == self.color):
                            continue
                    self.legalMoves.append( (self.x + i, self.y + j) )

    # moves w/o check
    def generateLegalMoves(self, board: 'board'): #type: ignore
        super().generateLegalMoves(board)
        self.generateLegalCastles(board)
    
    # generate legal castles
    def generateLegalCastles(self, board: 'board'): #type: ignore
        if (self.firstMove == True):
            if (not piece.inCheck(self.color, board, board.pieceList)):
                if self.color == WHITE:
                    if ( (5, 7) in self.legalMoves) and (not piece.causesCheck(self, 6, 7, WHITE, board) == True) and board.piecesOnBoard[6][7] == None:
                        prospectiveRook = board.piecesOnBoard[7][7]
                        if prospectiveRook != None and prospectiveRook.color == WHITE and type(prospectiveRook) == rook and prospectiveRook.firstMove:
                            self.legalMoves.append( (6, 7) )
                    for i in range(1, 4):
                        if piece.causesCheck(self, i, 7, WHITE, board) == True or board.piecesOnBoard[i][7] != None:
                            return
                    prospectiveRook = board.piecesOnBoard[0][7]
                    if not ((prospectiveRook != None and (prospectiveRook.color == WHITE and type(prospectiveRook) == rook) and (prospectiveRook.firstMove))):
                        return
                    self.legalMoves.append( (2, 7) )
                else:
                    if ( (5, 0) in self.legalMoves) and (not piece.causesCheck(self, 6, 0, BLACK, board) == True) and board.piecesOnBoard[6][0] == None:
                        prospectiveRook = board.piecesOnBoard[7][0]
                        if prospectiveRook != None and (prospectiveRook.color == BLACK and type(prospectiveRook) == rook) and (prospectiveRook.firstMove):
                            self.legalMoves.append( (6, 0) )
                    for i in range(1, 4):
                        if piece.causesCheck(self, i, 0, BLACK, board) == True or board.piecesOnBoard[i][0] != None:
                            return
                    prospectiveRook = board.piecesOnBoard[0][0]
                    if not ((prospectiveRook != None and (prospectiveRook.color == BLACK and type(prospectiveRook) == rook) and (prospectiveRook.firstMove))):
                        return
                    self.legalMoves.append( (2, 0) )

                   
class pawn(piece):
    def __init__(self, x: int, y: int, color: PieceColor, board: 'board'): #type: ignore
        self.color = color
        self.x = x
        self.y = y
        self.legalMoves = []
        self.firstMove = False

        if (self.color == BLACK):
            if (self.y == 1):
                self.firstMove = True
        else:
            if (self.y == 6):
                self.firstMove = True

        board.piecesOnBoard[self.x][self.y] = self
        
        if (color == BLACK):
            super().__init__("../res/blackPawn.png")
        else:
            super().__init__("../res/whitePawn.png")

        board.pieceList.append(self)

    def generateMoves(self, board: 'board'): #type: ignore
        self.legalMoves = []
        if self.color == BLACK:
            if (self.y != 7):
                if (self.x + 1 < 8) and board.piecesOnBoard[self.x + 1][self.y + 1] != None and board.piecesOnBoard[self.x + 1][self.y + 1].color != self.color:
                    self.legalMoves.append( (self.x + 1, self.y + 1) )
                if (self.x - 1 >= 0) and board.piecesOnBoard[self.x - 1][self.y + 1] != None and board.piecesOnBoard[self.x - 1][self.y + 1].color != self.color:
                    self.legalMoves.append( (self.x - 1, self.y + 1) )
                if board.piecesOnBoard[self.x][self.y + 1] == None:
                    self.legalMoves.append( (self.x, self.y + 1) )

                
            # double space
            if (self.firstMove == True):
                if board.piecesOnBoard[self.x][self.y + 1] == None and board.piecesOnBoard[self.x][self.y + 2] == None:
                    self.legalMoves.append( (self.x, self.y + 2) )
            
            # taking with en pessant
            for i in (-1, 1):
                if (self.x + i < 8 and self.x + i >= 0) and (self.y < 7):
                    if ( (self.x + i, self.y + 1) == board.enPessantSquare ):
                        self.legalMoves.append( (self.x + i, self.y + 1) )

        elif self.color == WHITE:
            if (self.y != 0):
                if (self.x + 1 < 8) and board.piecesOnBoard[self.x + 1][self.y - 1] != None and board.piecesOnBoard[self.x + 1][self.y - 1].color != self.color:
                    self.legalMoves.append( (self.x + 1, self.y - 1) )
                if (self.x - 1 >= 0) and board.piecesOnBoard[self.x - 1][self.y - 1] != None and board.piecesOnBoard[self.x - 1][self.y - 1].color != self.color:
                    self.legalMoves.append( (self.x - 1, self.y - 1) )
                if board.piecesOnBoard[self.x][self.y - 1] == None:
                    self.legalMoves.append( (self.x, self.y - 1) )
            
            # double space
            if (self.firstMove == True):
                if board.piecesOnBoard[self.x][self.y - 1] == None and board.piecesOnBoard[self.x][self.y - 2] == None:
                    self.legalMoves.append( (self.x, self.y - 2) )

            # taking with en pessant
            for i in (-1, 1):
                if (self.x + i < 8 and self.x + i >= 0) and (self.y > 0):
                    if ( (self.x + i, self.y - 1) == board.enPessantSquare ):
                        self.legalMoves.append( (self.x + i, self.y - 1) )
            
                

class queen(piece):
    def __init__(self, x: int, y, color: int, board: 'board'): #type: ignore
        self.color = color
        self.x = x
        self.y = y
        self.legalMoves = []
        self.firstMove = True

        board.piecesOnBoard[self.x][self.y] = self

        if (color == BLACK):
            super().__init__("../res/blackQueen.png")
        else:
            super().__init__("../res/whiteQueen.png")
        
        board.pieceList.append(self)
    
    def generateMoves(self, board: 'board'): #type: ignore
        self.temp = []
        self.legalMoves = []

        bishop.generateMoves(self, board)
        self.temp = self.legalMoves

        rook.generateMoves(self, board)
        self.legalMoves += self.temp
        

class bishop(piece):
    def __init__(self, x: int, y: int, color: PieceColor, board: 'board'): #type: ignore
        self.color = color
        self.x = x
        self.y = y
        self.legalMoves = []
        self.firstMove = True

        board.piecesOnBoard[self.x][self.y] = self

        if (color == BLACK):
            super().__init__("../res/blackBishop.png")
        else:
            super().__init__("../res/whiteBishop.png")
        
        board.pieceList.append(self)
    
    def generateMoves(self, board: 'board'): #type: ignore
        self.legalMoves = []
        
        # up-right
        i = 1
        j = 1
        while True:
            if (self.x + i < 8 and self.y - j >= 0):
                if (board.piecesOnBoard[self.x + i][self.y - j] == None): 
                    self.legalMoves.append( (self.x + i, self.y - j) )
                elif (board.piecesOnBoard[self.x + i][self.y - j] != None):
                    if (board.piecesOnBoard[self.x + i][self.y - j].color != self.color):
                        self.legalMoves.append( (self.x + i, self.y - j) )
                    break               
            else:
                break
            i += 1
            j += 1
        
        # up-left
        i = 1
        j = 1
        while True:
            if (self.x - i >= 0 and self.y - j >= 0):
                if (board.piecesOnBoard[self.x - i][self.y - j] == None): 
                    self.legalMoves.append( (self.x - i, self.y - j) )
                elif (board.piecesOnBoard[self.x - i][self.y - j] != None):
                    if (board.piecesOnBoard[self.x - i][self.y - j].color != self.color):
                        self.legalMoves.append( (self.x - i, self.y - j) )
                    break               
            else:
                break
            i += 1
            j += 1
            
        # down-left
        i = 1
        j = 1
        while True:
            if (self.x - i >= 0 and self.y + j < 8):
                if (board.piecesOnBoard[self.x - i][self.y + j] == None): 
                    self.legalMoves.append( (self.x - i, self.y + j) )
                elif (board.piecesOnBoard[self.x - i][self.y + j] != None):
                    if (board.piecesOnBoard[self.x - i][self.y + j].color != self.color):
                        self.legalMoves.append( (self.x - i, self.y + j) )
                    break               
            else:
                break
            i += 1
            j += 1

        # down-right
        i = 1
        j = 1
        while True:
            if (self.x + i < 8 and self.y + j < 8):
                if (board.piecesOnBoard[self.x + i][self.y + j] == None): 
                    self.legalMoves.append( (self.x + i, self.y + j) )
                elif (board.piecesOnBoard[self.x + i][self.y + j] != None):
                    if (board.piecesOnBoard[self.x + i][self.y + j].color != self.color):
                        self.legalMoves.append( (self.x + i, self.y + j) )
                    break               
            else:
                break
            i += 1
            j += 1

class rook(piece):
    def __init__(self, x: int, y: int, color: PieceColor, board: 'board'): #type: ignore
        self.color = color
        self.x = x
        self.y = y
        self.legalMoves = []
        self.firstMove = True

        board.piecesOnBoard[self.x][self.y] = self

        if (color == BLACK):
            super().__init__("../res/blackRook.png")
        else:
            super().__init__("../res/whiteRook.png")
        
        board.pieceList.append(self)

    def generateMoves(self, board: 'board'): #type: ignore
        self.legalMoves = []

        # right, x increases
        i = 1
        while True:
            if (self.x + i < 8):
                if (board.piecesOnBoard[self.x + i][self.y] == None): 
                    self.legalMoves.append( (self.x + i, self.y) )
                elif (board.piecesOnBoard[self.x + i][self.y] != None):
                    if (board.piecesOnBoard[self.x + i][self.y].color != self.color):
                        self.legalMoves.append( (self.x + i, self.y) )
                    break               
            else:
                break
            i += 1
                
        # left, x decreases
        i = 1
        while True:
            if (self.x - i >= 0):
                if (board.piecesOnBoard[self.x - i][self.y] == None): 
                    self.legalMoves.append( (self.x - i, self.y) )
                elif (board.piecesOnBoard[self.x - i][self.y] != None):
                    if (board.piecesOnBoard[self.x - i][self.y].color != self.color):
                        self.legalMoves.append( (self.x - i, self.y) )
                    break              
            else:
                break
            i += 1
        
        # up, y decreases
        i = 1
        while True:
            if (self.y - i >= 0):
                if (board.piecesOnBoard[self.x][self.y - i] == None): 
                    self.legalMoves.append( (self.x, self.y - i) )
                elif (board.piecesOnBoard[self.x][self.y - i] != None):
                    if (board.piecesOnBoard[self.x][self.y - i].color != self.color):
                        self.legalMoves.append( (self.x, self.y - i) )
                    break
               
            else:
                break
            i += 1

        # down, y increases
        i = 1
        while True:
            if (self.y + i < 8):
                if (board.piecesOnBoard[self.x][self.y + i] == None): 
                    self.legalMoves.append( (self.x, self.y + i) )
                elif (board.piecesOnBoard[self.x][self.y + i] != None):
                    if (board.piecesOnBoard[self.x][self.y + i].color != self.color):
                        self.legalMoves.append( (self.x, self.y + i) )
                    break               
            else:
                break
            i += 1

    
class knight(piece):
    def __init__(self, x: int, y: int, color: PieceColor, board: 'board'): #type: ignore
        self.color = color
        self.x = x
        self.y = y
        self.legalMoves = []
        self.firstMove = True

        board.piecesOnBoard[self.x][self.y] = self

        if (color == BLACK):
            super().__init__("../res/blackKnight.png")
        else:
            super().__init__("../res/whiteKnight.png")
        
        board.pieceList.append(self)
    
    def generateMoves(self, board: 'board'): #type: ignore
            self.legalMoves = []

            #     o
            # o o o
            if (self.x + 2 < 8 and self.y - 1 >= 0):
                square = board.piecesOnBoard[self.x + 2][self.y - 1]
                if (square == None):
                    self.legalMoves.append( (self.x + 2, self.y - 1) )
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x + 2, self.y - 1) )

            # o
            # o o o
            if (self.x - 2 >= 0 and self.y - 1 >= 0):
                square = board.piecesOnBoard[self.x - 2][self.y - 1]
                if (square == None):
                    self.legalMoves.append( (self.x - 2, self.y - 1) )
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x - 2, self.y - 1) )

            #   o
            #   o
            # o o
            if (self.x + 1 < 8 and self.y - 2 >= 0):
                square = board.piecesOnBoard[self.x + 1][self.y - 2]
                if (square == None):
                    self.legalMoves.append( (self.x + 1, self.y - 2) )
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x + 1, self.y - 2) )
            
            # o
            # o
            # o o
            if (self.x - 1 >= 0 and self.y - 2 >= 0):
                square = board.piecesOnBoard[self.x - 1][self.y - 2]
                if (square == None):
                    self.legalMoves.append( (self.x - 1, self.y - 2) )
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x - 1, self.y - 2) )
            
            # o o o
            #     o
            if (self.x + 2 < 8 and self.y + 1 < 8):
                square = board.piecesOnBoard[self.x + 2][self.y + 1]
                if (square == None):
                    self.legalMoves.append( (self.x + 2, self.y + 1) )
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x + 2, self.y + 1) )
            
            # o o o
            # o
            if (self.x - 2 >= 0 and self.y + 1 < 8):
                square = board.piecesOnBoard[self.x - 2][self.y + 1]
                if (square == None):
                    self.legalMoves.append( (self.x - 2, self.y + 1) )
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x - 2, self.y + 1) )
            
            # o o
            # o
            # o
            if (self.x - 1 >= 0 and self.y + 2 < 8):
                square = board.piecesOnBoard[self.x - 1][self.y + 2]
                if (square == None):
                    self.legalMoves.append( (self.x - 1, self.y + 2))
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x - 1, self.y + 2) )

            # o o
            #   o
            #   o
            if (self.x + 1 < 8 and self.y + 2 < 8):
                square = board.piecesOnBoard[self.x + 1][self.y + 2]
                if (square == None):
                    self.legalMoves.append( (self.x + 1, self.y + 2) )
                else:
                    if (square.color != self.color):
                        self.legalMoves.append( (self.x + 1, self.y + 2) )
