import graphs

friendships = [
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Carol"),
    ("Bob", "David"),
    ("Carol", "Eve"),
    ("David", "Eve"),
    ("David", "Frank"),
    ("Eve", "Frank"),
    ("Carol", "David"),
]


def main():
    graph = graphs.SocialGraph()

    # Add sample friendships
    for f in friendships:
        graph.add_friendship(f[0], f[1])

    # View the basic graph
    graph.print_graph()

    # View edges with mutual-friend-based weights
    graph.print_weighted_edges()

    # Bellman-Ford shortest path example
    graph.print_bellman_ford_result("Alice", "Frank")

    # Depth-First-Search
    graph.print_dfs("Alice")

    # Breadth-First-Search
    graph.print_bfs("Alice")

    return


if __name__ == "__main__":
    main()
