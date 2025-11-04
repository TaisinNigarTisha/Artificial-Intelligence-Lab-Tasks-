import heapq

def a_star_search(start, goal, heuristic_func, graph):
    frontier = []
    heapq.heappush(frontier, (0 + heuristic_func(start), 0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current_cost, current = heapq.heappop(frontier)

        if current == goal:
            break

        for neighbour, edge_cost in graph.get(current, []):
            new_cost = current_cost + edge_cost
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                priority = new_cost + heuristic_func(neighbour)
                came_from[neighbour] = current
                heapq.heappush(frontier, (priority, new_cost, neighbour))

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
path = a_star_search('A', 'F', h, graph)
print("Path found:", path)