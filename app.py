import streamlit as st
import numpy as np
import csv
import plotly.graph_objects as go
import pandas as pd
import os
import json


def plot_data(variation, table_data, algo_arrangement, table_header, csv_file, selected_unit, time_conversion):
    fig = go.Figure()
    x = np.array(table_header)

    # Convert data to selected unit
    table_data_converted = table_data / time_conversion

    for algo_index, algo in enumerate(algo_arrangement):
        y = table_data_converted[algo_index]
        if np.any(~np.isnan(y)):
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=algo, line=dict(width=2), marker=dict(size=8, opacity=0.7)))

    fig.update_layout(
        title=f"Performance",
        xaxis_title="Input Size [N]",
        yaxis_title=f"Time Taken ({selected_unit})",
        legend_title="Sorting Algorithms",
        template="plotly_white",
        hovermode="closest",
        margin=dict(l=0, r=0, t=50, b=0),
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
                    time = float(row["Time Taken"])
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
    csv_files = []
    for file in os.listdir("results/"):
        if file.endswith(".csv"):
            csv_files.append(f"results/{file}")
    specs = json.load(open("results/specs.json", "r"))
    table_header = [1000, 2000, 3000, 4000, 5000, 10000, 20000, 40000, 80000, 160000, 250000, 500000]
    algos = ["Bubble Sort", "Selection Sort", "Quick Sort", "Insertion Sort", "Merge Sort", "Heap Sort"]
    variations = ["Many Duplicates", "Nearly Sorted", "Reversed", "Sorted", "Unique Entries", "Random"]
    time_units = {"NanoSecond (ns)": 1, "Microsecond (μs)": 1_000, "Millisecond (ms)": 1_000_000, "Second (s)": 1_000_000_000, "Minute (m)": 60_000_000_000, "Hour (h)": 3_600_000_000_000}

    tables = read_data_from_csv(csv_files, variations, algos, table_header)
    avg_tables = calculate_averages(tables, variations, algos, table_header)

    st.sidebar.title("Options")
    variation = st.sidebar.selectbox("Select Data Variation", variations)
    selected_unit = st.sidebar.selectbox("Select Time Unit", list(time_units.keys()))
    time_conversion = time_units[selected_unit]

    # {
    #     "PC1": {
    #         "model": "Dell Latitude 5400",
    #         "cpu": "Intel Core i5-8600K",
    #         "ram": "16GB DDR4"
    #     },
    #     "PC2": {
    #         "model": "Dell Latitude E7250",
    #         "cpu": "Intel Core i5-5600K",
    #         "ram": "8GB DDR4"
    #     }
    # }

    specifications = ""

    for pc, spec in specs.items():
        specifications += f"##### {pc}\n"
        for key, value in spec.items():
            specifications += f"- {key.title()}: {value}\n"
        specifications += "\n"

    st.markdown(
        f"""                
# Sorting Algorithm Performance Visualization

This application visualizes the performance of various sorting algorithms on different datasets. The data is collected from the results of the sorting algorithm benchmarking.

## Data Variation: {variation}

The following data is in {selected_unit}.

#### System Specifications
{specifications}

"""
    )

    for csv_file in csv_files:
        st.markdown(f"### Dataset: {csv_file.split('/')[-1].split('.')[0]}")
        selected_table = tables[variation][csv_file]
        table_df = pd.DataFrame(selected_table / time_conversion, columns=table_header, index=algos)

        if not table_df.empty:
            st.table(table_df)
        else:
            st.write("No valid data available for this variation.")

        plot_data(variation, selected_table, algos, table_header, csv_file, selected_unit, time_conversion)
        st.markdown("---")

    st.markdown("### Dataset: Average")
    avg_table_df = pd.DataFrame(avg_tables[variation] / time_conversion, columns=table_header, index=algos)
    st.table(avg_table_df)
    plot_data(variation, avg_tables[variation], algos, table_header, "Average", selected_unit, time_conversion)


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="Sorting Algorithm Performance Visualization",
        page_icon="📊",
        initial_sidebar_state="expanded",
    )
    main()
