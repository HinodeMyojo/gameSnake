import heapq

def heuristic(a, b):
    """
    Calculate the Manhattan distance between points a and b in 3D space.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def find_path(position, target, fences):
    """
    Find the best path in 3D space using the A* algorithm.

    Args:
        position (tuple): Starting position (x, y, z).
        target (tuple): Target position (x, y, z).
        fences (set): Set of obstacle coordinates as (x, y, z).

    Returns:
        list: List of positions forming the path from position to target.
              Returns an empty list if no path is found.
    """
    # Priority queue for open nodes
    open_set = []
    heapq.heappush(open_set, (0, position))

    # Dictionaries for tracking paths
    came_from = {}

    # g_score: Cost from start to current node
    g_score = {position: 0}

    # f_score: Estimated cost from start to target through current node
    f_score = {position: heuristic(position, target)}

    # Keep track of visited nodes
    visited = set()
    i = 0
    while open_set:
        i += 1
        if i > 5000:
            print("break")
            return (0, -1, 0)
        # Get the node with the lowest f_score
        _, current = heapq.heappop(open_set)

        # If we reach the target, reconstruct the path
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(position)
            result = path[::-1]
            if len(result) == 1:
                print("We reach end!")
                return (0, -1, 0)
            result = result[1]
            direction = (result[0] - position[0], result[1] - position[1], result[2] - position[2]);
            print(direction)
            return direction  # Return reversed path

        visited.add(current)

        # Explore neighbors (6 directions in 3D space)
        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            neighbor = (current[0] + dx, current[1] + dy, current[2] + dz)

            # Skip obstacles and already visited nodes
            if neighbor in fences or neighbor in visited:
                continue
            # Tentative g_score for this neighbor
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                # This path to neighbor is better than any previous one
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, target)

                # Add neighbor to the open set
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # If we reach here, no path was found
    return []
