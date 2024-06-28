# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:05:28 2024

Sudoku Puzzle creator

@author: Jack Rawlinson
"""

import numpy as np


def row_box_generator(grid_layout):
    for i in range(3):  # Iterate over all rows
        # Generate a random order for the numbers 1-9 for current row
        order = np.random.choice(range(1, 10), 9, replace=False)
        grid_layout[:, i] = order
    return grid_layout


def box_checker(grid_layout):
    print("In box checker")
    invalid_layout = True
    # If a box has all numbers between 1 and 9 within all its cells then its sum will equal 45
    box_1_total = np.sum(grid_layout[0:3, 0:3])
    box_2_total = np.sum(grid_layout[3:7, 0:3])
    box_3_total = np.sum(grid_layout[7:10, 0:3])
    if box_1_total == 45 and box_2_total == 45 and box_3_total == 45:
        invalid_layout = False
    return invalid_layout


grid = np.zeros((9, 9))

order = np.random.choice(range(1, 10), 9, replace=False)

for i in range(3):  # Iterate over all rows
    i = i*3
    grid[:, i:i+3] = row_box_generator(grid[:, i:i+3])
    remake_boxes = box_checker(grid[:, i:i+3])
    while remake_boxes:
        print("In while loop")
        grid[:, i:i+3] = row_box_generator(grid[:, i:i+3])
        remake_boxes = box_checker(grid[:, i:i+3])

print(grid)
