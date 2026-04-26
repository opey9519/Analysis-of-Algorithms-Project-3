import random
import time
import tracemalloc
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt

# Allow this file to import from project-level src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src import graphs
from src import algorithms


DATA_DIR = PROJECT_ROOT / "data"


def generate_social_graph(num_users, density):

    # Generate a synthetic undirected social graph.

    # num_users = number of vertices
    # density = probability of an edge between two users

    graph = graphs.SocialGraph()
    users = [f"User{i}" for i in range(num_users)]

    for user in users:
        graph.add_user(user)

    for i in range(num_users):
        for j in range(i + 1, num_users):
            if random.random() < density:
                graph.add_friendship(users[i], users[j])

    # Force at least one connected chain so paths always exist
    for i in range(num_users - 1):
        graph.add_friendship(users[i], users[i + 1])

    return graph


def measure_algorithm(algorithm_name, function):

    # Measure execution time and peak memory usage for one algorithm call

    tracemalloc.start()

    start_time = time.perf_counter()
    function()
    end_time = time.perf_counter()

    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "Algorithm": algorithm_name,
        "Execution Time (seconds)": end_time - start_time,
        "Peak Memory (KB)": peak_memory / 1024
    }


def run_single_experiment(graph_label, graph, source, target):

    # Run DFS, BFS, Bellman-Ford, and Kruskal on one graph

    algo = algorithms.Algorithms(graph)

    vertex_count = len(graph.get_users())
    edge_count = len(graph.get_weighted_edges())

    results = []

    results.append(measure_algorithm("DFS", lambda: algo.dfs(source)))
    results.append(measure_algorithm("BFS", lambda: algo.bfs(source)))
    results.append(
        measure_algorithm(
            "Bellman-Ford",
            lambda: algo.shortest_path_bellman_ford(source, target)
        )
    )
    results.append(measure_algorithm("Kruskal", lambda: algo.kruskal()))

    for row in results:
        row["Graph Type"] = graph_label
        row["Vertices"] = vertex_count
        row["Edges"] = edge_count

    return results


def print_results_table(results):

    # Print benchmark results in a readable console table

    print("\nBenchmark Results")
    print("=" * 105)
    print(
        f"{'Graph Type':<22} "
        f"{'Algorithm':<15} "
        f"{'Vertices':<10} "
        f"{'Edges':<10} "
        f"{'Time (sec)':<18} "
        f"{'Memory (KB)':<15}"
    )
    print("-" * 105)

    for row in results:
        print(
            f"{row['Graph Type']:<22} "
            f"{row['Algorithm']:<15} "
            f"{row['Vertices']:<10} "
            f"{row['Edges']:<10} "
            f"{row['Execution Time (seconds)']:<18.8f} "
            f"{row['Peak Memory (KB)']:<15.2f}"
        )

    print("=" * 105)


def save_results_csv(results, filename):

    # Save benchmark results to a CSV file

    fieldnames = [
        "Graph Type",
        "Algorithm",
        "Vertices",
        "Edges",
        "Execution Time (seconds)",
        "Peak Memory (KB)"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"CSV results saved as: {filename}")


def create_bar_chart(results, metric, filename, title, y_label):

    # Create a bar chart for either execution time or memory usage

    labels = [f"{row['Graph Type']}\n{row['Algorithm']}" for row in results]
    values = [row[metric] for row in results]

    plt.figure(figsize=(14, 6))
    plt.bar(labels, values)
    plt.xticks(rotation=75, ha="right")
    plt.title(title)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"Graph saved as: {filename}")


def run_benchmarks():

    random.seed(42)

    # Create data folder if it does not exist
    DATA_DIR.mkdir(exist_ok=True)

    experiments = [
        # graph label, number of users, density
        ("Small Sparse", 20, 0.10),
        ("Small Dense", 20, 0.60),
        ("Large Sparse", 100, 0.04),
        ("Large Dense", 100, 0.20),
    ]

    all_results = []

    for graph_label, num_users, density in experiments:
        graph = generate_social_graph(num_users, density)

        source = "User0"
        target = f"User{num_users - 1}"

        experiment_results = run_single_experiment(
            graph_label,
            graph,
            source,
            target
        )

        all_results.extend(experiment_results)

    print_results_table(all_results)

    save_results_csv(
        all_results,
        DATA_DIR / "benchmark_results.csv"
    )

    create_bar_chart(
        all_results,
        metric="Execution Time (seconds)",
        filename=DATA_DIR / "benchmark_execution_time.png",
        title="Algorithm Execution Time Comparison",
        y_label="Execution Time (seconds)"
    )

    create_bar_chart(
        all_results,
        metric="Peak Memory (KB)",
        filename=DATA_DIR / "benchmark_memory_usage.png",
        title="Algorithm Memory Usage Comparison",
        y_label="Peak Memory (KB)"
    )

    print("\nBenchmark complete.")
    print(f"All benchmark files saved inside: {DATA_DIR}")


if __name__ == "__main__":
    run_benchmarks()
