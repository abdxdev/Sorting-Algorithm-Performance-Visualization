#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <stack>
#include <string>
#include <vector>

using namespace std;

class SortingAlgorithms {
public:
    // Insertion Sort //
    static void IInsertionSort(int arr[], int n) {
        for (int i = 1; i < n; i++) {
            int key = arr[i];
            int j = i - 1;

            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j = j - 1;
            }

            arr[j + 1] = key;
        }
    }

    // Quick Sort //
    static int Partition(int arr[], int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr[i], arr[j]);
            }
        }

        swap(arr[i + 1], arr[high]);
        return i + 1;
    }

    static void QuickSort(int arr[], int low, int high) {
        stack<pair<int, int>> stack;
        stack.push({low, high});

        while (!stack.empty()) {
            pair<int, int> p = stack.top();
            stack.pop();
            int low = p.first;
            int high = p.second;

            if (low < high) {
                int pivot_index = Partition(arr, low, high);
                stack.push({low, pivot_index - 1});
                stack.push({pivot_index + 1, high});
            }
        }
    }

    static void IQuickSort(int arr[], int n) {
        QuickSort(arr, 0, n - 1);
    }

    // Heap Sort //
    static void BuildMaxHeap(int arr[], int n) {
        for (int i = n / 2 - 1; i >= 0; i--) {
            Heapify(arr, i, n);
        }
    }

    static void Heapify(int arr[], int i, int n) {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        int largest = i;

        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }

        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }

        if (largest != i) {
            swap(arr[i], arr[largest]);
            Heapify(arr, largest, n);
        }
    }

    static void IHeapSort(int arr[], int n) {
        BuildMaxHeap(arr, n);

        for (int i = n - 1; i > 0; i--) {
            swap(arr[0], arr[i]);
            Heapify(arr, 0, i);
        }
    }

    // Selection Sort //
    static void ISelectionSort(int arr[], int n) {
        int i, j, minIndex, tmp;
        for (i = 0; i < n - 1; i++) {
            minIndex = i;
            for (j = i + 1; j < n; j++)
                if (arr[j] < arr[minIndex])
                    minIndex = j;
            if (minIndex != i) {
                tmp = arr[i];
                arr[i] = arr[minIndex];
                arr[minIndex] = tmp;
            }
        }
    }

    // Bubble Sort //
    static void IBubbleSort(int arr[], int n) {
        int i, j, tmp;
        for (i = 0; i < n - 1; i++) {
            for (j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                }
            }
        }
    }

    // Merge Sort //
    static void Merge(int arr[], int l, int m, int r) {
        int i, j, k;
        int n1 = m - l + 1;
        int n2 = r - m;
        int* L = new int[n1];
        int* R = new int[n2];
        for (i = 0; i < n1; i++)
            L[i] = arr[l + i];
        for (j = 0; j < n2; j++)
            R[j] = arr[m + 1 + j];
        i = 0;
        j = 0;
        k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {
                arr[k] = L[i];
                i++;
            } else {
                arr[k] = R[j];
                j++;
            }
            k++;
        }
        while (i < n1) {
            arr[k] = L[i];
            i++;
            k++;
        }
        while (j < n2) {
            arr[k] = R[j];
            j++;
            k++;
        }
        delete[] L;
        delete[] R;
    }

    static void MergeSort(int arr[], int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            MergeSort(arr, l, m);
            MergeSort(arr, m + 1, r);
            Merge(arr, l, m, r);
        }
    }

    static void IMergeSort(int arr[], int n) {
        MergeSort(arr, 0, n - 1);
    }
};

class Timer {
    chrono::time_point<chrono::high_resolution_clock> start, end;
    chrono::duration<double, nano> elapsed;

    int dataset_size;
    string dataset_variation;
    string sorting_algorithm;

    ofstream& file;

public:
    Timer(int dataset_size, string dataset_variation, string sorting_algorithm, ofstream& file) : dataset_size(dataset_size), dataset_variation(dataset_variation), sorting_algorithm(sorting_algorithm), file(file) {
        start = chrono::high_resolution_clock::now();
        elapsed = chrono::duration<double, nano>::zero();
    }

    ~Timer() {
        end = chrono::high_resolution_clock::now();
        elapsed = end - start;
        file << dataset_size << "," << dataset_variation << "," << sorting_algorithm << "," << elapsed.count() << endl;
        cout << dataset_size << " " << dataset_variation << " " << sorting_algorithm << " " << elapsed.count() << " ns" << endl;
    }
};

void loadDataset(int arr[], int dataset_size, string dataset_variation, string path) {
    ifstream file;
    string line;
    file.open(path + "/" + to_string(dataset_size) + "/" + dataset_variation + ".txt");
    if (file.is_open()) {
        for (int i = 0; i < dataset_size; i++) {
            getline(file, line);
            arr[i] = stoi(line);
        }
        file.close();
    }
}

void storeDataset(int arr[], int dataset_size, string dataset_variation, string path) {

    string directory = path + "/" + to_string(dataset_size);

    if (!filesystem::exists(directory))
        filesystem::create_directories(directory);

    ofstream file;
    file.open(directory + "/" + dataset_variation + ".txt");
    if (file.is_open()) {
        for (int i = 0; i < dataset_size; i++) {
            file << arr[i] << endl;
        }
        file.close();
    }
}

bool isSorted(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}

int main() {
    vector<int> dataset_sizes = {
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
    };
    vector<string> dataset_variations = {
        "Many Duplicates",
        "Nearly Sorted",
        "Reversed",
        "Sorted",
        "Unique Entries",
        "Random",
    };
    map<string, void (*)(int[], int)> sorting_algorithms = {
        {"Insertion Sort", SortingAlgorithms::IInsertionSort},
        {"Quick Sort", SortingAlgorithms::IQuickSort},
        {"Heap Sort", SortingAlgorithms::IHeapSort},
        {"Selection Sort", SortingAlgorithms::ISelectionSort},
        {"Bubble Sort", SortingAlgorithms::IBubbleSort},
        {"Merge Sort", SortingAlgorithms::IMergeSort},
    };

    string directory = "results";
    if (!filesystem::exists(directory))
        filesystem::create_directories(directory);

    ofstream file;
    file.open(directory + "/result.csv");
    if (file.is_open()) {
        file << "Dataset Size,Dataset Variation,Sorting Algorithm,Time Taken" << endl;
    }

    for (int dataset_size : dataset_sizes) {
        int* arr = new int[dataset_size];
        for (string dataset_variation : dataset_variations) {
            loadDataset(arr, dataset_size, dataset_variation, "datasets");
            for (auto sorting_algorithm : sorting_algorithms) {
                try {
                    {
                        Timer timer(dataset_size, dataset_variation, sorting_algorithm.first, file);
                        sorting_algorithm.second(arr, dataset_size);
                    }
                    storeDataset(arr, dataset_size, dataset_variation + "_" + sorting_algorithm.first, "datasets_sorted");
                } catch (exception e) {
                    cout << "Exception: " << e.what() << endl;
                }
            }
        }
        delete[] arr;
    }

    file.close();
    cout << "Verifying all datasets..." << endl;
    for (int dataset_size : dataset_sizes) {
        int* sorted_arr = new int[dataset_size];
        for (string dataset_variation : dataset_variations) {
            for (auto sorting_algorithm : sorting_algorithms) {
                loadDataset(sorted_arr, dataset_size, dataset_variation + "_" + sorting_algorithm.first, "datasets_sorted");
                if (!isSorted(sorted_arr, dataset_size)) {
                    cout << "Dataset: " << dataset_size << " " << dataset_variation << " " << sorting_algorithm.first << " not sorted!" << endl;
                }
            }
        }
        delete[] sorted_arr;
    }
    cout << "All datasets verified!" << endl;

    return 0;
}
