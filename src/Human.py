import pygame
import Player
import Game
from Piece import piece
from Board import board
from typing import Optional

class Human(Player.Player):
    def __init__(self, color):
        self.color = color
    
    def makeMove(self, clickedPiece: Optional[piece], board: board) -> bool:
        ''' Takes the first click as input, waits for the second click
        Based on the two clicks, if the resulting move is legal, true
        is returned. Else false is returned. '''
        clickedSquare = None


        if (clickedPiece == None or clickedPiece.color != self.color):
            return False
        
        board.shadeSquare((clickedPiece.x, clickedPiece.y), "blue")

        clickedPiece.generateLegalMoves(board)
        legalMoves = clickedPiece.legalMoves

        for move in legalMoves:
            board.shadeSquare(move, "red")
        
        pygame.event.clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickedSquare = board.getClickedSquare(Game.SQUARE_SIZE)

                    if (clickedSquare in legalMoves):
                        board.makeMove(clickedPiece, clickedSquare)
                        return True
                    return False
                
                if event.type == pygame.QUIT:
                    exit(0)

            pygame.display.update()


                    
                    
                











