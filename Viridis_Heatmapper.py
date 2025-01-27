import tkinter as tk
from tkinter import messagebox
import csv
import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# Define the custom colormap (cut off the top 25% of 'viridis')
original_cmap = plt.cm.viridis
n_colors = original_cmap.N
cutoff = int(n_colors * 0.75)  # 75% of the colormap
colors = original_cmap(np.linspace(0, 0.75, cutoff))  # Extract first 75%
custom_cmap = ListedColormap(colors)

# Function to create the heatmap
def heatmapper(path):
    with open(path, 'r') as file:
        content = file.read().strip().split('\n\n')
        color_data = pd.read_csv(io.StringIO(content[0]), index_col=0)
        annotation_data = pd.read_csv(io.StringIO(content[1]), index_col=0)

    if color_data.shape != annotation_data.shape:
        raise ValueError("Color data and annotation data must have the same dimensions")

    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(color_data, annot=annotation_data, fmt="d", cmap=custom_cmap, cbar_kws={'label': 'Color Value'})
    plt.title("Heatmap")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.show()


# Initialize the main Tkinter window
root = tk.Tk()
root.title("CSV Data Input with Duplicate Checkbox")


# Function to enable/disable the second row of input fields
def toggle_lower_entries():
    for row in entry_grid:
        for entry1, entry2 in row:
            if duplicate_checkbox_var.get():
                entry2.config(state=tk.DISABLED)
            else:
                entry2.config(state=tk.NORMAL)


# Function to create a grid of Entry fields
def create_grid():
    for widget in data_frame.winfo_children():
        widget.destroy()
    try:
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integer dimensions.")
        return

    col_labels.clear()
    for c in range(cols):
        label_entry = tk.Entry(data_frame, width=5)
        label_entry.grid(row=0, column=c + 1, padx=5, pady=5)
        col_labels.append(label_entry)

    entry_grid.clear()
    row_labels.clear()
    for r in range(rows):
        label_entry = tk.Entry(data_frame, width=5)
        label_entry.grid(row=r + 1, column=0, padx=5, pady=5)
        row_labels.append(label_entry)

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

    toggle_lower_entries()


# Function to gather data and save as CSV
def submit_data():
    file_path = file_path_entry.get()
    if not file_path:
        messagebox.showerror("File Path Error", "Please specify a file path to save the CSV.")
        return
    if not file_path.endswith(".csv"):
        file_path += ".csv"

    rows = len(entry_grid)
    cols = len(entry_grid[0]) if rows > 0 else 0

    upper_matrix = [[""] * (cols + 1) for _ in range(rows + 1)]
    lower_matrix = [[""] * (cols + 1) for _ in range(rows + 1)]

    upper_matrix[0][1:] = [col_label.get() for col_label in col_labels]
    lower_matrix[0][1:] = [col_label.get() for col_label in col_labels]
    for r in range(1, rows + 1):
        upper_matrix[r][0] = row_labels[r - 1].get()
        lower_matrix[r][0] = row_labels[r - 1].get()

    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            value1 = entry_grid[r - 1][c - 1][0].get()
            value2 = (
                value1 if duplicate_checkbox_var.get() else entry_grid[r - 1][c - 1][1].get()
            )
            upper_matrix[r][c] = value1 if value1 else "0"
            lower_matrix[r][c] = value2 if value2 else "0"

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(upper_matrix)
            writer.writerow([])
            writer.writerows(lower_matrix)
        
        messagebox.showinfo("Data Saved", f"Data has been saved to {file_path}")
        heatmapper(file_path)
    except Exception as e:
        messagebox.showerror("File Save Error", f"An error occurred while saving the file: {e}")


# Frame for dimension inputs
dimension_frame = tk.Frame(root)
dimension_frame.pack(pady=10)

tk.Label(dimension_frame, text="Rows:").grid(row=0, column=0)
rows_entry = tk.Entry(dimension_frame, width=5)
rows_entry.grid(row=0, column=1)

tk.Label(dimension_frame, text="Columns:").grid(row=0, column=2)
cols_entry = tk.Entry(dimension_frame, width=5)
cols_entry.grid(row=0, column=3)

create_button = tk.Button(dimension_frame, text="Create Grid", command=create_grid)
create_button.grid(row=0, column=4, padx=10)

# Frame for the Entry grid
data_frame = tk.Frame(root)
data_frame.pack(pady=10)

col_labels = []
row_labels = []
entry_grid = []

# Frame for file path input
file_path_frame = tk.Frame(root)
file_path_frame.pack(pady=10)
tk.Label(file_path_frame, text="Save CSV File Path:").pack(side=tk.LEFT)
file_path_entry = tk.Entry(file_path_frame, width=40)
file_path_entry.pack(side=tk.LEFT, padx=5)

# Checkbox for duplicate functionality
duplicate_checkbox_var = tk.BooleanVar(value=True)
duplicate_checkbox = tk.Checkbutton(
    root,
    text="Identical Values for text and colour",
    variable=duplicate_checkbox_var,
    command=toggle_lower_entries
)
duplicate_checkbox.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit Data", command=submit_data)
submit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
