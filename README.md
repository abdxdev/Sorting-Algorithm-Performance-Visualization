# Sorting Algorithm Performance Visualization

This Streamlit app visualizes the performance of various sorting algorithms across different input sizes and dataset variations. It reads data from multiple CSV files, displays the results in an interactive table, and provides plots to compare sorting algorithm performance.

![](screenshots/screenshot_1.png)

## Workflow Overview

1. **Generate Datasets**: Use the `generate_datasets.py` script to generate datasets with various variations.
2. **Run Sorting Algorithms**: Implement the sorting algorithms in `SortingAlgorithms.cpp`, compile the code using C++17, and calculate the sorting times for each dataset.
3. **Store Results**: The results will be saved into CSV files (e.g., `abd_results.csv` and `abd_results copy.csv`).
4. **Visualize Data**: Use this Streamlit app to visualize the performance of sorting algorithms on the datasets and calculate averages across multiple CSV files.

## Features

- Visualizes performance data from multiple CSV files for sorting algorithms.
- Allows selection of dataset variations (e.g., "Many Duplicates", "Sorted", etc.) from the sidebar.
- Displays the performance of each sorting algorithm for various input sizes.
- Calculates and displays average performance across all CSV files.
- Interactive plots generated using Plotly to compare the sorting algorithms.

## Requirements

- Python 3.7 or higher
- Streamlit
- Plotly
- Pandas
- Numpy
- C++17 compatible compiler (e.g., GCC, Clang)

## Installation

1. Clone the repository or download the code.
2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Install the required Python libraries:
   ```bash
   pip install streamlit plotly pandas numpy
   ```

## Workflow

### Step 1: Generate Datasets

Before you calculate the sorting times, you need to generate datasets with various variations. You can use the `generate_datasets.py` script to generate datasets like:

- "Many Duplicates"
- "Nearly Sorted"
- "Reversed"
- "Sorted"
- "Unique Entries"
- "Random"

Run the script like this:

```bash
python generate_datasets.py
```

This will create dataset files that you will use for benchmarking.

### Step 2: Calculate Sorting Times

Next, compile and run the sorting algorithms in `SortingAlgorithms.cpp` to sort the datasets generated in Step 1. The `SortingAlgorithms.cpp` file includes implementations of various sorting algorithms like:

- Quick Sort
- Merge Sort
- Heap Sort
- Insertion Sort
- Selection Sort
- Bubble Sort

Make sure you are using a C++17 compatible compiler. For example, with GCC you can compile it like this:

```bash
g++ -std=c++17 SortingAlgorithms.cpp -o SortingAlgorithms
```

Then, run the compiled program to calculate the sorting times for each dataset and save the results to a CSV file.

### Step 3: Visualize the Data

Once the CSV files (e.g., `results.csv`) are ready, you can use the Streamlit app to visualize the sorting performance data.

Run the Streamlit app with the following command:

```bash
streamlit run app.py
```

This will launch the app in your browser, where you can:

- Select dataset variations from the sidebar.
- View the performance data for different sorting algorithms.
- See a plot of the sorting algorithm performance.

### CSV File Format

Ensure that your CSV files contain the following columns:

- **Dataset Size**: The input size of the dataset (e.g., 1000, 2000, etc.).
- **Dataset Variation**: The variation of the dataset (e.g., "Many Duplicates", "Sorted").
- **Sorting Algorithm**: The name of the sorting algorithm (e.g., "Quick Sort", "Merge Sort").
- **Time Taken**: The time taken by the sorting algorithm (in nanoseconds, will be converted to seconds).

## License

This project is licensed under the MIT License.
