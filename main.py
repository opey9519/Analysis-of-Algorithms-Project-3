import math
import matplotlib.pyplot as plt

import src.graphs as graphs
import src.algorithms as algorithms

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


def visualize_social_graph(graph, shortest_path=None, filename="social_graph.png"):
    """
    Create a simple visual graph using matplotlib.

    This function does not change the SocialGraph or Algorithms classes.
    It only reads the existing graph data and saves a visual image.
    """
    users = sorted(graph.get_users())
    edges = graph.get_weighted_edges()

    if not users:
        print("Graph is empty. No visualization created.")
        return

    # Place nodes evenly around a circle
    positions = {}
    radius = 1.0

    for i, user in enumerate(users):
        angle = 2 * math.pi * i / len(users)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        positions[user] = (x, y)

    # Convert shortest path into edge pairs for highlighting
    highlighted_edges = set()
    if shortest_path:
        for i in range(len(shortest_path) - 1):
            edge = tuple(sorted((shortest_path[i], shortest_path[i + 1])))
            highlighted_edges.add(edge)

    plt.figure(figsize=(9, 7))

    # Draw edges
    for cost, user1, user2, mutuals in edges:
        x1, y1 = positions[user1]
        x2, y2 = positions[user2]

        edge_key = tuple(sorted((user1, user2)))

        if edge_key in highlighted_edges:
            linewidth = 3
            alpha = 1.0
        else:
            linewidth = 1
            alpha = 0.35

        plt.plot([x1, x2], [y1, y2], linewidth=linewidth, alpha=alpha)

        # Add cost label near the middle of the edge
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        plt.text(mid_x, mid_y, f"{cost:.2f}", fontsize=8)

    # Draw nodes
    for user in users:
        x, y = positions[user]
        plt.scatter(x, y, s=900)
        plt.text(x, y, user, ha="center", va="center", fontsize=9)

    plt.title("Social Network Graph with Friendship Costs")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"\nGraph visualization saved as: {filename}")


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

    # Get shortest path so it can be highlighted in the graph image
    shortest_path, total_cost = algo.shortest_path_bellman_ford("Alice", "Frank")

    # Create graph visualization
    visualize_social_graph(
        graph,
        shortest_path=shortest_path,
        filename="social_graph_bellman_ford.png"
    )

    # Depth-First-Search
    algo.print_dfs("Alice")

    # Breadth-First-Search
    algo.print_bfs("Alice")

    # Kruskal's MST
    algo.print_kruskal()

    return


if __name__ == "__main__":
    main()
