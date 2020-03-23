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


    start_box = s_and_d.pop(0)
    if len(s_and_d) == 0:
        print("No path!")
        raise SystemExit

    destination = s_and_d.pop(0)

    detail_points = {}

    detail_points[start_box] = source_point
    current_point = source_point

    # The priority queue
    queue = [(0, start_box, 'destination')]
    queue.append((0, destination, 'start_box'))

    # The dictionary that will be returned with the costs
    forward_distances = {}
    backward_distances = {}
    forward_distances[start_box] = 0
    backward_distances[destination] = 0

    # The dictionary that will store the backpointers
    forward_prev = {}
    backward_prev = {}
    forward_prev[start_box] = None
    backward_prev[destination] = None

    pathForward = []
    pathBackward = []

    while len(queue) != 0:
        current_dist, current_box, current_goal = heappop(queue)

        # Check if current node is the destination
        # Checks which direction you're moving in and which backwards to check if it's reached it
        if current_goal == 'destination' and current_box in backward_prev:
            # List containing all cells from initial_position to destination
            pathForward.append(current_box)
            
            # Go backwards from destination until the source using backpointers
            # and add all the nodes in the shortest path into a list
            current_back_node = forward_prev[current_box]
            while current_back_node is not None:
                pathForward.append(current_back_node)
                current_back_node = forward_prev[current_back_node]
            current_back_node = backward_prev[current_box]
            while current_back_node is not None:
                pathBackward.append(current_back_node)
                current_back_node = backward_prev[current_back_node]
            break
        if current_goal == 'start_box' and current_box in forward_prev:
            # List containing all cells from initial_position to destination
            pathBackward.append(current_box)
            
            # Go backwards from destination until the source using backpointers
            # and add all the nodes in the shortest path into a list
            current_back_node = backward_prev[current_box]
            while current_back_node is not None:
                pathBackward.append(current_back_node)
                current_back_node = backward_prev[current_back_node]
            current_back_node = forward_prev[current_box]
            while current_back_node is not None:
                pathForward.append(current_back_node)
                current_back_node = forward_prev[current_back_node]
            break

        # Calculate cost from current box to all the adjacent ones
        for box in mesh['adj'][current_box]:
            point_check = helper_box(detail_points[current_box], current_box, box)
            if current_goal == 'destination':
                pathcost = forward_distances[current_box] + euclidean_helper(detail_points[current_box], destination_point) + euclidean_helper(detail_points[current_box], point_check)
                # If the cost is new
                if box not in forward_distances or pathcost < forward_distances[box]:
                    forward_distances[box] = forward_distances[current_box] + euclidean_helper(detail_points[current_box], point_check)
                    forward_prev[box] = current_box
                    detail_points[box] = point_check
                    heappush(queue, (pathcost, box, 'destination'))
            else:
                pathcost = forward_distances[current_box] + euclidean_helper(detail_points[current_box], source_point) + euclidean_helper(detail_points[current_box], point_check)
                # If the cost is new
                if box not in backward_distances or pathcost < backward_distances[box]:
                    backward_distances[box] = backward_distances[current_box] + euclidean_helper(detail_points[current_box], point_check)
                    backward_prev[box] = current_box
                    detail_points[box] = point_check
                    heappush(queue, (pathcost, box, 'start_box'))

    newPath = []
    newBoxes = []

    for i in range(len(pathForward)-1):
        newPath.append((detail_points[pathForward[i]], detail_points[pathForward[i+1]]))
        newBoxes.append(pathForward[i])

    for i in range(len(pathBackward)-1):
        newPath.append((detail_points[pathBackward[i]], detail_points[pathBackward[i+1]]))
        newBoxes.append(pathBackward[i])

    top1 = len(pathBackward) - 1
    top2 = len(pathForward) - 1

    newPath.append((detail_points[path[top1]], detail_points[path[top2]]))
    
    #newPath.append((detail_points[path[0]], destination_point))
    #newBoxes.append(start_box)

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
