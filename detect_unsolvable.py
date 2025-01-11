import csv
from z3 import *

def read_sudoku_from_csv(file_path):
    input_array = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Parse each row and convert to integers, use 0 for empty cells
            input_array.append([int(val) if val else 0 for val in row])
    return input_array

def detect_unsolvable(grid):
    solver = Solver()
    cells = [[Int(f"cell_{i}_{j}") for j in range(9)] for i in range(9)]

    # Add constraints for valid number range (1 to 9)
    for i in range(9):
        for j in range(9):
            solver.add(cells[i][j] >= 1, cells[i][j] <= 9)
    
    # Row uniqueness
    for i in range(9):
        solver.add(Distinct(cells[i]))

    # Column uniqueness
    for j in range(9):
        solver.add(Distinct([cells[i][j] for i in range(9)]))

    # Sub-grid uniqueness
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = [cells[x][y] for x in range(i, i+3) for y in range(j, j+3)]
            solver.add(Distinct(block))

    # Add pre-filled values from the grid
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                solver.add(cells[i][j] == grid[i][j])

    # Check satisfiability and return result
    if solver.check() == sat:
        return "Puzzle is solvable."
    else:
        return "Puzzle is unsolvable."

# Example usage: reading from a CSV file
file_path = 'sudoku.csv'  # Provide the correct path to your CSV file
grid = read_sudoku_from_csv('sudoku.csv')
result = detect_unsolvable(grid)
print(result)
