import tkinter as tk
from tkinter import messagebox
import csv
import subprocess
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

#Heatmapper and Tkinter Application to enter data. If you want a separate file path box just uncomment the relevant sections.
#
#


def heatmapper(path):
    # Load data from CSV file
    file_path = path  # Update with the path to your CSV file
    with open(file_path, 'r') as file:
        # Split the file into two parts based on an empty line
        content = file.read().strip().split('\n\n')
        
        # Read each part with labels
        color_data = pd.read_csv(io.StringIO(content[0]), index_col=0)
        annotation_data = pd.read_csv(io.StringIO(content[1]), index_col=0)

    # Verify data shape
    if color_data.shape != annotation_data.shape:
        raise ValueError("Color data and annotation data must have the same dimensions")

    # Set up the matplotlib figure
    plt.figure(figsize=(8, 6))

    # Create the heatmap using 'color_data' for color values and 'annotation_data' for cell annotations
    ax = sns.heatmap(color_data, annot=annotation_data, fmt="d", cmap="YlGnBu", cbar_kws={'label': 'Color Value'})

    # Customizing the plot for readability
    plt.title("")
    plt.xlabel("")
    plt.ylabel("")

    # Show the plot
    plt.show()

# Initialize the main Tkinter window
root = tk.Tk()
root.title("CSV Data Input with Two Values per Cell and Labels")

# Function to create a grid of Entry fields based on dimensions
def create_grid():
    # Clear any existing fields
    for widget in data_frame.winfo_children():
        widget.destroy()
    
    # Get the dimensions from user input
    try:
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integer dimensions.")
        return
    
    # Create entry fields for column labels (top row)
    col_labels.clear()
    for c in range(cols):
        label_entry = tk.Entry(data_frame, width=5)
        label_entry.grid(row=0, column=c + 1, padx=5, pady=5)
        col_labels.append(label_entry)
    
    # Create the main grid of Entry widgets with two fields per cell
    entry_grid.clear()  # Reset the entry grid
    row_labels.clear()  # Reset the row labels
    for r in range(rows):
        # Entry field for row label (left column)
        label_entry = tk.Entry(data_frame, width=5)
        label_entry.grid(row=r + 1, column=0, padx=5, pady=5)
        row_labels.append(label_entry)
        
        # Create each cell with two Entry widgets for two values per cell
        row_entries = []
        for c in range(cols):
            cell_frame = tk.Frame(data_frame)
            cell_frame.grid(row=r + 1, column=c + 1, padx=5, pady=5)
            entry1 = tk.Entry(cell_frame, width=5)
            entry1.pack(side=tk.LEFT, padx=1)
            entry2 = tk.Entry(cell_frame, width=5)
            entry2.pack(side=tk.LEFT, padx=1)
            row_entries.append((entry1, entry2))
        entry_grid.append(row_entries)

# Function to gather the data from Entry fields and save it as a CSV file
def submit_data():
    # Get the file path from the entry
    file_path = file_path_entry.get()
    
    # Check if the file path is empty
    if not file_path:
        messagebox.showerror("File Path Error", "Please specify a file path to save the CSV.")
        return

    # Ensure the file has a .csv extension
    if not file_path.endswith(".csv"):
        file_path += ".csv"

    # Get the number of rows and columns
    rows = len(entry_grid)
    cols = len(entry_grid[0]) if rows > 0 else 0

    # Initialize the upper and lower matrices
    upper_matrix = [[""] * (cols + 1) for _ in range(rows + 1)]
    lower_matrix = [[""] * (cols + 1) for _ in range(rows + 1)]

    # Fill the top row with column labels and left column with row labels
    upper_matrix[0][1:] = [col_label.get() for col_label in col_labels]
    lower_matrix[0][1:] = [col_label.get() for col_label in col_labels]
    for r in range(1, rows + 1):
        upper_matrix[r][0] = row_labels[r - 1].get()
        lower_matrix[r][0] = row_labels[r - 1].get()

    # Fill in data from the Entry grid
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            value1 = entry_grid[r - 1][c - 1][0].get()  # First value
            value2 = entry_grid[r - 1][c - 1][1].get()  # Second value
            upper_matrix[r][c] = value1
            lower_matrix[r][c] = value2

    # Save the matrices to a CSV file
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the upper matrix
            writer.writerows(upper_matrix)
            writer.writerow([])  # Blank row between matrices
            # Write the lower matrix
            writer.writerows(lower_matrix)
        
        messagebox.showinfo("Data Saved", f"Data has been saved to {file_path}")
        heatmapper(file_path)
        

        # Run Heatmapper.py after saving the file
        #heatmapper_script = os.path.join(os.path.dirname(__file__), "Heatmapper.py")
        #try:
        #    subprocess.run(["python", heatmapper_script], check=True)
         #   messagebox.showinfo("Success", "Heatmapper.py executed successfully.")
    except Exception as e:
       messagebox.showerror("File Save Error", f"An error occurred while saving the file: {e}")

# Frame for dimension inputs
dimension_frame = tk.Frame(root)
dimension_frame.pack(pady=10)

# Row and Column labels and entry fields
tk.Label(dimension_frame, text="Rows:").grid(row=0, column=0)
rows_entry = tk.Entry(dimension_frame, width=5)
rows_entry.grid(row=0, column=1)

tk.Label(dimension_frame, text="Columns:").grid(row=0, column=2)
cols_entry = tk.Entry(dimension_frame, width=5)
cols_entry.grid(row=0, column=3)

# Button to create the grid of Entry fields
create_button = tk.Button(dimension_frame, text="Create Grid", command=create_grid)
create_button.grid(row=0, column=4, padx=10)

# Frame for the Entry grid
data_frame = tk.Frame(root)
data_frame.pack(pady=10)

# Lists to store column label entries, row label entries, and grid cell entries
col_labels = []
row_labels = []
entry_grid = []

# Frame for file path input
file_path_frame = tk.Frame(root)
file_path_frame.pack(pady=10)
tk.Label(file_path_frame, text="Save CSV File Path:").pack(side=tk.LEFT)
file_path_entry = tk.Entry(file_path_frame, width=40)
file_path_entry.pack(side=tk.LEFT, padx=5)

# Button to submit data
submit_button = tk.Button(root, text="Submit Data", command=submit_data)
submit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()



