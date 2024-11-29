import streamlit as st
import numpy as np
import csv
import plotly.graph_objects as go
import pandas as pd


def plot_data(variation, table_data, algo_arrangement, table_header, csv_file):
    fig = go.Figure()
    x = np.array(table_header)

    for algo_index, algo in enumerate(algo_arrangement):
        y = table_data[algo_index]
        if np.any(~np.isnan(y)):
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=algo, line=dict(width=2), marker=dict(size=8, opacity=0.7)))

    fig.update_layout(
        title=f"Performance for {variation.replace('_', ' ').title()} Input from {csv_file}",
        xaxis_title="Input Size [N]",
        yaxis_title="Time Taken (ms)",
        legend_title="Sorting Algorithms",
        template="plotly_white",
        hovermode="closest",
    )

    st.plotly_chart(fig, key=f"{variation}_{csv_file}_plot")


def read_data_from_csv(csv_files, variations, algos, table_header):
    tables = {variation: {file: np.full((len(algos), len(table_header)), np.nan) for file in csv_files} for variation in variations}

    for csv_file in csv_files:
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    size = int(row["Dataset Size"])
                    variation = row["Dataset Variation"].strip()
                    algo = row["Sorting Algorithm"].strip()
                    time = float(row["Time Taken"]) / 1_000_000

                    if variation in variations and size in table_header:
                        algo_index = algos.index(algo)
                        size_index = table_header.index(size)
                        tables[variation][csv_file][algo_index, size_index] = time
                except Exception as e:
                    st.write(f"Error processing row: {row}, Error: {e}")
                    continue

    return tables


def calculate_averages(tables, variations, algos, table_header):
    avg_tables = {variation: np.full((len(algos), len(table_header)), np.nan) for variation in variations}

    for variation in variations:
        for algo_index in range(len(algos)):
            for size_index in range(len(table_header)):
                times = [tables[variation][file][algo_index, size_index] for file in tables[variation] if not np.isnan(tables[variation][file][algo_index, size_index])]
                if times:
                    avg_tables[variation][algo_index, size_index] = np.mean(times)

    return avg_tables


def main():
    csv_files = ["results.csv"]
    table_header = [1000, 2000, 3000, 4000, 5000, 10000, 20000, 40000, 80000, 160000, 250000, 500000]
    algos = ["Insertion Sort", "Quick Sort", "Heap Sort", "Selection Sort", "Bubble Sort", "Merge Sort"]
    variations = ["Many Duplicates", "Nearly Sorted", "Reversed", "Sorted", "Unique Entries", "Random"]

    tables = read_data_from_csv(csv_files, variations, algos, table_header)

    avg_tables = calculate_averages(tables, variations, algos, table_header)

    st.title("Sorting Algorithm Performance Visualization")
    st.sidebar.title("Options")

    variation = st.sidebar.selectbox("Select Data Variation", variations)

    for csv_file in csv_files:
        selected_table = tables[variation][csv_file]
        table_df = pd.DataFrame(selected_table, columns=table_header, index=algos)
        st.write(f"Data from {csv_file} for {variation}:")

        if not table_df.empty:
            st.table(table_df)
        else:
            st.write("No valid data available for this variation.")

        plot_data(variation, selected_table, algos, table_header, csv_file)

    st.write(f"Averages for {variation}:")
    avg_table_df = pd.DataFrame(avg_tables[variation], columns=table_header, index=algos)
    st.table(avg_table_df)

    plot_data(variation, avg_tables[variation], algos, table_header, "Average")


if __name__ == "__main__":
    main()
