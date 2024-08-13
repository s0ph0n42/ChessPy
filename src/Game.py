import pygame
import Board
import Computer
import Human
from Player import Player

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SQUARE_SIZE = 128

# shortened enums
WHITE = __import__('Globals').PieceColor.WHITE
BLACK = __import__('Globals').PieceColor.BLACK

CPUONLY = __import__('Globals').GameMode.CPUONLY
HUMANCPU = __import__('Globals').GameMode.HUMANCPU
HUMANONLY = __import__('Globals').GameMode.HUMANONLY

BOARDCOLORS = [(70, 130, 180), (255, 248, 223)]

class Game:
    def __init__(self, mode: str):
        self.running = True

        self.mode = mode
        self.winner = None
        self.stalemate = False
        self.position = 0
        self.player1 = None
        self.player2 = None

        self.board = None
        computer = None

    def run(self):
        pygame.init()
        pygame.font.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess")

        self.board = Board.board(screen)
        self.board.initializePieces()

        if self.mode == CPUONLY:
            player1 = Computer.Computer(WHITE)
            player2 = Computer.Computer(BLACK)
            self.runCPUONLY(player1, player2, screen)

        elif self.mode == HUMANCPU:
            player1 = Human.Human(WHITE)
            player2 = Computer.Computer(BLACK)
            self.runHUMANCPU(player1, player2, screen)

        elif self.mode == HUMANONLY:
            player1 = Human.Human(WHITE)
            player2 = Human.Human(BLACK)
            self.runHUMANONLY(player1, player2, screen)
      

    def runHUMANONLY(self, player1: Human, player2: Human, screen):
        whiteTurn = True
        
        while self.running:
            screen.fill((255, 255, 255))
            self.board.drawBoard(screen, BOARDCOLORS)
            self.board.drawPieces(screen)

            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.winner != None or self.stalemate:
                        break
                    
                    clickedSquare = Board.board.getClickedSquare(SQUARE_SIZE)
                    clickedPiece = self.board.getPieceOnSquare(clickedSquare)
                    
                    if whiteTurn:
                        if player1.makeMove(clickedPiece, self.board):
                            whiteTurn = not whiteTurn
                    else:
                        if player2.makeMove(clickedPiece, self.board):
                            whiteTurn = not whiteTurn
                    
                    if (whiteTurn and self.board.isStalemate(WHITE)) or (not whiteTurn and self.board.isStalemate(BLACK)):
                        self.stalemate = True
                        print("Draw by stalemate")
                        break

                    self.winner = self.board.isCheckmate(WHITE) if whiteTurn else self.board.isCheckmate(BLACK)
                    if self.winner != None:
                        print(self.winner, "is the winner")

                if event.type == pygame.QUIT:
                    self.running = False


            pygame.display.update()

    def runHUMANCPU(self, player1: Human, player2: Computer, screen):
        ''' Assumes player1 is white and is the human '''
        whiteTurn = True
        
        while self.running:
            screen.fill((255, 255, 255))
            self.board.drawBoard(screen, BOARDCOLORS)
            self.board.drawPieces(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.winner != None or self.stalemate:
                        break
                    
                    clickedSquare = Board.board.getClickedSquare(SQUARE_SIZE)
                    clickedPiece = self.board.getPieceOnSquare(clickedSquare)
                    
                    if whiteTurn:
                        if player1.makeMove(clickedPiece, self.board):
                            whiteTurn = not whiteTurn
                    
                    if (whiteTurn and self.board.isStalemate(WHITE)) or (not whiteTurn and self.board.isStalemate(BLACK)):
                        self.stalemate = True
                        print("Draw by stalemate")
                        break

                    self.winner = self.board.isCheckmate(WHITE) if whiteTurn else self.board.isCheckmate(BLACK)
                    if self.winner != None:
                        print(self.winner, "is the winner")

                if event.type == pygame.QUIT:
                    self.running = False

            if self.winner != None or self.stalemate:
                pygame.display.update()
                continue

            if not whiteTurn:
                player2.makeMove(None, self.board)
                whiteTurn = not whiteTurn

            if (whiteTurn and self.board.isStalemate(WHITE)) or (not whiteTurn and self.board.isStalemate(BLACK)):
                self.stalemate = True
                print("Draw by stalemate")
                continue

            self.winner = self.board.isCheckmate(WHITE) if whiteTurn else self.board.isCheckmate(BLACK)
            if self.winner != None:
                print(self.winner, "is the winner")

            pygame.display.update()

    def runCPUONLY(self, player1: Computer, player2: Computer, screen):
        ''' Assumes player1 is white and player2 is black '''
        whiteTurn = True
        paused = False
        
        while self.running:
            screen.fill((255, 255, 255))
            self.board.drawBoard(screen, BOARDCOLORS)
            self.board.drawPieces(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    paused = not paused
                    pygame.event.clear()
                    pass

            pygame.display.update()
            
            if paused:
                continue

            if self.winner != None:
                continue

            if (whiteTurn):
                player1.makeMove(None, self.board)
            else:
                player2.makeMove(None, self.board)
            
            whiteTurn = not whiteTurn

            if (whiteTurn and self.board.isStalemate(WHITE)) or (not whiteTurn and self.board.isStalemate(BLACK)):
                self.stalemate = True
                self.winner = "stalemate"
                print("Draw by stalemate")
                continue

            self.winner = self.board.isCheckmate(WHITE) if whiteTurn else self.board.isCheckmate(BLACK)
            if self.winner != None:
                print(self.winner, "is the winner")
                continue
        
