import random
import os


def generate_datasets(n, output_dir="datasets"):
    """
    Generate various types of datasets and save them to files.

    Args:
        n (int): The size of each dataset.
        output_dir (str): Directory where the files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Nearly sorted data
    print("Nearly sorted data")
    nearly_sorted = list(range(1, n + 1))
    for _ in range(n // 10):  # Swap 10% of the elements to make it nearly sorted
        i, j = random.sample(range(n), 2)
        nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]
    with open(os.path.join(output_dir, "Nearly Sorted.txt"), "w") as f:
        f.write("\n".join(map(str, nearly_sorted)))

    # Sorted data
    print("Sorted data")
    sorted_data = list(range(1, n + 1))
    with open(os.path.join(output_dir, "Sorted.txt"), "w") as f:
        f.write("\n".join(map(str, sorted_data)))

    # Reversed data
    print("Reversed data")
    reversed_data = list(range(n, 0, -1))
    with open(os.path.join(output_dir, "Reversed.txt"), "w") as f:
        f.write("\n".join(map(str, reversed_data)))

    # Data with many duplicates
    print("Data with many duplicates")
    duplicates = [random.randint(1, n // 10) for _ in range(n)]
    with open(os.path.join(output_dir, "Many Duplicates.txt"), "w") as f:
        f.write("\n".join(map(str, duplicates)))

    # Data with unique entries
    print("Data with unique entries")
    unique_entries = random.sample(range(1, n * 10), n)
    with open(os.path.join(output_dir, "Unique Entries.txt"), "w") as f:
        f.write("\n".join(map(str, unique_entries)))

    # Random data
    print("Random data")
    random_data = [random.randint(1, n * 10) for _ in range(n)]
    with open(os.path.join(output_dir, "Random.txt"), "w") as f:
        f.write("\n".join(map(str, random_data)))


input_sizes = [
    1000,
    2000,
    3000,
    4000,
    5000,
    10000,
    20000,
    40000,
    80000,
    160000,
    250000,
    500000,
]

os.makedirs("datasets", exist_ok=True)

for n in input_sizes:
    print(f"Generating datasets of size {n}")
    generate_datasets(n, output_dir=f"datasets/{n}")
