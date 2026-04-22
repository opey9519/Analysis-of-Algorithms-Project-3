# Code entry point
class SocialGraph:
    def __init__(self):
        # Adjacency structure for direct friendships only
        # Example:
        # {
        #   "Alice": {"Bob", "Carol"},
        #   "Bob": {"Alice", "David"}
        # }
        self.friendships = {}

    def add_user(self, user):
        """Add a user to the graph if they do not already exist."""
        if user not in self.friendships:
            self.friendships[user] = set()

    def add_friendship(self, user1, user2):
        """
        Add an undirected friendship edge between two users.
        Since this is a social friendship graph, the relationship is mutual.
        """
        if user1 == user2:
            return  # Ignore self-loops

        self.add_user(user1)
        self.add_user(user2)

        self.friendships[user1].add(user2)
        self.friendships[user2].add(user1)

    def get_users(self):
        """Return a list of all users (vertices)."""
        return list(self.friendships.keys())

    def get_neighbors(self, user):
        """Return the direct friends of a user."""
        return self.friendships.get(user, set())

    def mutual_friends_count(self, user1, user2):
        """
        Return the number of mutual friends between user1 and user2.
        """
        if user1 not in self.friendships or user2 not in self.friendships:
            return 0

        return len(self.friendships[user1].intersection(self.friendships[user2]))

    def friendship_strength(self, user1, user2):
        """
        Raw relationship strength = number of mutual friends.
        """
        return self.mutual_friends_count(user1, user2)

    def friendship_cost(self, user1, user2):
        """
        Convert strength into algorithm-friendly cost.
        Lower cost means a stronger connection.

        Formula:
            cost = 1 / (mutual_friends + 1)

        Examples:
            0 mutual friends -> 1.0
            1 mutual friend  -> 0.5
            4 mutual friends -> 0.2
        """
        mutuals = self.mutual_friends_count(user1, user2)
        return 1 / (mutuals + 1)

    def get_weighted_edges(self):
        """
        Return all undirected edges as tuples:
            (cost, user1, user2, mutual_friend_count)

        We only include each undirected edge once.
        This is useful for Kruskal and for displaying/debugging the graph.
        """
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

    def print_graph(self):
        """
        Print the graph in a readable way for debugging.
        """
        print("Users and their direct friends:")
        for user in sorted(self.friendships):
            print(f"{user}: {sorted(self.friendships[user])}")

    def print_weighted_edges(self):
        """
        Print all edges with their mutual-friend strength and cost.
        """
        print("\nWeighted friendship edges:")
        for cost, user1, user2, mutuals in sorted(self.get_weighted_edges()):
            print(
                f"{user1} -- {user2} | mutual friends: {mutuals} | cost: {cost:.3f}"
            )

def main():
    if __name__ == "__main__":
    graph = SocialGraph()

    # Add sample friendships
    graph.add_friendship("Alice", "Bob")
    graph.add_friendship("Alice", "Carol")
    graph.add_friendship("Bob", "Carol")
    graph.add_friendship("Bob", "David")
    graph.add_friendship("Carol", "Eve")
    graph.add_friendship("David", "Eve")
    graph.add_friendship("David", "Frank")
    graph.add_friendship("Eve", "Frank")
    graph.add_friendship("Carol", "David")

    # View the basic graph
    graph.print_graph()

    # View edges with mutual-friend-based weights
    graph.print_weighted_edges()
    return


if __name__ == "__main__":
    main()
