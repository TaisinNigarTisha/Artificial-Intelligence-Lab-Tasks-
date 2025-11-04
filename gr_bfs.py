import heapq

def greedy_best_first_search(start, goal, heuristic_func, graph):
    frontier = []
    heapq.heappush(frontier, (heuristic_func(start), start))

    came_from = {start: None}
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbour, _ in graph.get(current, []):
            if neighbour not in visited:
                came_from[neighbour] = current
                heapq.heappush(frontier, (heuristic_func(neighbour), neighbour))

    # reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('D', 2), ('E', 5)],
    'C': [('A', 4), ('F', 1)],
    'D': [('B', 2)],
    'E': [('B', 5), ('F', 3)],
    'F': [('C', 1), ('E', 3)]
}

heuristic = {
    'A': 7,
    'B': 6,
    'C': 2,
    'D': 1,
    'E': 2,
    'F': 0
}

def h(n):
    return heuristic[n]

path = greedy_best_first_search('A', 'F', h, graph)
print("Path found:", path)
