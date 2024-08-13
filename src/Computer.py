import Player
from Piece import *
from Board import board
from typing import Optional
import random

class Computer(Player.Player):
    def __init__(self, color, model=None):
        self.color = color
        self.model = model # can be Stockfish, or custom
    
    def makeMove(self, clickedPiece: Optional[piece], board: board) -> bool:
        self.makeRandomMove(board)
        return True
    
    def makeRandomMove(self, board: board):
        randomPiece = self.pickRandomPiece(board)
        randomMove = self.pickRandomMove(randomPiece, board)
        while (not randomMove):
            randomPiece = self.pickRandomPiece(board)
            randomMove = self.pickRandomMove(randomPiece, board)
        board.makeMove(randomPiece, randomMove)

    def pickRandomPiece(self, board: board) -> piece:
        chosenPiece = None
        while (not chosenPiece):
            currentChoice = random.choice(board.pieceList)
            if (currentChoice.color == self.color):
                chosenPiece = currentChoice
        return chosenPiece
    
    def pickRandomMove(self, piece: piece, board: board) -> Optional[tuple]:
        piece.generateLegalMoves(board)
        return None if len(piece.legalMoves) == 0 else random.choice(piece.legalMoves)
    
    def makeStockfishMove(self):
        pass
    
    def translateStockfishMove(self):
        pass
    
        
        
