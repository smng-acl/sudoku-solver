from pulp import *
import streamlit as st

st.title("sudoku solver")

puzzleToSolve =  [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 3, 6, 0, 0, 0, 0, 0],
                  [0, 7, 0, 0, 9, 0, 2, 0, 0],
                  [0, 5, 0, 0, 0, 7, 0, 0, 0],
                  [0, 0, 0, 0, 4, 5, 7, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0, 3, 0],
                  [0, 0, 1, 0, 0, 0, 0, 6, 8],
                  [0, 0, 8, 5, 0, 0, 0, 1, 0],
                  [0, 9, 0, 0, 0, 0, 4, 0, 0]]

puzzleToSolve =  [[5,3, 0, 0, 7, 0, 0, 0, 0],
                  [6, 0, 0, 1, 9, 5, 0, 0, 0],
                  [0, 9, 8, 0, 0, 0, 0, 6, 0],
                  [8, 0, 0, 0, 6, 0, 0, 0, 3],
                  [4, 0, 0, 8, 0, 3, 0, 0, 1],
                  [7, 0, 0, 0, 2, 0, 0, 0, 6],
                  [0, 6, 0, 0, 0, 0, 2, 8, 0],
                  [0, 0, 0, 4, 1, 9, 0, 0, 5],
                  [0, 0, 0, 0, 8, 0, 0, 7, 9]]
                  
# print sudoku problem
st.write("Problem")
for r in range(len(puzzleToSolve)):
    if r == 0 or r == 3 or r == 6:
        st.write("+-------+-------+-------+")
    st_row = ""
    for c in range(len(puzzleToSolve[r])):
        if c == 0 or c == 3 or c ==6:
            st_row += "| "
        if puzzleToSolve[r][c] != 0:
            st_row += str(puzzleToSolve[r][c]) + " "
        else:
            st_row += "  "
        if c == 8:
            st_row += "|"
    st.write(st_row)
st.write("+-------+-------+-------+")

# A list of strings from 1 to 9 is created
Sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# The Vals, Rows and Cols sequences all follow this form
Vals = Sequence
Rows = Sequence
Cols = Sequence

# SquareBoxes list with the row and column index of each square
squareBoxes =[]
for i in range(3):
    for j in range(3):
        squareBoxes += [[(Rows[3*i+k],Cols[3*j+l]) for k in range(3) for l in range(3)]]
        
# Define Problem       
prob = LpProblem("Sudoku Problem",LpMinimize)

# Creating a Set of Variables
choices = LpVariable.dicts("Choice",(Vals,Rows,Cols),0,1,LpInteger)

# Added arbitrary objective function
prob += 0, "Arbitrary Objective Function"

# Setting Constraints
# 1. A constraint ensuring that only one value can be in each square is created
for r in Rows:
    for c in Cols:
        prob += lpSum([choices[v][r][c] for v in Vals]) == 1, ""

# 2, 3, 4. The row, column and square constraints are added for each value
for v in Vals:
    for r in Rows:
        prob += lpSum([choices[v][r][c] for c in Cols]) == 1,""
        
    for c in Cols:
        prob += lpSum([choices[v][r][c] for r in Rows]) == 1,""

    for b in squareBoxes:
        prob += lpSum([choices[v][r][c] for (r,c) in b]) == 1,""
                        
# 5. The starting numbers in sudoku problem are entered as constraints                
for r in range(len(puzzleToSolve)):
    for c in range(len(puzzleToSolve[r])):
        value = puzzleToSolve[r][c]
        if value != 0:
            prob += choices[value][r + 1][c + 1] == 1,""
            
# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
st.write("Status:", LpStatus[prob.status])

# print out sudoku solution
st.write("\nSudoku Solution")
for r in Rows:
    if r == 1 or r == 4 or r == 7:
        st.write("+-------+-------+-------+")
    st_row = ""
    for c in Cols:
        for v in Vals:
            if choices[v][r][c].varValue == 1:               
                if c == 1 or c == 4 or c == 7:
                    st_row += "| "
                st_row += str(v) + " "
                
                if c == 9:
                    st_row += "|"
    st.write(st_row)
st.write("+-------+-------+-------+")
