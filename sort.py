import random
from typing import List, Tuple
from time import perf_counter
import csv

def bubble_sort(a: List[int]) -> Tuple[List[int], int, int]:
    n, comps, swaps = len(a), 0, 0
    arr = a[:]
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comps += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:  
            break
    return arr, comps, swaps

def selection_sort(a: List[int]) -> Tuple[List[int], int, int]:
    n, comps, swaps = len(a), 0, 0
    arr = a[:]
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, comps, swaps

def insertion_sort(a: List[int]) -> Tuple[List[int], int, int]:
    n, comps, moves = len(a), 0, 0
    arr = a[:]
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                moves += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr, comps, moves

def make_case(n: int):
    rand = [random.randint(0, 10000) for _ in range(n)]
    sorted_case = sorted(rand)
    reverse_case = sorted(rand, reverse=True)
    return {"random": rand, "sorted": sorted_case, "reverse": reverse_case}

def time_run(sort_fn, data: List[int]) -> Tuple[float, int, int]:
    t0 = perf_counter()
    sorted_out, comps, swaps_moves = sort_fn(data)
    t_ms = (perf_counter() - t0) * 1000
    assert sorted_out == sorted(data), "Sorting failed!"
    return t_ms, comps, swaps_moves

def fmt_row(row: dict) -> str:
    return f"{row['algo']:<14} {row['n']:>6} {row['case']:<8} {row['time_ms']:>10.2f} {row['comparisons']:>12} {row['swaps_moves']:>12}"

def get_input_sizes():
    n_sets = int(input("Enter the number of size sets: "))
    sizes = []
    for i in range(n_sets):
        size = int(input(f"Enter size for set {i+1}: "))
        sizes.append(size)
    return sizes

def main():
    random.seed(42)
    sizes = get_input_sizes()
    compare_case = sizes[1] if len(sizes) > 1 else sizes[0]   

    algos = [
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Selection Sort", selection_sort),
    ]

    results = []

    for n in sizes:
        case = make_case(n)
        for name, fn in algos:
            t_ms, comps, swaps_moves = time_run(fn, case["random"])
            results.append({
                "algo": name,
                "n": n,
                "case": "random",
                "time_ms": t_ms,
                "comparisons": comps,
                "swaps_moves": swaps_moves
            })

    case_cmp = make_case(compare_case)
    for case_name, arr in case_cmp.items():
        for name, fn in algos:
            t_ms, comps, swaps_moves = time_run(fn, arr)
            results.append({
                "algo": name,
                "n": compare_case,
                "case": case_name,
                "time_ms": t_ms,
                "comparisons": comps,
                "swaps_moves": swaps_moves
            })

    header = "ALGO           n  CASE      TIME(ms)   COMPARISONS  SWAPS/MOVES"
    print(header)
    print("-" * len(header))
    for r in results:
        print(fmt_row(r))

    with open("sort_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["algo", "n", "case", "time_ms", "comparisons", "swaps_moves"]
        )
        writer.writeheader()
        writer.writerows(results)

    print("\nResults written to sort_results.csv")

if __name__ == "__main__":
    main()
