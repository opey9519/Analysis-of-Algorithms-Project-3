class SocialGraph:
    def __init__(self):
        self.friendships = {}
       
    # Add a user to the graph if they do not already exist
    def add_user(self, user):
        if user not in self.friendships:
            self.friendships[user] = set()

    # Add an undirected friendship edge between two users 
    # This relationship is mutual since it's a social friendship graph
    def add_friendship(self, user1, user2):

        if user1 == user2:
            return  # Ignore self-loops

        self.add_user(user1)
        self.add_user(user2)

        self.friendships[user1].add(user2)
        self.friendships[user2].add(user1)

    # Return a list of all users (vertices)
    def get_users(self):
        return list(self.friendships.keys())

    # Return the direct friends of a user
    def get_neighbors(self, user):
        return self.friendships.get(user, set())

    # Return the number of mutual friends between user1 and user2
    def mutual_friends_count(self, user1, user2):
        if user1 not in self.friendships or user2 not in self.friendships:
            return 0

        return len(self.friendships[user1].intersection(self.friendships[user2]))

    # Raw relationship strength = number of mutual friends.
    def friendship_strength(self, user1, user2):

        return self.mutual_friends_count(user1, user2)

    # Convert strength into algorithm-friendly cost.
    # Lower cost means a stronger connection.
    def friendship_cost(self, user1, user2):

        # Formula: cost = 1 / (mutual_friends + 1)

        # Examples:
        # 0 mutual friends -> 1.0
        # 1 mutual friend  -> 0.5
        # 4 mutual friends -> 0.2

        mutuals = self.mutual_friends_count(user1, user2)
        return 1 / (mutuals + 1)

    # Return all undirected edges as tuples:
    # (cost, user1, user2, mutual_friend_count)
    def get_weighted_edges(self):

        edges = []
        seen = set()

        for user1 in self.friendships:
            for user2 in self.friendships[user1]:
                edge_key = tuple(sorted((user1, user2)))
                if edge_key not in seen:
                    seen.add(edge_key)

                    mutuals = self.mutual_friends_count(user1, user2)
                    cost = self.friendship_cost(user1, user2)

                    edges.append((cost, user1, user2, mutuals))

        return edges

    # Print the graph in a readable way for debugging.
    def print_graph(self):

        print("Users and their direct friends:")
        for user in sorted(self.friendships):
            print(f"{user}: {sorted(self.friendships[user])}")

    # Print all edges with their mutual-friend strength and cost.
    def print_weighted_edges(self):

        print("\nWeighted friendship edges:")
        for cost, user1, user2, mutuals in sorted(self.get_weighted_edges()):
            print(
                f"{user1} -- {user2} | mutual friends: {mutuals} | cost: {cost:.3f}"
            )
    #---------------------------------------------------------------------------------
    # Traversal
    # Algorithm: BSF or DSF


    #---------------------------------------------------------------------------------
    # Shortest Path
    # Algorithm: Bellman-Ford

    # Compute shortest paths from a source user using Bellman-Ford.
    def bellman_ford(self, source):

        # Returns:
        # distances: dictionary of shortest known cost from source to each user
        # predecessors: dictionary used to reconstruct shortest paths

        # Note: Since friendships are undirected, each edge is relaxed in both directions

        if source not in self.friendships:
            raise ValueError(f"Source user '{source}' does not exist in the graph.")

        users = self.get_users()

        # Step 1: initialize distances
        distances = {user: float("inf") for user in users}
        predecessors = {user: None for user in users}
        distances[source] = 0

        # Step 2: get all weighted undirected edges once
        edges = self.get_weighted_edges()

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

        if target not in self.friendships:
            raise ValueError(f"Target user '{target}' does not exist in the graph.")

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
    #---------------------------------------------------------------------------------
    # MST
    # Algorithm: Kruskal
    def kruskal():
        pass