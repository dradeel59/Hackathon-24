import tkinter as tk
from tkinter import messagebox, Tk, PhotoImage, Canvas
from PIL import Image, ImageTk
import random

class SudokuApp:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Application")
        
        self.canvas = Canvas(master, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        background_image_path = "full_width-d.png"  # Replace with your image path
        self.background_image = PhotoImage(file=background_image_path)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        
        self.menu_screen()

    def menu_screen(self):
        self.clear_screen()

        self.canvas = Canvas(self.master, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        background_image_path = "full_width.png"  # Replace with your image path
        # self.background_image = Image.open(background_image_path)
        # self.background_image = self.background_image.resize((600, 600))
        # self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background_image = PhotoImage(file=background_image_path)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

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

        self.canvas = Canvas(master, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        background_image_path = "full_width-d.png"  # Replace with your image path
        self.background_image = PhotoImage(file=background_image_path)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        self.cells = [[tk.Entry(self.canvas, width=5, justify='center', font="Arial", borderwidth=2)
                       for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.canvas.create_window(50 * j + 25, 50 * i + 25, window=self.cells[i][j])

        self.solve_button = tk.Button(master, text="Solve", command=self.solve, background="salmon4", pady=5, padx=10, font="Arial")
        self.canvas.create_window(250, 500, window=self.solve_button)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear)
        self.canvas.create_window(300, 500, window=self.clear_button)

        self.generate_button = tk.Button(master, text="Generate", command=self.generate)
        self.canvas.create_window(350, 500, window=self.generate_button)

        self.check_button = tk.Button(master, text="Check", command=self.check)
        self.canvas.create_window(400, 500, window=self.check_button)

    def hint(self):
        pass

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
        for i in range(0, 9, 3):
            self.fill_box(board, i, i)
        self.solve_sudoku(board)
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
        for i in range(9):
            if (board[row][i] == num and i != col) or (board[i][col] == num and i != row):
                return False

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

        # Choose the number of instances to keep for each unique element
        num_instances_to_keep = 7  # Adjust this number to increase or decrease the filled cells
        
        for num in unique_elements:
            instances_found = 0
            for r, c in all_positions:
                if board[r][c] == num:
                    filled_positions.append((r, c))
                    instances_found += 1
                    if instances_found >= num_instances_to_keep:
                        break

        for r in range(9):
            for c in range(9):
                if (r, c) not in filled_positions:
                    board[r][c] = 0  
 
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(padx=20, pady=15, background="tan")
    app = SudokuApp(root)
    root.mainloop()
