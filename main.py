import src.graphs as graphs
import src.algorithms as algorithms
import analysis.visualize as visualize

from analysis.benchmark import run_benchmarks

from pathlib import Path


friendships = [
    # Core cluster
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Carol"),
    ("Bob", "David"),
    ("Carol", "Eve"),
    ("David", "Eve"),
    ("David", "Frank"),
    ("Eve", "Frank"),
    ("Carol", "David"),
    # Extended network
    ("Frank", "Grace"),
    ("Eve", "Grace"),
    ("Grace", "Henry"),
    ("Henry", "Bob"),
    ("Henry", "David"),
    ("Ivan", "Henry"),
    ("Ivan", "Alice"),
    ("Ivan", "Carol"),
]


def main():
    # Graph-related methods and properties
    graph = graphs.SocialGraph()

    # Add sample friendships
    for f in friendships:
        graph.add_friendship(f[0], f[1])

    # Algorithm-related methods
    algo = algorithms.Algorithms(graph)

    # View the basic graph
    graph.print_graph()

    # View edges with mutual-friend-based weights
    graph.print_weighted_edges()

    # Bellman-Ford shortest path example
    algo.print_bellman_ford_result("Alice", "Frank")

    # Depth-First-Search
    algo.print_dfs("Alice")

    # Breadth-First-Search
    algo.print_bfs("Alice")

    # Kruskal's MST
    algo.print_kruskal()

    # Run benchmark and create all benchmark files inside data/
    run_benchmarks()

    # Get shortest path for highlighting
    shortest_path, total_cost = algo.shortest_path_bellman_ford(
        "Alice", "Frank")

    # Create data folder
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Save social graph image inside data/
    visualize.visualize_social_graph(
        graph,
        shortest_path=shortest_path,
        filename=str(data_dir / "social_graph.png"),
    )
    return


if __name__ == "__main__":
    main()
