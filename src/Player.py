from abc import ABC
from abc import abstractmethod
from Piece import piece
from typing import Optional


class Player(ABC):
    @abstractmethod
    def makeMove(self, clickedPiece: Optional[piece], board: 'Board') -> bool:# type: ignore
        '''Intended to handle all pygame mouse click/drag events until a legal move has been made'''
        pass

