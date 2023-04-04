import numpy as np
from ortools.sat.python import cp_model

from sudoku_data import SudokuData


class SudokuSolver:
    """数独ソルバークラス
    """

    def __init__(self, data: SudokuData, options: dict) -> None:
        self.hint = data.hint
        self.options = options

    def preprocess(self) -> None:
        """前処理
        """
        pass

    def modeling(self) -> None:
        """モデリング

        1. モデルオブジェクトの作成
        2. 決定変数の定義
        3. 制約条件の定義
        4. 求解
        """
        self.model = cp_model.CpModel()

        # 決定変数
        self.rows = range(9)
        self.cols = range(9)
        self.x = [[self.model.NewIntVar(lb=0, ub=8, name=f"x[{row}, {col}]")
                   for row in self.rows] for col in self.cols]

        # 制約条件
        ## 制約条件①：行方向に見た時に、同じ数字は入らない
        for row in self.rows:
            self.model.AddAllDifferent([self.x[row][col] for col in self.cols])

        ## 制約条件②：列方向に見た時に、同じ数字は入らない
        for col in self.cols:
            self.model.AddAllDifferent([self.x[row][col] for row in self.rows])

        ## 制約条件③：3×3のマスの中に同じ数字は入らない
        for r in [0, 3, 6]:
            for c in [0, 3, 6]:
                self.model.AddAllDifferent([self.x[r+i][c+j] for i in range(3) for j in range(3)])

        ## 制約条件④：既に数字が入っているマスは数字が固定
        for row in self.rows:
            for col in self.cols:
                if self.hint[row, col] != 0:
                    self.model.Add(self.x[row][col] == self.hint[row, col] - 1)

        # 求解
        self.solver = cp_model.CpSolver()
        self.status = self.solver.Solve(self.model)

    def postprocess(self):
        """後処理

        求められた決定変数をnp.array型の変数に変換する
        """
        self.solution = np.empty((9, 9))
        for row in self.rows:
            for col in self.cols:
                self.solution[row][col] = self.solver.Value(self.x[row][col]) + 1
        self.solution = self.solution.astype(int)

    def display_data(self, display_data: np.array) -> None:
        """引数で受け取ったデータを9×9の表で表示する

        Args:
            display_data (np.array): 表示するデータ
        """
        data = display_data.astype(str)
        data[data == "0"] = "_"
        print("┌" + "─"*7 + "┬" + "─"*7 + "┬" + "─"*7 + "┐")
        for row in range(9):
            print("│", end=" ")
            for col in range(9):
                if (col + 1) % 3 == 0:
                    if col == 8:
                        print(data[row, col], end=" ")
                    else:
                        print(data[row, col], end=" │ ")
                else:
                    print(data[row, col], end=" ")
            print("│")
            if ((row + 1) % 3 == 0) and not row == 8:
                print("├" + "─"*7 + "┼" + "─"*7 + "┼" + "─"*7 + "┤")
        print("└" + "─"*7 + "┴" + "─"*7 + "┴" + "─"*7 + "┘")

    def display_solution(self) -> None:
        """数独の問題データと最適化で求めた結果を並べて表示する
        """
        hint = self.hint.astype(str)
        hint[hint == "0"] = "_"
        solution = self.solution
        print("┌" + "─"*7 + "┬" + "─"*7 + "┬" + "─"*7 + "┐" + "   " + "┌" + "─"*7 + "┬" + "─"*7 + "┬" + "─"*7 + "┐")
        for row in range(9):
            print("│", end=" ")
            for col in range(9):
                if (col + 1) % 3 == 0:
                    if col == 8:
                        print(hint[row, col], end=" ")
                    else:
                        print(hint[row, col], end=" │ ")
                else:
                    print(hint[row, col], end=" ")
            if row == 4:
                print("│", end=" → ")
            else:
                print("│", end="   ")
            print("│", end=" ")
            for col in range(9):
                if (col + 1) % 3 == 0:
                    if col == 8:
                        print(solution[row, col], end=" ")
                    else:
                        print(solution[row, col], end=" │ ")
                else:
                    print(solution[row, col], end=" ")
            print("│")
            if ((row + 1) % 3 == 0) and not row == 8:
                print("├" + "─"*7 + "┼" + "─"*7 + "┼" + "─"*7 + "┤" + "   " + "├" + "─"*7 + "┼" + "─"*7 + "┼" + "─"*7 + "┤")
        print("└" + "─"*7 + "┴" + "─"*7 + "┴" + "─"*7 + "┘" + "   " + "└" + "─"*7 + "┴" + "─"*7 + "┴" + "─"*7 + "┘")


if __name__ == "__main__":
    sudoku_data = SudokuData()
    sudoku_data.get_data()

    solver = SudokuSolver(sudoku_data, options=None)
    solver.preprocess()
    solver.modeling()
    solver.postprocess()
    solver.display_solution()
