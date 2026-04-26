# SocialGraph - Contains graph-related methods
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

    # Convert strength into algorithm-friendly cost
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

    # Print the graph in a readable way for debugging
    def print_graph(self):

        print("Users and their direct friends:")
        for user in sorted(self.friendships):
            print(f"{user}: {sorted(self.friendships[user])}")

    # Print all edges with their mutual-friend strength and cost
    def print_weighted_edges(self):

        print("\nWeighted friendship edges:")
        for cost, user1, user2, mutuals in sorted(self.get_weighted_edges()):
            print(
                f"{user1} -- {user2} | mutual friends: {mutuals} | cost: {cost:.3f}"
            )
