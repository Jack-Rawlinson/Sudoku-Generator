# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:05:28 2024

Sudoku Puzzle creator

@author: Jack Rawlinson
"""

import numpy as np


def cell_generator(grid_layout):
    """
    Cycles through every cell in the sudoku grid and assigns a valid number

    Parameters
    ----------
    grid_layout : 3-D numpy array
      grid_layout[:,:,0] - Contains the real value in each cell 
      grid_layout[:,:,x] - Conains map of 1's & 0's informing function if it is possible 
        for a cell to contain the number x, in following with sudoku rules.

    Returns
    -------
    grid_layout : 3-D numpy array
      Array containing the completed sudoku grid.

    """
    # Set initail starting position
    row = 0
    collumn = 0
    grid_incomplete = True
    # Create a depp copy for use if code gets stuck for options at the end of a row
    grid_memory = np.copy(grid_layout)
    # Itterate over each cell

    while grid_incomplete:

        # 1-d array of probabilities for each number in a cell
        probailities = get_cell_probabilites(grid_layout, row, collumn)

        # Save configureation at the start of a new row
        if collumn == 0:
            grid_memory = np.copy(grid_layout)

        # Check for NaNs, if found then reset current row
        # This is repeated until a valid row is created
        if np.isnan(probailities[0]):
            collumn = 0
            # Reset using memory
            # Hard copy used to avoid memory corruption
            grid_layout = np.copy(grid_memory)
            # Update probability array
            probailities = get_cell_probabilites(grid_layout, row, collumn)

        # Assign the cell a number between 1 and 9
        cell_value = np.random.choice(range(1, 10), 1, p=probailities)
        grid_layout[0, row, collumn] = cell_value

        # Reset the probability maps in accordance to this new cell number
        set_probabilities(cell_value, grid_layout, row, collumn)

        # Update current collumn position
        collumn += 1

        # End code if in final cell
        if collumn == 9 and row == 8:
            grid_incomplete = False

        # Move to new row at end of current one
        if collumn == 9:
            row += 1
            collumn = 0

    return grid_layout


def get_cell_probabilites(grid_layout, row, collumn):
    """
    Cylces through the grid_layout probability maps to create 
      1-d array of probabilities for the current cell choice.

    Parameters
    ----------
    grid_layout : 3-D numpy array
      grid_layout[:,:,0] - Contains the real value in each cell 
      grid_layout[:,:,x] - Conains map of 1's & 0's informing function if it is possible 
        for a cell to contain the number x, in following with sudoku rules.
    row : Int
      Current row index.
    collumn : Int
      Current collumn index.

    Returns
    -------
    probs : 1-D numpy array
      1-D array of probabilites for the current cell.

    """

    probs = np.zeros(9)

    for i in range(9):
        probs[i] = grid_layout[i+1, row, collumn]
    total = sum(probs)
    # Set equal probability for each possible number
    probs = probs * (1/total)
    return probs


def set_probabilities(number, grid_layout, row, collumn):
    """
    Updates probability map in accordance with the latest cell value 

    Parameters
    ----------
    number : Int
      Value that has just been placed into cell
    grid_layout : 3-D numpy array
      grid_layout[:,:,0] - Contains the real value in each cell 
      grid_layout[:,:,x] - Conains map of 1's & 0's informing function if it is possible 
        for a cell to contain the number x, in following with sudoku rules.
    row : Int
      Current row index.
    collumn : int
      Current collumn index

    Returns
    -------
    None.

    """
    # Set current row and collumn probabilities to 0 in the map of the cell value
    grid_layout[number, :, collumn] = 0
    grid_layout[number, row, :] = 0
    # Locate the 3x3 box where cell is situated
    box_row = int(np.floor(row/3)) * 3
    box_collumn = int(np.floor(collumn/3))*3
    # Set probabilites in box to 0
    for current_row in range(3):
        cell_row = box_row + current_row
        for current_collumn in range(3):
            cell_collumn = box_collumn + current_collumn
            grid_layout[number, cell_row, cell_collumn] = 0


# Create empty sudoku grid
grid = np.zeros((10, 9, 9))

# Fill each probability map
for i in range(9):
    grid[i+1:, :] = 1

# Generate sudoku grid
grid = cell_generator(grid)


print("SUCCESSFUL GRID : ")
print(grid[0, :, :])
