# --- 1. Graph and Domain Definition ---

# The graph represents the divisions of Bangladesh (nodes) and their shared borders (edges).
# Key: Division Name (Node)
# Value: List of adjacent divisions (Edges)
BANGLADESH_GRAPH = {
    'Rangpur': ['Rajshahi', 'Mymensingh'],
    'Rajshahi': ['Rangpur', 'Mymensingh', 'Dhaka', 'Khulna'],
    'Mymensingh': ['Rangpur', 'Rajshahi', 'Dhaka', 'Sylhet'],
    'Sylhet': ['Mymensingh', 'Dhaka', 'Chattogram'],
    # Dhaka is highly connected, adjacent to 6 other divisions
    'Dhaka': ['Rajshahi', 'Mymensingh', 'Sylhet', 'Khulna', 'Barishal', 'Chattogram'],
    'Khulna': ['Rajshahi', 'Dhaka', 'Barishal'],
    'Barishal': ['Khulna', 'Dhaka', 'Chattogram'],
    'Chattogram': ['Sylhet', 'Dhaka', 'Barishal']
}

# The available colors (domain for the constraint satisfaction problem).
COLORS = ['Red', 'Green', 'Blue', 'Yellow']

# Dictionary to store the final assigned color for each division.
# This will be updated during the backtracking process.
coloring_solution = {}


# --- 2. Constraint Checking Function ---

def is_safe(division, color, graph, coloring):
    """
    Checks if assigning the given color to the division is safe (i.e., does not 
    conflict with any of its already colored neighbors).
    
    Args:
        division (str): The current division to color.
        color (str): The color to check.
        graph (dict): The adjacency graph.
        coloring (dict): The current state of assigned colors.
        
    Returns:
        bool: True if safe, False otherwise.
    """
    # Iterate through all adjacent divisions
    for neighbor in graph.get(division, []):
        # Check if the neighbor has already been colored
        if neighbor in coloring and coloring[neighbor] == color:
            return False  # Conflict found!
    
    return True # No conflicts, the assignment is safe


# --- 3. Backtracking Algorithm Implementation ---

def solve_map_coloring(divisions, graph, colors, coloring):
    """
    Uses the backtracking algorithm to find a valid coloring for the map.
    
    Args:
        divisions (list): List of all divisions to be colored.
        graph (dict): The adjacency graph.
        colors (list): The list of available colors.
        coloring (dict): The current assignment of colors.
        
    Returns:
        bool: True if a solution is found, False otherwise (triggers backtracking).
    """
    
    # Base Case: If all divisions have been successfully colored, we found a solution.
    if len(coloring) == len(divisions):
        return True

    # Selection: Pick an unassigned division.
    # We use a simple strategy: the first division not yet in the 'coloring' dictionary.
    # A more advanced heuristic (like Most Constrained Variable, e.g., Dhaka)
    # would make the search faster, but this keeps it simple.
    
    uncolored_division = None
    for division in divisions:
        if division not in coloring:
            uncolored_division = division
            break

    # Should not happen if the base case check is correct, but good for robustness.
    if uncolored_division is None:
        return True 

    # Recursive Step: Try assigning a color to the uncolored division.
    for color in colors:
        if is_safe(uncolored_division, color, graph, coloring):
            # 1. Assignment: Tentatively assign the color
            coloring[uncolored_division] = color

            # 2. Recurse: Move to the next uncolored division
            if solve_map_coloring(divisions, graph, colors, coloring):
                return True # Solution found down this path

            # 3. Backtrack: If the recursion returned False, the current color choice
            #    did not lead to a full solution. Undo the assignment and try the next color.
            del coloring[uncolored_division]

    # Exhausted all colors for this division without finding a solution.
    return False


# --- 4. Main Execution ---

def main():
    # List of divisions sorted alphabetically for consistent iteration
    all_divisions = sorted(list(BANGLADESH_GRAPH.keys()))
    
    # Note: We pass the 'coloring_solution' dictionary which is modified in place
    # by the recursive function.
    if solve_map_coloring(all_divisions, BANGLADESH_GRAPH, COLORS, coloring_solution):
        print("✅ Solution Found!")
        
        # Determine the number of colors used
        used_colors = set(coloring_solution.values())
        print(f"Number of colors used: {len(used_colors)} (K={len(COLORS)})")
        print("\n--- Map Coloring Assignment ---")
        
        # Print the solution in a clean format
        for division in all_divisions:
            color = coloring_solution[division]
            # Use ASCII color codes for better visualization in the console
            color_code = ''
            if color == 'Red': color_code = '\033[91m'
            elif color == 'Green': color_code = '\033[92m'
            elif color == 'Blue': color_code = '\033[94m'
            elif color == 'Yellow': color_code = '\033[93m'
            reset_code = '\033[0m'

            print(f"{division:<12}: {color_code}{color}{reset_code}")

    else:
        print("❌ No solution found with the given constraints (K=4 colors).")


if __name__ == "__main__":
    # Increase recursion limit for potentially deep backtracking paths
    sys.setrecursionlimit(2000)
    main()

# Note on Forward Checking:
# Forward checking would involve checking the remaining valid colors (domains)
# of unassigned neighbors immediately after an assignment. If an assignment
# reduces a neighbor's domain to zero, we immediately prune the current path.
# This code uses basic Backtracking (checking only assigned neighbors).
