import sqlite3
from random import randint, uniform


class DFBnB:
    def __init__(self, branching_factor, depth, db_path, edge_cost_distribution="zero_or_one", verbose=False):
        """
        Initialize the DFBnB class.

        :param branching_factor: Number of children each node has.
        :param depth: Depth of the tree.
        :param db_path: Path to the SQLite database.
        :param edge_cost_distribution: Distribution of edge costs.
                                       Options: "zero_or_one", "uniform", "custom".
        :param verbose: Boolean to control verbose output.
        """
        self.bound = float('inf')
        self.optimal_path = None
        self.expanded_nodes = []
        self.branching_factor = branching_factor
        self.depth = depth
        self.db_path = db_path
        self.edge_cost_distribution = edge_cost_distribution
        self.verbose = verbose

        self.start_node = 1 if self.depth else None
        self.is_goal_node = lambda node: node >= branching_factor ** depth
        self.heuristic = lambda node: 0  # Heuristic currently not used
        self.initialize_database()

    def initialize_database(self):
        """Initializes the database and creates the tree structure."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        self._create_edges_table(cursor)
        if self.depth > 0:
            self._populate_edges_table(cursor)

        conn.commit()
        conn.close()

    def _create_edges_table(self, cursor):
        """Creates the edges table in the database."""
        cursor.execute('''DROP TABLE IF EXISTS edges''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS edges (
            from_node INTEGER,
            to_node INTEGER,
            weight INTEGER
        )
        ''')

    def _populate_edges_table(self, cursor):
        """Populates the edges table with a randomly generated tree."""
        total_nodes = self.branching_factor ** (self.depth + 1)
        for node in range(1, total_nodes):
            if node < self.branching_factor ** self.depth:
                self._add_edges_for_node(cursor, node)

    def _add_edges_for_node(self, cursor, node):
        """Adds edges for a given node in the tree."""
        for branch in range(1, self.branching_factor + 1):
            child_node = (node - 1) * self.branching_factor + branch + 1
            edge_weight = self._generate_edge_cost()
            cursor.execute('''
            INSERT INTO edges (from_node, to_node, weight) VALUES (?, ?, ?)
            ''', (node, child_node, edge_weight))

    def _generate_edge_cost(self):
        """Generates an edge cost based on the selected distribution."""
        if self.edge_cost_distribution == "zero_or_one":
            return randint(0, 1)
        elif self.edge_cost_distribution == "uniform":
            return randint(1, 10)
        elif self.edge_cost_distribution == "custom":
            # Example: A custom distribution (you can define it as needed)
            return int(uniform(1, 5))  # Adjust as necessary
        else:
            raise ValueError("Unsupported edge cost distribution")

    def depth_first_search_with_pruning(self):
        """Performs a Depth-First Branch-and-Bound search using the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        self._perform_search(cursor)

        conn.close()

        if self.verbose:
            self.print_search_results()
        return self.optimal_path, self.expanded_nodes

    def _perform_search(self, cursor):
        """Performs the recursive search for the optimal path."""

        def search(current_path, current_cost):
            current_node = current_path[-1]

            if current_node not in self.expanded_nodes:
                self.expanded_nodes.append(current_node)

            if self.verbose:
                self._print_verbose_output(current_path, current_node, current_cost)

            if self._should_prune(current_node, current_cost):
                return

            if self.is_goal_node(current_node):
                self._update_optimal_path(current_path, current_cost)
            else:
                self._explore_children(cursor, current_node, current_path, current_cost, search)

        search([self.start_node], 0)

    def _print_verbose_output(self, current_path, current_node, current_cost):
        """Prints detailed search progress information."""
        print(f'PATH: {current_path}, Curr_Node: {current_node}, Cost: {current_cost}, Bound: {self.bound}')

    def _should_prune(self, current_node, current_cost):
        """Determines if a path should be pruned based on its cost."""
        return current_cost + self.heuristic(current_node) >= self.bound

    def _update_optimal_path(self, current_path, current_cost):
        """Updates the optimal path and bound if a better path is found."""
        self.optimal_path = current_path
        self.bound = current_cost

    def _explore_children(self, cursor, current_node, current_path, current_cost, search_func):
        """Explores the child nodes of the current node."""
        cursor.execute('''
        SELECT to_node, weight FROM edges WHERE from_node = ? ORDER BY weight ASC
        ''', (current_node,))
        edges = cursor.fetchall()

        for to_node, weight in edges:
            search_func(current_path + [to_node], current_cost + weight)

    def print_search_results(self):
        """Prints the final results of the search."""
        print("-------------------------------------------------------------------------------")
        print(f"Best Path: {'-> '.join(map(str, self.optimal_path))}, with the Cost: {self.bound}")
        print(f"Nodes Expanded: {', '.join(map(str, self.expanded_nodes))}")
        print("-------------------------------------------------------------------------------")
