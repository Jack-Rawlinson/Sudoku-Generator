# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:05:28 2024

Sudoku Puzzle creator

@author: Jack Rawlinson
"""

import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class sudoku_grid_GUI:
    """
    Creates the window for users to access the sudoku grid

    Parameters
    ----------
    grid_layout : 3-D numpy array
      grid_layout[:,:,0] - Contains the real value in each cell 
      grid_layout[:,:,1] - Once a valid grid is created this will store a solvable grid
        for user to complete 
      grid_layout[:,:,x+1] - Conains map of 1's & 0's informing function if it is possible 
        for a cell to contain the number x, in following with sudoku rules.

    Returns
    -------
    None.

    """

    def __init__(self, grid_layout):
        self.grid = grid_layout

        # back & fore ground colours
        bg_colour = "white"
        fg_colour = "Black"

        # Initilaise window
        self.window = tk.Tk()
        # Set title and colours
        self.window.title("Sudoku")
        self.window.configure(background=bg_colour)

        # Fill window with sudoku grid
        self.set_visual_grid()
        #ttk.Separator(window, orient='vertical').place(x=0.5, y=0.5, relwidth=0.1, relheight=0.1)

        self.window.mainloop()

    def set_visual_grid(self):
        """
        Fills window with a Sudoku grid from grid_layout

        Parameters
        ----------
        grid_layout : 3-D numpy array
          grid_layout[:,:,0] - Contains the real value in each cell 
          grid_layout[:,:,1] - Once a valid grid is created this will store a solvable grid
            for user to complete 
          grid_layout[:,:,x+1] - Conains map of 1's & 0's informing function if it is possible 
            for a cell to contain the number x, in following with sudoku rules.
        build_window : tkinter parent window 
          parent window which will showcase the widgets created in this function

        Returns
        -------
        None.

        """
        # Frame used in attempt to create sudoku boxes
        label_frame = tk.Frame(self.window)

        # Create and fill 9x9 grid
        for row_itr in range(9):
            #build_window.rowconfigure(i, weight=100)
            for column_itr in range(9):
                #    if i % 3 == 0 and j % 3 == 0:
                #        label_frame = tk.Frame(build_window)
                # Show pre-filled numbers and create text box for empty cells which need to be filled
                if self.grid[1, row_itr, column_itr] != 0:
                    tk.Label(label_frame, text=str(
                        int(self.grid[1, row_itr, column_itr])), bg="white", fg="black", font="none 12 bold").grid(row=row_itr, column=column_itr)
                else:
                    extinput = tk.Entry(label_frame, bg="White", ).grid(
                        row=row_itr, column=column_itr)
                    self.grid[1, row_itr, column_itr] = extinput
                #build_window.columnconfigure(j, weight=1)
        #ttk.Separator(label_frame, orient='vertical').place(x=0.5, y=0.5, relwidth=0.1, relheight=0.1)
        check = tk.Button(label_frame, text="Check answer",
                          command=self.check_answer).grid(row=10, column=3)
        #check.grid(row=10, column=3, columnspan=3)
        # Allow frame to expand with window tab
        label_frame.pack()  # fill=tk.BOTH)  # , expand=1, padx=20, pady=20)

    def check_answer(self):
        try:
            for row_itr in range(9):
                for column_itr in range(9):
                    int(self.grid[1, :, :])
            if self.grid[1, :, :] == self.grid[0, :, :]:
                messagebox.showinfo("Success", "You completed it!!!!")
            else:
                messagebox.showinfo("Fail", "There is a mistake somewhere :(")
        except:
            messagebox.showerror("Error", "Please only enter intergers between 1-9 !")


def complete_grid_generator(grid_layout):
    """
    Cycles through every cell in the sudoku grid and assigns a valid number

    Parameters
    ----------
    grid_layout : 3-D numpy array
      grid_layout[:,:,0] - Contains the real value in each cell 
      grid_layout[:,:,1] - Once a valid grid is created this will store a solvable grid
        for user to complete 
      grid_layout[:,:,x+1] - Conains map of 1's & 0's informing function if it is possible 
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
        grid_layout[0, row, collumn] = int(cell_value)

        # Reset the probability maps in accordance to this new cell number
        set_probabilities(cell_value+1, grid_layout, row, collumn)

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
      grid_layout[:,:,1] - Once a valid grid is created this will store a solvable grid
        for user to complete 
      grid_layout[:,:,x+1] - Conains map of 1's & 0's informing function if it is possible 
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
        probs[i] = grid_layout[i+2, row, collumn]
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
      grid_layout[:,:,1] - Once a valid grid is created this will store a solvable grid
        for user to complete 
      grid_layout[:,:,x+1] - Conains map of 1's & 0's informing function if it is possible 
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


def solvable_grid(grid_layout):
    """
    Creates solvable sudoku grid using the complete grid 

    Parameters
    ----------
    grid_layout : 3-D numpy array
      grid_layout[:,:,0] - Contains the real value in each cell 
      grid_layout[:,:,1] - Once a valid grid is created this will store a solvable grid
        for user to complete 
      grid_layout[:,:,x+1] - Conains map of 1's & 0's informing function if it is possible 
        for a cell to contain the number x, in following with sudoku rules.

    Returns
    -------
    grid_layout : 3-D numpy array
      grid_layout[:,:,0] - Contains the real value in each cell 
      grid_layout[:,:,1] - Once a valid grid is created this will store a solvable grid
        for user to complete 
      grid_layout[:,:,x+1] - Conains map of 1's & 0's informing function if it is possible 
        for a cell to contain the number x, in following with sudoku rules.
    """
    # Iterator to track number of filled cells
    filled_cells = 0
    while filled_cells < 17:
        # Choose random cell to show value of
        row_value = np.random.choice(range(9), 1)
        column_value = np.random.choice(range(9), 1)
        # Check that this cell does not already showcase a correct value
        if grid_layout[1, row_value, column_value] == 0:
            grid_layout[1, row_value, column_value] = grid_layout[0, row_value, column_value]
            # Update iterator
            filled_cells += 1

    return grid_layout


# Create empty sudoku grid
grid = np.zeros((11, 9, 9))

# Fill each probability map
for i in range(9):
    grid[i+2:, :] = 1

# Generate sudoku grid
grid = complete_grid_generator(grid)
solvable_grid = solvable_grid(grid)

print("SUCCESSFUL GRID : ")
print(grid[0, :, :])

app = sudoku_grid_GUI(solvable_grid)
