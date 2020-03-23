from math import sqrt
from heapq import heappop, heappush

def find_path (source_point, destination_point, mesh):
    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to
    Returns:
        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """


    s_and_d = []

    for x in mesh['boxes']:
        if x[0] <= source_point[0] and x[2] <= source_point[1] and x[1] >= source_point[0] and x[3] >= source_point[1]:
            s_and_d.insert(0, x)
        if x[0] <= destination_point[0] and x[2] <= destination_point[1] and x[1] >= destination_point[0] and x[3] >= destination_point[1]:
            s_and_d.append(x)

    s_and_d_copy = s_and_d.copy()

    if len(s_and_d) == 1:
        print("No Path!")
        raise SystemExit


    start_box = s_and_d.pop(0)
    destination = s_and_d.pop(0)

    detail_points = {}

    detail_points[start_box] = source_point
    current_point = source_point

    # The priority queue
    queue = [(0, start_box, 'destination')]
    heappush(queue, (0, destination, 'start_box'))

    # The dictionary that will be returned with the costs
    distance_front = {}
    distance_back = {}
    distance_front[start_box] = 0
    distance_back[destination] = 0

    # The dictionary that will store the backpointers
    front_prev = {}
    back_prev = {}
    front_prev[start_box] = None
    back_prev[destination] = None

    path = []
    last_box = start_box
    while queue:
        current_dist, current_box, goal = heappop(queue)

        # Check if current node is the destination
        if current_box in front_prev or current_box in back_prev:
            if current_box in front_prev:
                current_back_node = front_prev[current_box]
                while current_back_node is not None:
                    path.append(current_back_node)
                    current_back_node = front_prev[current_back_node]
                current_back_node = back_prev[last_box]
                while current_back_node is not None:
                    path.insert(0, current_back_node)
                    current_back_node = back_prev[current_back_node]
            else:
                current_back_node = back_prev[current_box]
                while current_back_node is not None:
                    path.append(current_back_node)
                    current_back_node = back_prev[current_back_node]
                current_back_node = front_prev[last_box]
                while current_back_node is not None:
                    path.insert(0, current_back_node)
                    current_back_node = front_prev[current_back_node]
            break

        # Calculate cost from current note to all the adjacent ones
        for x in mesh['adj'][current_box]:
            point_check = helper_box(detail_points[current_box], current_box, x)
            pathcost = current_dist + euclidean_helper(detail_points[current_box], destination_point) + euclidean_helper(detail_points[current_box], point_check)

            # If the cost is new
            if goal == 'destination':
                if x not in distance_front or pathcost < distance_front[x]:
                    distance_front[x] = distance_front[x] + euclidean_helper(detail_points[current_box], point_check)
                    front_prev[x] = current_box
                    detail_points[x] = point_check
                    heappush(queue, (pathcost, x, 'destination'))
            else:
                if x not in distance_back or pathcost < distance_back[x]:
                    distance_back[x] = distance_back[x] + euclidean_helper(detail_points[current_box], point_check)
                    back_prev[x] = current_box
                    detail_points[x] = point_check
                    heappush(queue, (pathcost, x, 'start_box'))
        last_box = current_box

    newPath = []
    newBoxes = []

    print(path)

    for i in range(len(path)-1):
        newPath.append((detail_points[path[i]], detail_points[path[i+1]]))
        newBoxes.append(path[i])

    newPath.append((detail_points[path[0]], destination_point))
    newBoxes.append(start_box)

    return newPath, newBoxes

def euclidean_helper (current, test):
    first_in = (current[0]-test[0])**2
    second_in = (current[1]-test[1])**2

    sum = sqrt(first_in+second_in)

    return sum

def helper_box (current_point, box1, box2):
    b1x1 = box1[0]
    b1x2 = box1[1]
    b2x1 = box2[0]
    b2x2 = box2[1]

    x_range = [max(b1x1, b2x1), min(b1x2, b2x2)]

    b1y1 = box1[2]
    b1y2 = box1[3]
    b2y1 = box2[2]
    b2y2 = box2[3]

    y_range = [max(b1y1, b2y1), min(b1y2, b2y2)]

    if current_point[0] > x_range[0] and current_point[0] < x_range[1]:
        if current_point[1] < y_range[0]:
            current_point = (current_point[0], y_range[0])
        else:
            current_point = (current_point[0], y_range[1])

    elif current_point[1] > y_range[0] and current_point[1] < y_range[1]:
        if current_point[0] < x_range[0]:
            current_point = (x_range[0], current_point[1])
        else:
            current_point = (x_range[1], current_point[1])

    else:
        dist_1 = euclidean_helper(current_point, (x_range[0], y_range[0]))
        dist_2 = euclidean_helper(current_point, (x_range[1], y_range[0]))
        dist_3 = euclidean_helper(current_point, (x_range[0], y_range[1]))
        dist_4 = euclidean_helper(current_point, (x_range[1], y_range[1]))

        min_dist = dist_1
        current_point = (x_range[0], y_range[0])

        if min_dist > dist_2:
            min_dist = dist_2
            current_point = (x_range[1], y_range[0])
        if min_dist > dist_3:
            min_dist = dist_3
            current_point = (x_range[0], y_range[1])
        if min_dist > dist_4:
            min_dist = dist_4
            current_point = (x_range[1], y_range[1])

    return current_point