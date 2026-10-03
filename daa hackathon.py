import tkinter as tk
from tkinter import ttk, messagebox
import math


# ============================================================
# TOURIST ATTRACTION DATA
# ============================================================

ATTRACTIONS = [
    {
        "name": "Charminar",
        "time": 1.5,
        "cost": 150,
        "priority": 9,
        "category": "Historical",
        "x": 120,
        "y": 80
    },
    {
        "name": "Salar Jung Museum",
        "time": 2.0,
        "cost": 200,
        "priority": 8,
        "category": "Museum",
        "x": 260,
        "y": 130
    },
    {
        "name": "Birla Mandir",
        "time": 1.0,
        "cost": 60,
        "priority": 8,
        "category": "Religious",
        "x": 430,
        "y": 70
    },
    {
        "name": "Hussain Sagar",
        "time": 1.5,
        "cost": 100,
        "priority": 7,
        "category": "Nature",
        "x": 560,
        "y": 160
    },
    {
        "name": "NTR Gardens",
        "time": 1.0,
        "cost": 80,
        "priority": 6,
        "category": "Nature",
        "x": 460,
        "y": 260
    },
    {
        "name": "Golconda Fort",
        "time": 2.5,
        "cost": 250,
        "priority": 10,
        "category": "Historical",
        "x": 100,
        "y": 330
    },
    {
        "name": "Qutb Shahi Tombs",
        "time": 1.5,
        "cost": 120,
        "priority": 8,
        "category": "Historical",
        "x": 250,
        "y": 370
    },
    {
        "name": "Shilparamam",
        "time": 2.0,
        "cost": 100,
        "priority": 7,
        "category": "Cultural",
        "x": 590,
        "y": 360
    }
]


# ============================================================
# GRAPH CREATION
# ============================================================

def create_graph():
    graph = {}

    for attraction in ATTRACTIONS:
        graph[attraction["name"]] = []

    for i in range(len(ATTRACTIONS)):
        for j in range(i + 1, len(ATTRACTIONS)):
            a = ATTRACTIONS[i]
            b = ATTRACTIONS[j]

            distance = math.sqrt(
                (a["x"] - b["x"]) ** 2 +
                (a["y"] - b["y"]) ** 2
            )

            graph[a["name"]].append((b["name"], distance))
            graph[b["name"]].append((a["name"], distance))

    return graph


GRAPH = create_graph()


# ============================================================
# GREEDY ALGORITHM
# ============================================================

def greedy_algorithm(time_limit, budget_limit):
    attractions = []

    for a in ATTRACTIONS:
        denominator = (
            (a["time"] / time_limit) +
            (a["cost"] / budget_limit)
        )

        score = a["priority"] / denominator

        item = a.copy()
        item["score"] = score
        attractions.append(item)

    attractions.sort(key=lambda x: x["score"], reverse=True)

    selected = []
    decisions = []

    remaining_time = time_limit
    remaining_budget = budget_limit

    for attraction in attractions:

        if (
            attraction["time"] <= remaining_time
            and attraction["cost"] <= remaining_budget
        ):
            selected.append(attraction)

            remaining_time -= attraction["time"]
            remaining_budget -= attraction["cost"]

            decisions.append({
                "name": attraction["name"],
                "decision": "SELECTED",
                "reason": "High value and fits within remaining time and budget."
            })

        else:

            reasons = []

            if attraction["time"] > remaining_time:
                reasons.append("insufficient time")

            if attraction["cost"] > remaining_budget:
                reasons.append("insufficient budget")

            decisions.append({
                "name": attraction["name"],
                "decision": "REJECTED",
                "reason": " and ".join(reasons)
            })

    return selected, decisions


# ============================================================
# 0/1 KNAPSACK ALGORITHM
# ============================================================

def knapsack_algorithm(time_limit, budget_limit):

    # Convert time into half-hour units
    time_units = int(round(time_limit * 2))
    n = len(ATTRACTIONS)

    # DP dictionary:
    # (time_used, budget_used) -> total priority
    dp = {}

    for t in range(time_units + 1):
        for b in range(budget_limit + 1):
            dp[(t, b)] = 0

    for i in range(1, n + 1):

        attraction = ATTRACTIONS[i - 1]

        item_time = int(round(attraction["time"] * 2))
        item_cost = attraction["cost"]
        item_value = attraction["priority"]

        for t in range(time_units, item_time - 1, -1):

            for b in range(budget_limit, item_cost - 1, -1):

                old_value = dp[(t, b)]

                new_value = (
                    dp[(t - item_time, b - item_cost)]
                    + item_value
                )

                dp[(t, b)] = max(old_value, new_value)

    # Find maximum priority
    best_value = 0
    best_t = 0
    best_b = 0

    for t in range(time_units + 1):
        for b in range(budget_limit + 1):

            if dp[(t, b)] > best_value:
                best_value = dp[(t, b)]
                best_t = t
                best_b = b

    # Reconstruct solution
    selected = []

    t = best_t
    b = best_b

    for i in range(n, 0, -1):

        attraction = ATTRACTIONS[i - 1]

        item_time = int(round(attraction["time"] * 2))
        item_cost = attraction["cost"]
        item_value = attraction["priority"]

        if (
            t >= item_time
            and b >= item_cost
            and dp[(t, b)]
            == dp[(t - item_time, b - item_cost)] + item_value
        ):

            selected.append(attraction)

            t -= item_time
            b -= item_cost

    selected.reverse()

    return selected


# ============================================================
# BFS GRAPH TRAVERSAL
# ============================================================

def bfs(start):
    visited = set()
    queue = [start]
    order = []

    while queue:

        current = queue.pop(0)

        if current in visited:
            continue

        visited.add(current)
        order.append(current)

        neighbours = GRAPH[current]

        neighbours = sorted(
            neighbours,
            key=lambda x: x[1]
        )

        for neighbour, distance in neighbours:

            if neighbour not in visited:
                queue.append(neighbour)

    return order


# ============================================================
# ROUTE PLANNING
# NEAREST NEIGHBOUR APPROACH
# ============================================================

def create_route(selected):

    if not selected:
        return []

    remaining = selected.copy()

    route = [remaining.pop(0)]

    while remaining:

        current = route[-1]

        nearest = min(
            remaining,
            key=lambda attraction:
            math.sqrt(
                (current["x"] - attraction["x"]) ** 2 +
                (current["y"] - attraction["y"]) ** 2
            )
        )

        route.append(nearest)
        remaining.remove(nearest)

    return route


# ============================================================
# MAIN APPLICATION
# ============================================================

class TouristPlanner:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Tourist Attraction Planner - DAA Hackathon"
        )

        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        self.root.configure(bg="#f4f7fb")

        self.greedy_result = []
        self.knapsack_result = []
        self.route = []

        self.create_header()
        self.create_input_panel()
        self.create_tabs()

        self.draw_map()

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#123b5d",
            height=90
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="TOURIST ATTRACTION PLANNER",
            font=("Arial", 24, "bold"),
            bg="#123b5d",
            fg="white"
        ).pack(
            pady=(15, 2)
        )

        tk.Label(
            header,
            text="Plan Smarter • Explore More • Powered by DAA Algorithms",
            font=("Arial", 11),
            bg="#123b5d",
            fg="#dbeafe"
        ).pack()

    # ========================================================
    # INPUT PANEL
    # ========================================================

    def create_input_panel(self):

        panel = tk.Frame(
            self.root,
            bg="white",
            bd=1,
            relief="solid"
        )

        panel.pack(
            fill="x",
            padx=15,
            pady=12
        )

        tk.Label(
            panel,
            text="Available Time (hours)",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=12
        )

        self.time_entry = tk.Entry(
            panel,
            width=12,
            font=("Arial", 11)
        )

        self.time_entry.insert(
            0,
            "8"
        )

        self.time_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            panel,
            text="Maximum Budget (₹)",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        self.budget_entry = tk.Entry(
            panel,
            width=12,
            font=("Arial", 11)
        )

        self.budget_entry.insert(
            0,
            "1500"
        )

        self.budget_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        tk.Label(
            panel,
            text="Algorithm",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.algorithm = ttk.Combobox(
            panel,
            values=[
                "Compare Both",
                "Greedy",
                "0/1 Knapsack"
            ],
            state="readonly",
            width=18
        )

        self.algorithm.set(
            "Compare Both"
        )

        self.algorithm.grid(
            row=0,
            column=5,
            padx=5
        )

        generate_button = tk.Button(
            panel,
            text="🚀 GENERATE PLAN",
            command=self.generate_plan,
            font=("Arial", 11, "bold"),
            bg="#0f766e",
            fg="white",
            activebackground="#115e59",
            activeforeground="white",
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )

        generate_button.grid(
            row=0,
            column=6,
            padx=15
        )

        reset_button = tk.Button(
            panel,
            text="RESET",
            command=self.reset,
            font=("Arial", 10, "bold"),
            bg="#64748b",
            fg="white",
            padx=12,
            pady=8,
            relief="flat",
            cursor="hand2"
        )

        reset_button.grid(
            row=0,
            column=7,
            padx=5
        )

    # ========================================================
    # TABS
    # ========================================================

    def create_tabs(self):

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.attraction_tab = tk.Frame(
            self.notebook,
            bg="white"
        )

        self.result_tab = tk.Frame(
            self.notebook,
            bg="white"
        )

        self.log_tab = tk.Frame(
            self.notebook,
            bg="white"
        )

        self.map_tab = tk.Frame(
            self.notebook,
            bg="white"
        )

        self.notebook.add(
            self.attraction_tab,
            text="Attractions"
        )

        self.notebook.add(
            self.result_tab,
            text="Results"
        )

        self.notebook.add(
            self.log_tab,
            text="Decision Log"
        )

        self.notebook.add(
            self.map_tab,
            text="Route Map"
        )

        self.create_attraction_tab()
        self.create_result_tab()
        self.create_log_tab()
        self.create_map_tab()

    # ========================================================
    # ATTRACTION TAB
    # ========================================================

    def create_attraction_tab(self):

        title = tk.Label(
            self.attraction_tab,
            text="Hyderabad Tourist Attractions",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#123b5d"
        )

        title.pack(
            pady=15
        )

        columns = (
            "Attraction",
            "Category",
            "Time",
            "Cost",
            "Priority"
        )

        tree = ttk.Treeview(
            self.attraction_tab,
            columns=columns,
            show="headings",
            height=14
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=170,
                anchor="center"
            )

        for attraction in ATTRACTIONS:

            tree.insert(
                "",
                "end",
                values=(
                    attraction["name"],
                    attraction["category"],
                    f'{attraction["time"]} hrs',
                    f'₹{attraction["cost"]}',
                    attraction["priority"]
                )
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    # ========================================================
    # RESULT TAB
    # ========================================================

    def create_result_tab(self):

        self.result_text = tk.Text(
            self.result_tab,
            font=("Consolas", 11),
            bg="#f8fafc",
            fg="#0f172a",
            wrap="word"
        )

        self.result_text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ========================================================
    # DECISION LOG TAB
    # ========================================================

    def create_log_tab(self):

        self.log_text = tk.Text(
            self.log_tab,
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#0f172a",
            wrap="word"
        )

        self.log_text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ========================================================
    # MAP TAB
    # ========================================================

    def create_map_tab(self):

        title = tk.Label(
            self.map_tab,
            text="🗺 Tourist Attraction Route Map",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#123b5d"
        )

        title.pack(
            pady=(10, 2)
        )

        subtitle = tk.Label(
            self.map_tab,
            text="Gray = available attractions    Green = selected route",
            font=("Arial", 10),
            bg="white",
            fg="#64748b"
        )

        subtitle.pack()

        self.canvas = tk.Canvas(
            self.map_tab,
            bg="#eaf4f2",
            highlightthickness=1,
            highlightbackground="#cbd5e1"
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.draw_map()
        )

    # ========================================================
    # DRAW MAP
    # ========================================================

    def draw_map(self):

        if not hasattr(self, "canvas"):
            return

        self.canvas.delete(
            "all"
        )

        width = max(
            self.canvas.winfo_width(),
            800
        )

        height = max(
            self.canvas.winfo_height(),
            450
        )

        # ----------------------------------------------------
        # Draw title
        # ----------------------------------------------------

        self.canvas.create_text(
            20,
            20,
            text="Hyderabad Attraction Graph",
            anchor="nw",
            font=("Arial", 14, "bold"),
            fill="#123b5d"
        )

        # ----------------------------------------------------
        # Scale original coordinates
        # ----------------------------------------------------

        min_x = min(
            a["x"]
            for a in ATTRACTIONS
        )

        max_x = max(
            a["x"]
            for a in ATTRACTIONS
        )

        min_y = min(
            a["y"]
            for a in ATTRACTIONS
        )

        max_y = max(
            a["y"]
            for a in ATTRACTIONS
        )

        map_width = width - 120
        map_height = height - 100

        def convert(x, y):

            px = (
                60
                + (x - min_x)
                / (max_x - min_x)
                * map_width
            )

            py = (
                70
                + (y - min_y)
                / (max_y - min_y)
                * map_height
            )

            return px, py

        positions = {}

        for attraction in ATTRACTIONS:

            positions[
                attraction["name"]
            ] = convert(
                attraction["x"],
                attraction["y"]
            )

        # ----------------------------------------------------
        # Draw graph edges
        # ----------------------------------------------------

        for name, neighbours in GRAPH.items():

            x1, y1 = positions[name]

            for neighbour, distance in neighbours:

                if name < neighbour:

                    x2, y2 = positions[neighbour]

                    self.canvas.create_line(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill="#cbd5e1",
                        width=1
                    )

        # ----------------------------------------------------
        # Draw selected route
        # ----------------------------------------------------

        if len(self.route) > 1:

            for i in range(
                len(self.route) - 1
            ):

                first = self.route[i]
                second = self.route[i + 1]

                x1, y1 = positions[
                    first["name"]
                ]

                x2, y2 = positions[
                    second["name"]
                ]

                self.canvas.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#0f766e",
                    width=5,
                    arrow=tk.LAST,
                    arrowshape=(12, 14, 5)
                )

        # ----------------------------------------------------
        # Selected attractions
        # ----------------------------------------------------

        selected_names = {
            a["name"]
            for a in self.route
        }

        for attraction in ATTRACTIONS:

            name = attraction["name"]

            x, y = positions[name]

            selected = (
                name in selected_names
            )

            self.canvas.create_oval(
                x - 13,
                y - 13,
                x + 13,
                y + 13,
                fill="#0f766e"
                if selected
                else "#94a3b8",
                outline="white",
                width=2
            )

            self.canvas.create_text(
                x,
                y + 25,
                text=name,
                font=("Arial", 8, "bold"),
                fill="#0f172a"
            )

        # ----------------------------------------------------
        # Route text
        # ----------------------------------------------------

        if self.route:

            route_string = (
                " → ".join(
                    a["name"]
                    for a in self.route
                )
            )

            self.canvas.create_text(
                20,
                height - 25,
                text="Recommended Route: "
                + route_string,
                anchor="w",
                font=("Arial", 9, "bold"),
                fill="#0f766e"
            )

        else:

            self.canvas.create_text(
                width - 20,
                20,
                text="Generate a plan to see the route",
                anchor="ne",
                font=("Arial", 9, "bold"),
                fill="#64748b"
            )

    # ========================================================
    # GENERATE PLAN
    # ========================================================

    def generate_plan(self):

        try:

            time_limit = float(
                self.time_entry.get()
            )

            budget_limit = int(
                self.budget_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers."
            )

            return

        if time_limit <= 0:

            messagebox.showerror(
                "Invalid Time",
                "Available time must be greater than 0."
            )

            return

        if budget_limit <= 0:

            messagebox.showerror(
                "Invalid Budget",
                "Budget must be greater than 0."
            )

            return

        selected_algorithm = (
            self.algorithm.get()
        )

        # ----------------------------------------------------
        # Run Greedy
        # ----------------------------------------------------

        self.greedy_result, greedy_log = (
            greedy_algorithm(
                time_limit,
                budget_limit
            )
        )

        # ----------------------------------------------------
        # Run Knapsack
        # ----------------------------------------------------

        self.knapsack_result = (
            knapsack_algorithm(
                time_limit,
                budget_limit
            )
        )

        # ----------------------------------------------------
        # Select final result
        # ----------------------------------------------------

        if selected_algorithm == "Greedy":

            final_selection = (
                self.greedy_result
            )

        elif selected_algorithm == "0/1 Knapsack":

            final_selection = (
                self.knapsack_result
            )

        else:

            # For comparison mode, use the
            # higher-priority result for route display.
            greedy_priority = sum(
                a["priority"]
                for a in self.greedy_result
            )

            knapsack_priority = sum(
                a["priority"]
                for a in self.knapsack_result
            )

            if knapsack_priority >= greedy_priority:
                final_selection = (
                    self.knapsack_result
                )
            else:
                final_selection = (
                    self.greedy_result
                )

        # ----------------------------------------------------
        # Create route
        # ----------------------------------------------------

        self.route = create_route(
            final_selection
        )

        # ----------------------------------------------------
        # Display results
        # ----------------------------------------------------

        self.show_results(
            time_limit,
            budget_limit
        )

        # ----------------------------------------------------
        # Display logs
        # ----------------------------------------------------

        self.show_logs(
            greedy_log,
            time_limit,
            budget_limit
        )

        # ----------------------------------------------------
        # Refresh map
        # ----------------------------------------------------

        self.draw_map()

        # Open result tab
        self.notebook.select(
            self.result_tab
        )

    # ========================================================
    # SHOW RESULTS
    # ========================================================

    def show_results(
        self,
        time_limit,
        budget_limit
    ):

        self.result_text.delete(
            "1.0",
            tk.END
        )

        def summary(selected):

            total_time = sum(
                a["time"]
                for a in selected
            )

            total_cost = sum(
                a["cost"]
                for a in selected
            )

            total_priority = sum(
                a["priority"]
                for a in selected
            )

            return (
                total_time,
                total_cost,
                total_priority
            )

        greedy_time, greedy_cost, greedy_priority = (
            summary(
                self.greedy_result
            )
        )

        knap_time, knap_cost, knap_priority = (
            summary(
                self.knapsack_result
            )
        )

        self.result_text.insert(
            tk.END,
            "TOURIST ATTRACTION PLANNER\n"
        )

        self.result_text.insert(
            tk.END,
            "=" * 70 + "\n\n"
        )

        self.result_text.insert(
            tk.END,
            f"Available Time : {time_limit} hours\n"
        )

        self.result_text.insert(
            tk.END,
            f"Maximum Budget : ₹{budget_limit}\n\n"
        )

        self.result_text.insert(
            tk.END,
            "GREEDY ALGORITHM\n"
        )

        self.result_text.insert(
            tk.END,
            "-" * 50 + "\n"
        )

        self.result_text.insert(
            tk.END,
            f"Selected Attractions : "
            f"{len(self.greedy_result)}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Total Time : "
            f"{greedy_time:.1f} hours\n"
        )

        self.result_text.insert(
            tk.END,
            f"Total Cost : "
            f"₹{greedy_cost}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Total Priority : "
            f"{greedy_priority}\n\n"
        )

        for i, attraction in enumerate(
            self.greedy_result,
            1
        ):

            self.result_text.insert(
                tk.END,
                f"{i}. {attraction['name']} "
                f"({attraction['time']} hrs, "
                f"₹{attraction['cost']})\n"
            )

        self.result_text.insert(
            tk.END,
            "\n\n0/1 KNAPSACK ALGORITHM\n"
        )

        self.result_text.insert(
            tk.END,
            "-" * 50 + "\n"
        )

        self.result_text.insert(
            tk.END,
            f"Selected Attractions : "
            f"{len(self.knapsack_result)}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Total Time : "
            f"{knap_time:.1f} hours\n"
        )

        self.result_text.insert(
            tk.END,
            f"Total Cost : "
            f"₹{knap_cost}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Total Priority : "
            f"{knap_priority}\n\n"
        )

        for i, attraction in enumerate(
            self.knapsack_result,
            1
        ):

            self.result_text.insert(
                tk.END,
                f"{i}. {attraction['name']} "
                f"({attraction['time']} hrs, "
                f"₹{attraction['cost']})\n"
            )

        self.result_text.insert(
            tk.END,
            "\n\nRECOMMENDED VISIT ORDER\n"
        )

        self.result_text.insert(
            tk.END,
            "=" * 50 + "\n"
        )

        if self.route:

            for i, attraction in enumerate(
                self.route,
                1
            ):

                self.result_text.insert(
                    tk.END,
                    f"{i}. {attraction['name']}\n"
                )

        else:

            self.result_text.insert(
                tk.END,
                "No feasible route found.\n"
            )

        self.result_text.insert(
            tk.END,
            "\n\nALGORITHM COMPLEXITIES\n"
        )

        self.result_text.insert(
            tk.END,
            "-" * 50 + "\n"
        )

        self.result_text.insert(
            tk.END,
            "Greedy     : O(n log n)\n"
        )

        self.result_text.insert(
            tk.END,
            "Knapsack   : O(n × T × B)\n"
        )

        self.result_text.insert(
            tk.END,
            "BFS        : O(V + E)\n"
        )

        self.result_text.insert(
            tk.END,
            "Route      : O(k²)\n"
        )

    # ========================================================
    # SHOW DECISION LOG
    # ========================================================

    def show_logs(
        self,
        greedy_log,
        time_limit,
        budget_limit
    ):

        self.log_text.delete(
            "1.0",
            tk.END
        )

        self.log_text.insert(
            tk.END,
            "GREEDY DECISION LOG\n"
        )

        self.log_text.insert(
            tk.END,
            "=" * 70 + "\n\n"
        )

        for index, decision in enumerate(
            greedy_log,
            1
        ):

            symbol = (
                "✓"
                if decision["decision"]
                == "SELECTED"
                else "✗"
            )

            self.log_text.insert(
                tk.END,
                f"{index}. {symbol} "
                f"{decision['name']}\n"
            )

            self.log_text.insert(
                tk.END,
                f"   Decision : "
                f"{decision['decision']}\n"
            )

            self.log_text.insert(
                tk.END,
                f"   Reason   : "
                f"{decision['reason']}\n\n"
            )

        self.log_text.insert(
            tk.END,
            "\nKNAPSACK EXPLANATION\n"
        )

        self.log_text.insert(
            tk.END,
            "=" * 70 + "\n\n"
        )

        self.log_text.insert(
            tk.END,
            "The 0/1 Knapsack algorithm evaluates "
            "combinations of attractions using "
            "dynamic programming.\n\n"
        )

        self.log_text.insert(
            tk.END,
            "Each attraction can either be selected "
            "or not selected.\n"
        )

        self.log_text.insert(
            tk.END,
            "The algorithm respects both time and "
            "budget constraints.\n\n"
        )

        self.log_text.insert(
            tk.END,
            "BFS GRAPH TRAVERSAL\n"
        )

        self.log_text.insert(
            tk.END,
            "=" * 70 + "\n\n"
        )

        start = ATTRACTIONS[0]["name"]

        traversal = bfs(start)

        self.log_text.insert(
            tk.END,
            "Starting Node: "
            + start
            + "\n\n"
        )

        self.log_text.insert(
            tk.END,
            " → ".join(traversal)
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.time_entry.delete(
            0,
            tk.END
        )

        self.time_entry.insert(
            0,
            "8"
        )

        self.budget_entry.delete(
            0,
            tk.END
        )

        self.budget_entry.insert(
            0,
            "1500"
        )

        self.algorithm.set(
            "Compare Both"
        )

        self.greedy_result = []
        self.knapsack_result = []
        self.route = []

        self.result_text.delete(
            "1.0",
            tk.END
        )

        self.log_text.delete(
            "1.0",
            tk.END
        )

        self.draw_map()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TouristPlanner(
        root
    )

    root.mainloop()
