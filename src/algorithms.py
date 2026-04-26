# Algorithms - Contains algorithm-related methods


class Algorithms:
    def __init__(self, graph):
        self.graph = graph
    # ---------------------------------------------------------------------------------
    # Traversal
    # Algorithm: DFS

    def dfs(self, start):
        # Returns: order of vertices visited from start ("Alice")
        if start not in self.graph.friendships:
            raise ValueError(
                f"User '{start}' does not exist in the graph.")

        visited = set()  # Track visited users
        order = []  # Store traversal order

        # DFS utility
        def dfs_helper(user):
            visited.add(user)
            order.append(user)

            # Recursively visits all unvisited neighbors
            for neighbor in self.graph.get_neighbors(user):
                if neighbor not in visited:
                    dfs_helper(neighbor)

        dfs_helper(start)
        return order

    # Print dfs path result in a readable format.
    def print_dfs(self, start):
        if start is None:
            print(f"No path exists from {start}")
        else:
            print("\nDFS Traversal starting from Alice:")
            dfs_result = self.dfs(start)
            print(" -> ".join(dfs_result))

    # Algorithm: BFS

    def bfs(self, start):

        # Returns: order of vertices visited from start ("Alice")
        if start not in self.graph.friendships:
            raise ValueError(
                f"User '{start}' does not exist in the graph.")

        visited = set()  # Track visited users
        queue = [start]  # Use list as a queue
        visited.add(start)

        order = []  # Store traversal order

        while queue:
            user = queue.pop(0)  # Remove from front of queue (FIFO)
            order.append(user)

            # Visit neighbors in sorted order for consistent results
            for neighbor in self.graph.get_neighbors(user):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    # Print bfs path result in a readable format
    def print_bfs(self, start):
        if start is None:
            print(f"No path exists from {start}")
        else:
            print("\nBFS Traversal starting from Alice:")
            bfs_result = self.bfs(start)
            print(" -> ".join(bfs_result))

    # ---------------------------------------------------------------------------------
    # Shortest Path
    # Algorithm: Bellman-Ford

    # Compute shortest paths from a source user using Bellman-Ford.

    def bellman_ford(self, source):

        # Returns:
        # distances: dictionary of shortest known cost from source to each user
        # predecessors: dictionary used to reconstruct shortest paths

        # Note: Since friendships are undirected, each edge is relaxed in both directions

        if source not in self.graph.friendships:
            raise ValueError(
                f"Source user '{source}' does not exist in the graph.")

        users = self.graph.get_users()

        # Step 1: initialize distances
        distances = {user: float("inf") for user in users}
        predecessors = {user: None for user in users}
        distances[source] = 0

        # Step 2: get all weighted undirected edges once
        edges = self.graph.get_weighted_edges()

        # Step 3: relax all edges |V| - 1 times
        for _ in range(len(users) - 1):
            updated = False

            for cost, user1, user2, mutuals in edges:
                # Relax user1 -> user2
                if distances[user1] != float("inf") and distances[user1] + cost < distances[user2]:
                    distances[user2] = distances[user1] + cost
                    predecessors[user2] = user1
                    updated = True

                # Relax user2 -> user1
                if distances[user2] != float("inf") and distances[user2] + cost < distances[user1]:
                    distances[user1] = distances[user2] + cost
                    predecessors[user1] = user2
                    updated = True

            # Optimization: stop early if no update happened
            if not updated:
                break

        # Step 4: check for negative-weight cycles
        for cost, user1, user2, mutuals in edges:
            if distances[user1] != float("inf") and distances[user1] + cost < distances[user2]:
                raise ValueError("Graph contains a negative-weight cycle.")
            if distances[user2] != float("inf") and distances[user2] + cost < distances[user1]:
                raise ValueError("Graph contains a negative-weight cycle.")

        return distances, predecessors

    # Return the shortest path and total cost from source to target using Bellman-Ford
    def shortest_path_bellman_ford(self, source, target):

        distances, predecessors = self.bellman_ford(source)

        if target not in self.graph.friendships:
            raise ValueError(
                f"Target user '{target}' does not exist in the graph.")

        if distances[target] == float("inf"):
            return None, float("inf")

        # Reconstruct path by walking backward from target
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = predecessors[current]

        path.reverse()
        return path, distances[target]

    # Print the shortest path result in a readable format.
    def print_bellman_ford_result(self, source, target):

        path, total_cost = self.shortest_path_bellman_ford(source, target)

        if path is None:
            print(f"\nNo path exists from {source} to {target}.")
        else:
            print(f"\nBellman-Ford shortest path from {source} to {target}:")
            print(" -> ".join(path))
            print(f"Total path cost: {total_cost:.3f}")
    # ---------------------------------------------------------------------------------
    # MST
    # Algorithm: Kruskal

    def kruskal(self):

        # sort all edges by cost, cheapest first (strongest mutual connection = lowest cost)
        edges = sorted(self.graph.get_weighted_edges())
        users = self.graph.get_users()

        # union-find: each user starts as its own component
        parent = {user: user for user in users}
        rank = {user: 0 for user in users}

        def find(x):
            # path compression: flatten the tree on the way up to the root
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            # merge the two components; return false if they're already connected
            rx, ry = find(x), find(y)
            if rx == ry:
                return False
            # union by rank: attach the shorter tree under the taller one
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1
            return True

        mst = []
        total_cost = 0.0

        # greedily pick the cheapest edge that connects two different components
        for cost, user1, user2, mutuals in edges:
            if union(user1, user2):
                mst.append((cost, user1, user2, mutuals))
                total_cost += cost

        return mst, total_cost

    # print the mst edges and total cost in a readable format
    def print_kruskal(self):

        mst, total_cost = self.kruskal()

        print("\nKruskal's MST (minimum spanning friendship tree):")
        for cost, user1, user2, mutuals in mst:
            print(
                f"  {user1} -- {user2} | mutual friends: {mutuals} | cost: {cost:.3f}")
        print(f"Total MST cost: {total_cost:.3f}")
