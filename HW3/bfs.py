# De-que: list-like container with fast appends and pops on either end
from collections import deque

# BFS algorithm in maze finding
def bfs(grid, start, goal, width, height, obs):
    # initiate the queue with stating point (as tuple of 2 numbers (x,y))
    queue = deque([[start]])
    print("Starting queue", queue)

    # initiate explored set
    seen = set([start])

    # loop until queue is not empty
    while queue:
        # Remove and return an element from the left side of the deque
        # Add that element to path
        path = queue.popleft()
        print(" Current path", path)

        # extract the last element of path
        x, y = path[-1]
        # print(x, y)

        # Check if goal state is met
        if grid[y][x] == goal:
            return path

        # Loop through neighboring points:
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            # First check if x2,y2 is a valid coordinate
            # Then check if they are obstacle
            # Finally check if coordinate has been visited
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != obs and (x2, y2) not in seen:
                # Add to queue with the WHOLE path from starting point
                queue.append(path + [(x2, y2)])
                # add to visited nodes
                seen.add((x2, y2))
                print("Current queue", queue)
                print("Current visited nodes", seen)

def main():
    obs, clear, goal = "#", ".", "*"
    width, height = 10, 5
    start = (5, 2)
    grid = ["..........",
            "..*#...##.",
            "..##...#*.",
            ".....###..",
            "......*..."]
    path = bfs(grid, start, goal, width, height, obs)
    print("Final path", path)
main()