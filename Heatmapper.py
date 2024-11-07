import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Load data from CSV file
file_path = 'a.csv'  # Update with the path to your CSV file
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
