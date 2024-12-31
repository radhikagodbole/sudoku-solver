from z3 import Bool, Solver, Or, And, sat, is_true

# Create boolean variables
# p = Bool('p')
# q = Bool('q')
BIJK = [[[Bool(f'b_{i}{j}{k}') for k in range(9)] for j in range(9)] for i in range(9)]

# input_array = [[-1 for i in range(9)] for j in range(9)]
input_array = []
for i in range(9):
    row = []
    for j in range(9):
        value = int(input(f"Enter value for ({i+1},{j+1}) : "))
        row.append(value)
    input_array.append(row)

# Sanity check
# print(BIJK[0][0][0])

# Create a solver instance
solver = Solver()

all_constraints = []

# Add existing numbers
for i in range(9):
    for j in range(9):
        if input_array[i][j] != -1:    
            all_constraints.append(BIJK[i][j][input_array[i][j]-1])

# Add row constraints
for i in range(9):
    for k in range(9):
        atleast_once = Or([BIJK[i][j][k] for j in range(9)])
        all_constraints.append(atleast_once)

# Add column constraints
for j in range(9):
    for k in range(9):
        atleast_once = Or([BIJK[i][j][k] for i in range(9)])
        all_constraints.append(atleast_once)

# Add square constraints
for sq in range(9):
    # sq, col_offset, row_offset
        # 0, 0, 0
        # 1, 1, 0
        # 2, 2, 0
    col_offset = sq % 3
    row_offset = int(sq / 3)
    # print(col_offset, row_offset)
    for k in range(9):
        indices = [
            (row_offset*3+_i, col_offset*3+_j)
            for _i in range(3) for _j in range(3)
        ]
        cell_list = [BIJK[_i][_j][k] for (_i, _j) in indices]
        atleast_once = Or(cell_list)
        all_constraints.append(atleast_once)

# Add cell constraints
for i in range(9):
    for j in range(9):
        all_constraints.append(Or([BIJK[i][j][k] for k in range(9)]))
        for k1 in range(9):
            for k2 in range(k1):
                cell_constraint = ~And(BIJK[i][j][k1], BIJK[i][j][k2])
                all_constraints.append(cell_constraint)


# Add a constraint (e.g., p AND q)
# constraint = p & ~p
solver.add(And(all_constraints))

if solver.check() == sat:
    m = solver.model()
    values = [[[m.evaluate(BIJK[i][j][k]) for k in range(9)] 
               for j in range(9)] for i in range(9)]
    # print(values)
    correct_values = [
        [values[i][j].index(True)+1 for j in range(9)]
            for i in range(9)
    ]
    # print(correct_values)

    for row in correct_values:
        print(" ".join(map(str, row)))