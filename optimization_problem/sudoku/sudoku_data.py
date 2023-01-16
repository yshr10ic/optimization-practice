import numpy as np


class SudokuData:
    def __init__(self) -> None:
        self.hint = None

    def get_data(self) -> None:
        self.hint = np.array([
            [0, 0, 9, 0, 0, 8, 0, 0, 0],
            [1, 0, 6, 0, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 3, 0, 2],
            [0, 0, 0, 5, 7, 0, 0, 0, 0],
            [4, 3, 0, 0, 0, 0, 0, 0, 9],
            [0, 9, 8, 0, 0, 3, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 7, 4],
            [6, 0, 0, 0, 0, 0, 8, 0, 0],
            [5, 4, 0, 0, 0, 0, 0, 0, 3]
        ])
