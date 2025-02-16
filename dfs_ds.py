import tkinter as tk
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def dfs_util(self, v, visited, result, edge_order):
        visited.add(v)
        result.append(v)

        for neighbor in self.graph[v]:
            if neighbor not in visited:
                edge_order.append((v, neighbor))  # Track the edge being traversed
                self.dfs_util(neighbor, visited, result, edge_order)

    def dfs(self, start_vertex):
        visited = set()
        result = []
        edge_order = []  # Store the order in which edges are traversed
        self.dfs_util(start_vertex, visited, result, edge_order)
        return result, edge_order


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DFS Graph Traversal with Visualization")
        self.graph = Graph()

        # GUI Components
        self.label = tk.Label(root, text="Enter edges (e.g., '0 1' for an edge from 0 to 1):")
        self.label.pack()

        self.entry = tk.Entry(root, width=30)
        self.entry.pack()

        self.add_edge_button = tk.Button(root, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack()

        self.start_label = tk.Label(root, text="Enter start vertex for DFS:")
        self.start_label.pack()

        self.start_entry = tk.Entry(root, width=10)
        self.start_entry.pack()

        self.dfs_button = tk.Button(root, text="Run DFS", command=self.run_dfs)
        self.dfs_button.pack()

        self.result_label = tk.Label(root, text="DFS Result:")
        self.result_label.pack()

        self.result_text = tk.Text(root, height=5, width=30)
        self.result_text.pack()

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

    def add_edge(self):
        edge_input = self.entry.get()
        try:
            u, v = map(int, edge_input.split())
            self.graph.add_edge(u, v)
            self.entry.delete(0, tk.END)
            self.result_text.insert(tk.END, f"Added edge: {u} -> {v}\n")
            self.draw_graph()
        except ValueError:
            self.result_text.insert(tk.END, "Invalid input. Please enter two integers separated by a space.\n")

    def run_dfs(self):
        start_vertex = self.start_entry.get()
        try:
            start_vertex = int(start_vertex)
            result, edge_order = self.graph.dfs(start_vertex)
            self.result_text.insert(tk.END, f"DFS Traversal: {result}\n")
            self.highlight_traversal(edge_order)
        except ValueError:
            self.result_text.insert(tk.END, "Invalid start vertex. Please enter an integer.\n")

    def draw_graph(self):
        """Draw the graph using networkx and matplotlib."""
        self.ax.clear()
        G = nx.DiGraph()

        for u in self.graph.graph:
            for v in self.graph.graph[u]:
                G.add_edge(u, v)

        pos = nx.spring_layout(G)  # Layout for the graph
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        self.canvas.draw()

    def highlight_traversal(self, edge_order):
        """Highlight the edges in the order they are traversed during DFS."""
        G = nx.DiGraph()

        for u in self.graph.graph:
            for v in self.graph.graph[u]:
                G.add_edge(u, v)

        pos = nx.spring_layout(G)
        self.ax.clear()

        # Draw all edges in gray
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color='lightblue', node_size=500, font_size=10,
                edge_color='gray', width=1)

        # Highlight traversed edges in red
        for i, (u, v) in enumerate(edge_order):
            nx.draw_networkx_edges(G, pos, ax=self.ax, edgelist=[(u, v)], edge_color='red', width=2)
            self.canvas.draw()
            self.root.update()  # Update the GUI to show the highlighted edge
            self.root.after(1000)  # Pause for 1 second to visualize the traversal

        self.canvas.draw()


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()