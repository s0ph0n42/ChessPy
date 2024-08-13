import pygame
from Piece import *
from typing import Optional

# shortened enums
WHITE = __import__('Globals').PieceColor.WHITE
BLACK = __import__('Globals').PieceColor.BLACK

class board:
    ''' Note: board coordinates are (0, 0) for top left and (7, 7) for bottom right '''
    def __init__(self, screen):
        self.piecesOnBoard = [[None for j in range(8)] for i in range(8)]
        self.pieceList = []
        self.whiteTurn = True
        self.history = []
        self.screen = screen
        self.enPessantSquare = None
        self.turn = 0

    
    def noMovesPossible(self, color: PieceColor) -> bool:
        for savior in self.pieceList:
            if savior.color == color:
                savior.generateLegalMoves(self)
                if (len(savior.legalMoves) != 0):
                    return False
        return True

    def isCheckmate(self, color: PieceColor) -> Optional[PieceColor]:
        ''' Returns the winning color if applicable, else returns False '''
        if (color == WHITE):
            if (self.noMovesPossible(WHITE) and piece.inCheck(WHITE, self, self.pieceList)):
                return BLACK
        if (color == BLACK):
            if (self.noMovesPossible(BLACK) and piece.inCheck(BLACK, self, self.pieceList)):
                return WHITE
        return None
    
    def isStalemate(self, color: PieceColor) -> bool:
        if (piece.inCheck(color, self, self.pieceList)):
            return False
        
        if (not self.noMovesPossible(color)):
            return False

        return True
    
    # TODO: add 50 move draw rule
    def drawBy50Moves(self):
        pass

    # TODO: add threefold repetition rule
    def drawByThreefold(self):
        pass

    # TODO: add draw by insufficient material
    def drawByInsufficientMaterial(self):
        pass
        

    @staticmethod
    def getClickedSquare(SQUARESIZE: int) -> Optional[tuple]:
        coords = pygame.mouse.get_pos();

        return (coords[0] // SQUARESIZE, coords[1] // SQUARESIZE)
    
    def getPieceOnSquare(self, coord: tuple) -> Optional[piece]:
        return self.piecesOnBoard[coord[0]][coord[1]]
    
    def drawBoard(self, screen, colors: tuple):
        for i in range(0, 8):
            if (i % 2 == 0):
                colorIndex = 0
            else:
                colorIndex = 1
                
            for j in range(0, 8):
                color = colors[colorIndex]

                rect = pygame.Rect(128*i, 128*j, 128, 128)
                pygame.draw.rect(screen, color, rect)
                
                colorIndex = (colorIndex + 1) % 2

        self.drawColRowLabels(screen)
    
    def drawColRowLabels(self, screen):
        ''' Draw row and column annotations, i.e. a-h and 1-8'''
        for i in range(8):
            screen.blit(pygame.font.SysFont('Times New Roman', 18).render(chr(97 + i), False, (0, 0, 0)), (5 + (i+0.78)*128, 5))
            screen.blit(pygame.font.SysFont('Times New Roman', 18).render(chr(56 - i), False, (0, 0, 0)), (5, 5 + (i+0.78)*128))

    def drawPieces(self, screen):
        for piece in self.pieceList:
            screen.blit(piece.image, (piece.x*128, piece.y*128))

    #TODO: add halfmove field and fullmove field
    def getFEN(self) -> str:
        ''' Returns FEN representation of current board instance '''
        castle = ""
        fen = ""
        row = ""
        for i in range(8):
            row = ""
            space_count = 0
            for j in range(8):
                if self.piecesOnBoard[j][i] != None:
                    if (space_count != 0):
                        row += str(space_count)
                        space_count = 0

                    piece_type = ""

                    if (type(self.piecesOnBoard[j][i]) is rook):
                        piece_type = "r"
                    elif (type(self.piecesOnBoard[j][i]) is knight):
                        piece_type = "n"
                    elif (type(self.piecesOnBoard[j][i]) is bishop):
                        piece_type = "b"
                    elif (type(self.piecesOnBoard[j][i]) is queen):
                        piece_type = "q"
                    elif (type(self.piecesOnBoard[j][i]) is king):
                        piece_type = "k"
                        if self.piecesOnBoard[j][i].firstMove == True:
                            if self.piecesOnBoard[j][i].color == WHITE:
                                castle += "QK"
                            else:
                                castle += "qk"
                    elif (type(self.piecesOnBoard[j][i]) is pawn):
                        piece_type = "p"
                    
                    if (self.piecesOnBoard[j][i].color == WHITE):
                        piece_type = piece_type.upper()
                    
                    row += piece_type
                    
                else:
                    space_count += 1

            if (space_count != 0):
                row += str(space_count)

            fen += row
            fen += "/"
        fen = fen[:-1]

        if (self.whiteTurn):
            fen += " w"
        else:
            fen += " b"
        
        if castle == "":
            fen += " -"
        else:
            fen = fen + " " + castle

        if (self.enPessantSquare != None):
            fen += f" {self.coordinateToAlgebraic(self.enPessantSquare)}"
        else:
            fen += " -"

        return fen
    
    #TODO: add halfmove field and fullmove field
    def setFEN(self, fen: str, first: bool = False) -> None:
        ''' Sets current board state based on given FEN. first can be 
            set to true if this is the game's starting state. '''
        self.pieceList = []
        self.piecesOnBoard = [[None for j in range(8)] for i in range(8)]

        parsedFen = fen.replace("/", "").split() # splits by spaces
        count = 0

        boardString = parsedFen[0]
        turn = parsedFen[1]
        validCastles = parsedFen[2]
        enPessantField = parsedFen[3]

        if (enPessantField != "-"):
            self.enPessantSquare = self.algebraicToCoordinate(enPessantField)

        if (turn != "w"):
            self.whiteTurn = False
        else:
            self.whiteTurn = True

        for i in range(len(boardString)):
            c = boardString[i]
            if (ord(c) < 57):
                count += ord(c) - 48
                continue
            if (c == c.upper()):
                match c:
                    case "R":
                        r = rook(count % 8, count // 8, WHITE, self)
                    case "N":
                        n = knight(count % 8, count // 8, WHITE, self)
                    case "B":
                        b = bishop(count % 8, count // 8, WHITE, self)
                    case "Q":
                        q = queen(count % 8, count // 8, WHITE, self)
                    case "K":
                        k = king(count % 8, count // 8, WHITE, self)
                        if ("Q" not in validCastles and "K" not in validCastles):
                            k.firstMove = False
                        else:
                            k.firstMove = True
                    case "P":
                        p = pawn(count % 8, count // 8, WHITE, self)
            else:
                match c:
                    case "r":
                        r = rook(count % 8, count // 8, BLACK, self)
                    case "n":
                        n = knight(count % 8, count // 8, BLACK, self)
                    case "b":
                        b = bishop(count % 8, count // 8, BLACK, self)
                    case "q":
                        q = queen(count % 8, count // 8, BLACK, self)
                    case "k":
                        k = king(count % 8, count // 8, BLACK, self)
                        if ("q" not in validCastles and "k" not in validCastles):
                            k.firstMove = False
                        else:
                            k.firstMove = True
                    case "p":
                        p = pawn(count % 8, count // 8, BLACK, self)
            count += 1

        if (first):
            self.history.append(fen)

    def initializePieces(self):
        self.setFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w QKqk -", True)

    def shadeSquare(self, screen, x: int, y: int):
        screen.blit(pygame.image.load("../res/translucentRed.png"), (x*128, y*128))

    def removeFromSquare(self, clickedSquare: tuple) -> bool:
        ''' Removes piece from given square and returns true if removal took place
            false otherwise '''
        x, y = clickedSquare[0], clickedSquare[1]
        
        if (self.piecesOnBoard[x][y] != None):
            self.pieceList.remove(self.piecesOnBoard[x][y])
            self.piecesOnBoard[x][y] = None
            return True
        return False

    def makeMove(self, clickedPiece: piece, endingSquare: tuple):
        ''' Performs the move on the GUI, deals with updating internal board
            representation '''
        
        startX, startY = clickedPiece.x, clickedPiece.y
        endX, endY = endingSquare[0], endingSquare[1]

        if (type(clickedPiece) == pawn):
            if (startY - endY == 2):
                self.enPessantSquare = (startX, startY - 1)
            elif (startY - endY == -2):
                self.enPessantSquare = (startX, startY + 1)

            if (self.handlePawnMove(clickedPiece, endingSquare)):
                self.endTurn()
                return
        else:
            self.enPessantSquare = None
         
        if (type(clickedPiece) == king):
            if (self.handleKingMove(clickedPiece, endingSquare)):
                self.endTurn()
                return

        if (type(clickedPiece) == rook):
            self.handleRookMove(clickedPiece, endingSquare)
        
        if (self.piecesOnBoard[endingSquare[0]][endingSquare[1]]):
            self.removeFromSquare(endingSquare)
        
        
        self.piecesOnBoard[startX][startY] = None

        clickedPiece.x, clickedPiece.y = endX, endY
        self.piecesOnBoard[endX][endY] = clickedPiece

        self.endTurn()

    def handleKingMove(self, clickedKing: king, endingSquare: tuple) -> bool:
        ''' Returns if castling was performed or not '''

        startX, startY = clickedKing.x, clickedKing.y
        endX, endY = endingSquare[0], endingSquare[1]

        if (startX - endX == -2):
            if (self.performKingsideCastle(clickedKing, endingSquare)):
                clickedKing.firstMove = False
                return True
        elif (startX - endX == 2):
            if (self.performQueensideCastle(clickedKing, endingSquare)):
                clickedKing.firstMove = False
                return True
        else:
            clickedKing.firstMove = False
        
        return False

    def performKingsideCastle(self, clickedKing: king, endingSquare: tuple) -> bool:
        ''' Returns if kingside castling was performed '''
        startX, startY = clickedKing.x, clickedKing.y
        endX, endY = endingSquare[0], endingSquare[1]

        prospectiveRook = self.getPieceOnSquare((endX + 1, endY))
        if (type(prospectiveRook) == rook and prospectiveRook.color == clickedKing.color and prospectiveRook.firstMove):
            rookX, rookY = prospectiveRook.x, prospectiveRook.y
            self.piecesOnBoard[rookX][rookY] = None
            
            prospectiveRook.x, prospectiveRook.y = startX + 1, rookY
            self.piecesOnBoard[startX + 1][rookY] = prospectiveRook

            prospectiveRook.firstMove = False

            self.piecesOnBoard[startX][startY] = None
            clickedKing.x, clickedKing.y = endX, endY
            self.piecesOnBoard[endX][endY] = clickedKing
            return True
        
        return False

    def performQueensideCastle(self, clickedKing: king, endingSquare: tuple) -> bool:
        ''' Returns if queenside castling was performed '''
        startX, startY = clickedKing.x, clickedKing.y
        endX, endY = endingSquare[0], endingSquare[1]

        prospectiveRook = self.getPieceOnSquare((endX - 2, endY))
        if (type(prospectiveRook) == rook and prospectiveRook.color == clickedKing.color and prospectiveRook.firstMove):
            rookX, rookY = prospectiveRook.x, prospectiveRook.y
            self.piecesOnBoard[rookX][rookY] = None

            prospectiveRook.x, prospectiveRook.y = startX - 1, rookY
            self.piecesOnBoard[startX - 1][rookY] = prospectiveRook
            prospectiveRook.firstMove = False

            self.piecesOnBoard[startX][startY] = None
            clickedKing.x, clickedKing.y = endX, endY
            self.piecesOnBoard[endX][endY] = clickedKing
            return True
        
        return False

    
    def handleRookMove(self, clickedRook: rook, endingSquare: tuple):
        if (clickedRook.firstMove):
            clickedRook.firstMove = False

    def handlePawnMove(self, clickedPawn: pawn, endingSquare: tuple) -> bool:
        ''' Returns if pawn promotion or en pessant was performed '''

        startX, startY = clickedPawn.x, clickedPawn.y
        endX, endY = endingSquare[0], endingSquare[1]

        if (startY - endY == 2):
            self.enPessantSquare = (startX, startY - 1)
        elif (startY - endY == -2):
            self.enPessantSquare = (startX, startY + 1)
        else:
            self.enPessantSquare = None

        if (clickedPawn.firstMove):
            clickedPawn.firstMove = False
        
        #TODO: Make other pieces options during pawn promotion
        if (clickedPawn.color == BLACK and endY == 7) or (clickedPawn.color == WHITE and endY == 0):
            self.removeFromSquare( (endX, endY) )
            self.removeFromSquare( (clickedPawn.x, clickedPawn.y) )
            clickedPawn = queen(endingSquare[0], endingSquare[1], clickedPawn.color, self)
            return True

        
        if (self.getPieceOnSquare(endingSquare) == None and startX != endX):
            self.handleEnPessant(clickedPawn, endingSquare)
            return True

        return False
    
    def handleEnPessant(self, clickedPawn: pawn, endingSquare: tuple):
        startX, startY = clickedPawn.x, clickedPawn.y
        endX, endY = endingSquare[0], endingSquare[1]

        if (startX > endX):
            if (clickedPawn.color == BLACK):
                self.removeFromSquare((endX, endY - 1))
            else:
                self.removeFromSquare((endX, endY + 1))
        else:
            if (clickedPawn.color == WHITE):
                self.removeFromSquare((endX, endY + 1))
            else:
                self.removeFromSquare((endX, endY - 1))

        self.piecesOnBoard[startX][startY] = None

        clickedPawn.x, clickedPawn.y = endX, endY
        self.piecesOnBoard[endX][endY] = clickedPawn
    
    def endTurn(self):
        ''' Updates board history with new FEN string, increments board turn '''
        self.history.append(self.getFEN())
        self.turn += 1
        self.whiteTurn = not self.whiteTurn

    def algebraicToCoordinate(self, alg: str) -> tuple:
        ''' Takes a board square in algebraic notation and converts it to equivalent 
            ending square in coordinate notation. '''
        destinationRow = ord(alg[-2]) - 97
        destinationCol = 8 - int(alg[-1])

        return (destinationRow, destinationCol)
    
    def coordinateToAlgebraic(self, coord: tuple) -> str:
        ''' Takes a board square in coordinate notation and converts it to equivalent 
            ending square in algebraic notation. '''
        alg = ""
        alg += chr(coord[0] + 97)
        alg += str(8 - coord[1])
        return alg

    def shadeSquare(self, square: tuple, color: str):
        if color == "red":
            self.screen.blit(pygame.image.load("../res/translucentRed.png"), (square[0]*128, square[1]*128))
        elif color == "blue":
            self.screen.blit(pygame.image.load("../res/translucentBlue.png"), (square[0]*128, square[1]*128))






