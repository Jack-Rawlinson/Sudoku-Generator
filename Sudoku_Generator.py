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

class Sudoku_Grid_GUI:
    """
    Creates the window for users to access the sudoku grid
    """

    def __init__(self):

        # back & fore ground colours
        bg_colour = "Black"

        # Initilaise window
        self.window = tk.Tk()
        # Set title and colours
        self.window.title("Sudoku")
        self.window.configure(background=bg_colour)

        # Fill window with sudoku grid
        #print("Entering gui creation")
        self.gui_config()
        # Highlight cells with number pressed 
        self.window.bind("<Key>", self.highlight_cells)
        #print("Created gui config")
        # Create timer widegt after 1 microsecond
        self.window.after(1, self.create_timer)
        # Start window
        self.window.mainloop()

    def gui_config(self):
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
        print("Setting GUI")
        # Frame used in attempt to create sudoku boxes
        #label_frame = tk.Frame(self.window, relief="solid", bd=2, bg="white")
        self.entry_grid = [[0 for i in range(9)] for j in range(9)]

        # Validation command for entry boxes, resticts inputs to only ints
        self.vcmd = self.window.register(self.callback)

        # Creating combo box to set the difficulty of the puzzle
        difficulties = ["Easy", "Medium", "Hard"]
        self.difficulty_widget = ttk.Combobox(self.window, values=difficulties, state="readonly")
        self.difficulty_widget.grid(row=10, column=6, columnspan=2)
        # Setting initial diffculty to Hard
        self.difficulty_widget.current(2)
        self.difficulty = "Hard"
        # Link box action to set_difficulty function
        self.difficulty_widget.bind("<<ComboboxSelected>>", self.set_difficulty)

        # Generate sudoku grid
        self.complete_grid_generator()

        # self.set_visual_grid()

        # Check answer button
        tk.Button(self.window, text="Check answer",
                  command=self.check_answer).grid(row=10, column=0)
        # Button to generate and show a new puzzle without closing application
        tk.Button(self.window, text="Generate new grid",
                  command=self.generate_new_grid).grid(row=10, column=1, columnspan=2)
        # Changes background colour of all incorrect boxes to red
        tk.Button(self.window, text="Show mistakes",
                  command=self.show_errors).grid(row=10, column=3)

        # Allow frame to expand with window tab
        #label_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)

    def set_visual_grid(self):
        """
        Set up the Sudoku grid in the GUI

        Returns
        -------
        None.

        """
        self.colours = ["white", "light blue"]
        # Create and fill 9x9 grid
        for row_start in range(3):
            row_start *= 3
            #build_window.rowconfigure(i, weight=100)
            for column_start in range(3):
                column_start *= 3
                # Use entry boxes as cells
                colour_index = (row_start + column_start) % 2
                self.create_3x3_box(row_start, column_start, self.colours[colour_index])
        print("Leaving set_visual_grid")

    def create_3x3_box(self, row_start, column_start, colour):
        """
        Function to reduce code duplication when creating boxes

        Parameters
        ----------
        row_start : Int
          Grid position of uppper left corner of current box
        column_start : Int
          Grid position of upper left corner of current box
        colour : String
          Background colour of cells within current box 

        Returns
        -------
        None.

        """
        # Cerate new frame for 3x3 box
        frame = tk.Frame(self.window, relief="groove", bd=2,
                         bg=colour).grid(row=row_start, column=column_start)
        print("Creating frames")
        for row_itr in range(3):
            for column_itr in range(3):
                # Calculate index of current cell
                row_index = row_start + row_itr
                column_index = column_start + column_itr

                entry = tk.Entry(frame, width=5, justify='center', font=(
                    'Arial', 18), bg=colour,  validate="all", validatecommand=(self.vcmd, "%P"))  
                # Store entries
                self.entry_grid[row_index][column_index] = entry
                entry.grid(row=row_index, column=column_index, padx=5, pady=5)
                entry.bind("<Up>", self.navigation)
                entry.bind("<Down>", self.navigation)
                entry.bind("<Left>", self.navigation)
                entry.bind("<Right>", self.navigation)

                # Pre-fill the entry with the initial value from the board if not zero
                if self.grid[1, row_index, column_index] != 0:
                    entry.insert(0, int(self.grid[1, row_index, column_index]))
                    # Disable editing of initial values
                    entry.config(state='disabled', disabledbackground=colour)
                    entry.bind("<Button-1>", self.highlight_cells_click)
        print("Created frames")

    def navigation(self, event):
        """
        Function to navigate betwen cells using arrow keys, makes for better UX

        Parameters
        ----------
        event : Tkinter event
          Tkinter key press event

        Returns
        -------
        None.
        """
        # Get row and column of current cell
        pos = event.widget.grid_info()
        row = pos["row"]
        col = pos["column"]
        # Update current cell in accordance to arrow key pressed
        if(event.keysym == "Up"):
            self.entry_grid[row-1][col].focus()
        if(event.keysym == "Down"):
            if(row==8):
              row = -1
            self.entry_grid[row+1][col].focus()
        if(event.keysym == "Left"):
            self.entry_grid[row][col-1].focus()
        if(event.keysym == "Right"):
            if(col==8):
              col = -1
            self.entry_grid[row][col+1].focus()

    def highlight_cells(self, event):
        """
        Function to override key press event and will highlight all cells with the same number as the key presssed.

        Parameters
        ----------
        event : Tkinter event
          Tkinter key press event

        Returns
        -------
        None.

        """
        print(f'Button press event: {event}')
        # Don't highlight cells if directional keys are used
        if(not(event.keysym in ("Up", "Down", "Left", "Right"))):
          for row_itr in range(9):
              for column_itr in range(9):
                  cell_colour = self.entry_grid[row_itr][column_itr]["background"]
                  # Reset all gold
                  if(cell_colour == "gold"):
                      # Define position of box containing cell
                      box_row = np.floor(row_itr / 3)
                      box_column = np.floor(column_itr / 3)
                      colour_index = int((box_row + box_column) % 2)

                      # Reset cell to its original colour
                      self.entry_grid[row_itr][column_itr].config(
                          bg=self.colours[colour_index], disabledbackground=self.colours[colour_index])

                  # Set any cells with the same number as key pressed to gold as well as current cell
                  if (self.entry_grid[row_itr][column_itr].get() == event.char):
                      self.entry_grid[row_itr][column_itr].config(
                          bg="gold", disabledbackground="gold")

    def highlight_cells_click(self, event):
        """
        Function to override key press event and will highlight all cells with the same number as the key presssed.

        Parameters
        ----------
        event : Tkinter event
          Tkinter key press event

        Returns
        -------
        None.

        """
        print(f'Button press event: {event.widget.get()}')
        for row_itr in range(9):
            for column_itr in range(9):
                cell_colour = self.entry_grid[row_itr][column_itr]["background"]
                # Reset all gold
                if(cell_colour == "gold"):
                    # Define position of box containing cell
                    box_row = np.floor(row_itr / 3)
                    box_column = np.floor(column_itr / 3)
                    colour_index = int((box_row + box_column) % 2)

                    # Reset cell to its original colour
                    self.entry_grid[row_itr][column_itr].config(
                        bg=self.colours[colour_index], disabledbackground=self.colours[colour_index])

                # Set any cells with the same number as key pressed to gold as well as current cell
                if (self.entry_grid[row_itr][column_itr].get() == event.widget.get()):
                    self.entry_grid[row_itr][column_itr].config(
                        bg="gold", disabledbackground="gold")

    def callback(self, P):
        """
        Validation function in order to restrict inputs to only numbers

        Parameters
        ----------
        P : String
          Value entered into entry box

        Returns
        -------
        bool
          Results of validation

        """
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def generate_new_grid(self):
        """
        Generates and shows a new grid

        Returns
        -------
        None.

        """
        print("IN GENERATE NEW GRID")
        self.complete_grid_generator()
        self.set_visual_grid()
        print("lEAVING GENERATE NEW GRID")

    def set_difficulty(self, selection):
        """
        Will change the difficulty of the displayed puzzle 

        Parameters
        ----------
        selection : TYPE
          DESCRIPTION.

        Returns
        -------
        None.

        """
        print("In SET DIFFICULTY")
        # Update difficulty when combobx is used

        self.difficulty = self.difficulty_widget.get()

        # Assume hard difficulty to begin to cut down of if statements
        self.grid[1, :, :] = np.copy(self.hard_grid)

        if self.difficulty_widget.get() == "Easy":
            print("Setting to easy")
            #self.difficulty = "Easy"
            self.grid[1, :, :] = np.copy(self.easy_grid)

        if self.difficulty_widget.get() == "Medium":
            print("setting to medium")
            #self.difficulty = "Medium"
            self.grid[1, :, :] = np.copy(self.medium_grid)

        # Update grid
        self.set_visual_grid()
        print(f'EASY GRID : \n{self.easy_grid}')
        print(f'MEDIUM GRID : \n{self.medium_grid}')
        print(f'HARD GRID : \n{self.hard_grid}')
        print("LEAVING SET DIFFICULTY")
        print(f'Diffculty = {self.difficulty}')
        # print(f'Entry grid = {self.entry_grid}')
        # print(f'Entry grid = {self.entry_grid[0]}')
        # print(f'Entry grid = {self.entry_grid[0][0].get()}')

    def create_timer(self):
        """
        Creates a timer widget and will start the clock after 1 second 

        Returns
        -------
        None.

        """
        # Create and psotion the widget
        self.timer_variable = tk.Label(self.window, text="00:00")
        self.timer_variable.grid(
            row=10, column=4, columnspan=2)

        self.seconds = 0
        self.minutes = 0
        # Itterator statement for timer
        self.incomplete = True

        self.window.after(1000, self.update_timer)

    def update_timer(self):
        """
        Updates timer every second 

        Returns
        -------
        None.

        """

        self.seconds += 1
        # Update minute count after 60 seconds
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0

        self.timer_variable.config(text=f'{self.minutes:02d}:{self.seconds:02d}')
        if self.incomplete:
            self.window.after(1000, self.update_timer)

    def check_answer(self):
        """
        Command function to validate the entered solution and show an info box

        Returns
        -------
        None.

        """
        try:
            correct_answers = 0
            for row_itr in range(9):
                for column_itr in range(9):
                    # Note when value in entry display matches the correct grid

                    if int(self.grid[0, row_itr, column_itr]) == int(self.entry_grid[row_itr][column_itr].get()):
                        correct_answers += 1

            if correct_answers == 81:
                messagebox.showinfo(
                    "Success", f'You completed it!!!! \nTime to complete : {self.minutes} minutes {self.seconds} seconds')
                # Update that sudoku is solved to stop timer
                self.incomplete = False
            else:
                messagebox.showinfo(
                    "Fail", f'There is a mistake somewhere :(, Correct answers = {correct_answers})')
        # To catch when nothing is entered
        except Exception:
            messagebox.showerror("Error", "Please fill all cells with intergers 1-9")

    def show_errors(self):
        """
        Change background colour of all empty/incorrect cells to red 

        Returns
        -------
        None.

        """
        for row_itr in range(9):
            for column_itr in range(9):
                # Try except catch empty cells
                try:
                    # If cell value doesn't match completed grid then change it to red
                    if int(self.grid[0, row_itr, column_itr]) != int(self.entry_grid[row_itr][column_itr].get()):
                        #print("seen a mistake ")
                        self.entry_grid[row_itr][column_itr].config(bg="red")
                    #print("Leaving show errors")
                except:
                    #print("Seen as a NaN, In show errors")
                    self.entry_grid[row_itr][column_itr].config(bg="red")

    def complete_grid_generator(self):
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
        # Create empty sudoku grid
        self.grid = np.zeros((11, 9, 9))

        # Fill probility grids for each possible number
        for number in range(2, 11):
            self.grid[number, :, :] = 1

        # Set initial starting position
        row = 0
        collumn = 0
        resets = 0
        grid_incomplete = True
        start_of_row = False
        # Create a deep copy for use if code gets stuck for options at the end of a row
        grid_memory = np.copy(self.grid)
        # Iterate over each cell

        while grid_incomplete:

            # If grid not fixed after 3 atempts then completely reset the grid
            if resets == 3:
                # Create empty sudoku grid
                self.grid = np.zeros((11, 9, 9))

                # Fill probility grids for each possible number
                for number in range(2, 11):
                    self.grid[number, :, :] = 1

                # Set initial starting position
                row = 0
                collumn = 0
                resets = 0
                grid_incomplete = True
                start_of_row = False

            # 1-d array of probabilities for each number in a cell
            probailities = self.get_cell_probabilites(row, collumn)
            print("Getting initial probs for cell")

            # Save configureation at the start of a new row
            if start_of_row:
                start_of_row = False
                resets = 0
                grid_memory = np.copy(self.grid)

            # Check for NaNs, if found then reset current row
            # This is repeated until a valid row is created

            if np.isnan(probailities[0]):
                collumn = 0
                print(f'Issue grid \n{self.grid[0,:,:]}')
                # Reset using memory
                # Hard copy used to avoid memory corruption
                self.grid = np.copy(grid_memory)
                # Update probability array
                probailities = self.get_cell_probabilites(row, collumn)
                resets += 1
                print("Reset grid")
                print(f'Issue row = {row}')

            # Assign the cell a number between 1 and 9
            cell_value = np.random.choice(range(1, 10), 1, p=probailities)
            self.grid[0, row, collumn] = int(cell_value)

            # Reset the probability maps in accordance to this new cell number
            self.set_probabilities(cell_value+1, row, collumn)

            # Update current collumn position
            collumn += 1

            # End code if in final cell
            if collumn == 9 and row == 8:
                #print("------------- IN FINAL CELL ---------------")
                grid_incomplete = False

            # Move to new row at end of current one
            if collumn == 9:
                row += 1
                collumn = 0
                start_of_row = True

        print("SUCCESSFUL GRID : ")
        print(self.grid[0, :, :])
        # Set interator now for use in solvable grid function
        self.filled_cells = 0
        self.solvable_grid()

    def get_cell_probabilites(self, row, collumn):
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
            probs[i] = self.grid[i+2, row, collumn]
        total = sum(probs)
        # Set equal probability for each possible number
        probs = probs * (1/total)
        print("leaving get probs")
        return probs

    def set_probabilities(self, number, row, collumn):
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
        self.grid[number, :, collumn] = 0
        self.grid[number, row, :] = 0
        # Locate the 3x3 box where cell is situated
        box_row = int(np.floor(row/3)) * 3
        box_collumn = int(np.floor(collumn/3))*3
        # Set probabilites in box to 0
        for current_row in range(3):
            cell_row = box_row + current_row
            for current_collumn in range(3):
                cell_collumn = box_collumn + current_collumn
                self.grid[number, cell_row, cell_collumn] = 0

    def solvable_grid(self):
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
        print("FILLING SOLVABLE GRID")
        while self.filled_cells < 61:
            # Choose random cell to show value of
            row_value = np.random.choice(range(9), 1)
            column_value = np.random.choice(range(9), 1)
            # Check that this cell does not already showcase a correct value
            if self.grid[1, row_value, column_value] == 0:
                self.grid[1, row_value, column_value] = self.grid[0, row_value, column_value]
                # Update iterator
                self.filled_cells += 1
            # Save configureations of the grid for different difficulties
            if self.filled_cells == 17:
                self.hard_grid = np.copy(self.grid[1, :, :])
            if self.filled_cells == 39:
                self.medium_grid = np.copy(self.grid[1, :, :])

        print("SET SOLVABLE GRID")
        self.easy_grid = np.copy(self.grid[1, :, :])
        # Call set_difficulty so that difficulty level is kept constant when generating new grids
        self.set_difficulty(self.difficulty)


if __name__ == "__main__":

    app = Sudoku_Grid_GUI()
