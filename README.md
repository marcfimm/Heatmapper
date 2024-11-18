# Heatmapper

This project provides an easy-to-use interface for creating heatmaps in Python, it could be used for visualizing paired data such a yield and recovered starting material.

- **UI.py**: A user interface for creating `.csv` files in the required format, allowing data input with two values per cell, under the hood this uses Tkinter.
- **Heatmapper.py**: The script that generates the heatmap visualization from the `.csv` file, using the `seaborn` library.

![alt text](https://github.com/marcfimm/Heatmapper/blob/main/Seperate_A.png?raw=true)

## Installation

### Requirements

- **Python 3.7+**
- **Libraries**:
  - `pandas`
  - `seaborn`
  - `matplotlib`
  - `tkinter`

I would recommend using anaconda:

```bash
conda create --name Heatmapper python=3.8
conda activate Heatmapper
```

To install the necessary packages, use (Inside the enviroment if using anaconda):

```bash
pip install pandas seaborn matplotlib
```

### Files

1. `UI.py`: The main interface for creating CSV files.
2. `Heatmapper.py`: The heatmap generator.

## Usage

1. **Run `UI.py`**:
    - Open `UI.py` in your favourite terminal:
      ```bash
      python UI.py
      ```
    - Enter the matrix dimensions (number of rows and columns) and press **Create Grid**.
    - Fill in the labels (top row for column labels and leftmost column for row labels).
    - Enter two values for each cell:
      - **Left** value: Defines the color intensity for that cell in the heatmap.
      - **Right** value: Displayed as the numeric value in the heatmap cell.
    - Specify a save path for the `.csv` file.
    - Press **Submit Data** to save the CSV and automatically generate a heatmap.

2. **Run `Heatmapper.py` (if not automatically run)**:
    - If you want to manually create a heatmap (for example from a already or manually created csv), run:
      ```bash
      python Heatmapper.py
      ```

3. **View the Heatmap**:
   - After `Heatmapper.py` executes, the generated heatmap should display, showcasing both color intensities and numeric labels.

## CSV Format

To use `Heatmapper.py` directly with a pre-existing `.csv` file, structure it as follows:

- **Top Matrix** (color data):
    - Each cell contains the color parameter values (e.g., yield).
  
- **Bottom Matrix** (numeric data):
    - Each cell contains the numeric display values (e.g., recovered starting material).

**Example Format**:

```csv
,LabelA,LabelB,LabelC
Label1,0.1,0.5,0.3
Label2,0.9,0.3,0.6
Label3,0.5,0.8,0.1

,LabelA,LabelB,LabelC
Label1,5,10,15
Label2,30,35,40
Label3,55,60,65
```

Each section should start with a blank cell in the top-left corner, followed by the column labels on the first row and row labels in the first column.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contact

For questions or contributions, please reach out to Marc or any other contributers.



