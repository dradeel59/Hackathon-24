import tkinter as tk
from tkinter import messagebox
import random

class SudokuApp:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Application")

        self.menu_screen()

    def menu_screen(self):
        self.clear_screen()

        self.menu_label = tk.Label(self.master, text="Welcome to Sudoku Solver", font=("Helvetica", 16))
        self.menu_label.pack(pady=20)

        self.play_button = tk.Button(self.master, text="Play Sudoku", command=self.sudoku_screen, width=20, height=2)
        self.play_button.pack(pady=10)

    def sudoku_screen(self):
        self.clear_screen()
        self.sudoku_gui = SudokuGUI(self.master)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

class SudokuGUI:
    def __init__(self, master):
        self.master = master

        self.cells = [[tk.Entry(master, width=5, justify='center') for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.cells[i][j].grid(row=i, column=j)

        self.solve_button = tk.Button(master, text="Solve", command=self.solve)
        self.solve_button.grid(row=9, column=2)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear)
        self.clear_button.grid(row=9, column=3)

        self.generate_button = tk.Button(master, text="Generate", command=self.generate)
        self.generate_button.grid(row=9, column=4)

        self.check_button = tk.Button(master, text="Check", command=self.check)
        self.check_button.grid(row=9, column=5)

        self.hint_button = tk.Button(master, text="Hint", command=self.hint)

    def get_board(self):
        board = []
        for row in self.cells:
            board.append([int(cell.get() or 0) for cell in row])
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.cells[i][j].insert(0, str(board[i][j]))

    def clear(self):
        for row in self.cells:
            for cell in row:
                cell.delete(0, tk.END)

    def solve(self):
        board = self.get_board()
        if self.solve_sudoku(board):
            self.set_board(board)
            messagebox.showinfo("Success", "The Sudoku puzzle has been solved!")
        else:
            messagebox.showerror("Error", "No solution exists for the given puzzle.")

    def generate(self):
        board = self.generate_sudoku()
        self.set_board(board)

    def check(self):
        board = self.get_board()
        if self.is_complete(board):
            messagebox.showinfo("Success", "Congratulations! You have completed the Sudoku correctly.")
        else:
            messagebox.showerror("Error", "The Sudoku puzzle is not solved correctly.")

    def is_complete(self, board):
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num == 0 or not self.is_valid(board, num, row, col):
                    return False
        return True

    def generate_sudoku(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        # Fill the diagonal 3x3 boxes to ensure the puzzle is valid
        for i in range(0, 9, 3):
            self.fill_box(board, i, i)
        # Fill the rest of the board
        self.solve_sudoku(board)
        # Remove elements to leave only nine unique digits
        self.keep_only_unique_elements(board)
        return board

    def fill_box(self, board, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[row+i][col+j] = nums.pop()

    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(board, num, row, col):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0

        return False

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, row, col):
        # Check row and column
        for i in range(9):
            if (board[row][i] == num and i != col) or (board[i][col] == num and i != row):
                return False

        # Check 3x3 box
        box_x = row // 3
        box_y = col // 3
        for i in range(box_x * 3, box_x * 3 + 3):
            for j in range(box_y * 3, box_y * 3 + 3):
                if board[i][j] == num and (i != row or j != col):
                    return False

        return True

    def keep_only_unique_elements(self, board):
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_positions)
        
        unique_elements = list(range(1, 10))
        random.shuffle(unique_elements)
        
        filled_positions = []
        
        for num in unique_elements:
            for r, c in all_positions:
                if board[r][c] == num:
                    filled_positions.append((r, c))
                    break
        
        for r in range(9):
             for c in range(9):
                 if (r, c) not in filled_positions:
                     board[r][c] = 0

        # for r in range(9):
        #     for c in range(9):
        #         if (r, c) not in elements_to_keep:
        #             board[r][c] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
