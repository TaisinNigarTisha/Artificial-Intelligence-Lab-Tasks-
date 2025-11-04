import random

def hill_climb(problem, max_iterations=1000):
    
    current_state = problem.get_start_state()
    current_value = problem.evaluate(current_state)

    for _ in range(max_iterations):
        if problem.is_goal_state(current_state):
            return current_state

        successors = problem.get_successors(current_state)
        next_state = None
        next_value = current_value

        for successor, action, step_cost in successors:
            successor_value = problem.evaluate(successor)
            if successor_value > next_value:
                next_state = successor
                next_value = successor_value

        if next_state is None:
            break

        current_state = next_state
        current_value = next_value

    return None

class ExampleProblem:
    def __init__(self):
        self.start_state = 0

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        return state == 10

    def get_successors(self, state):
        return [(state + 1, 'increment', 1), (state - 1, 'decrement', 1)]

    def evaluate(self, state):
        return -abs(10 - state)

if __name__ == "__main__":
    problem = ExampleProblem()
    solution = hill_climb(problem)
    if solution is not None:
        print(f"Solution found: {solution}")
    else:
        print("No solution found.")

