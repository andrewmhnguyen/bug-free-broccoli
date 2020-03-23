from math import sqrt

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
        if x[0] < source_point[0] and x[2] < source_point[1] and x[1] > source_point[0] and x[3] > source_point[1]:
            s_and_d.insert(0, x)
        if x[0] < destination_point[0] and x[2] < destination_point[1] and x[1] > destination_point[0] and x[3] > destination_point[1]:
            s_and_d.append(x)

    s_and_d_copy = s_and_d.copy()

    if len(s_and_d) == 1:
        print("No Path!")
        raise SystemExit

    to_visit_queue = []
    start_box = s_and_d.pop(0)
    to_visit_queue.append(start_box)
    prev = {}
    prev[source_point] = None

    while to_visit_queue:
        current_box = to_visit_queue.pop(0)
        for x in mesh['adj'][current_box]:
            if x not in prev:
                to_visit_queue.append(x)
                prev[x] = current_box

        if current_box in s_and_d:
            break

    destination = s_and_d.pop(0)
    bfs_path = []

    if destination in prev:
        current_key = destination   #set the end of the path
        while current_key is not start_box:  #iterate over the path
            bfs_path.append(current_key)    #for each new node of the path save it to the list
            current_key = prev[current_key] #change current key to previous one
        bfs_path.append(start_box)   #append the initial position
        bfs_path.reverse()  #reverse the order of the path so that it displays start to finish
    else:
        print("No path!")

    detail_points = {}

    detail_points[start_box] = source_point
    current_point = source_point

    i = 0

    path_line_segments = []
    secondtoLastPoint = None

    while i < len(bfs_path)-1:
        
        if current_point is destination_point:
            break

        box1 = bfs_path[i]
        box2 = bfs_path[i+1]

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

        detail_points[box2] = current_point
        path_line_segments.append((detail_points[box1], detail_points[box2]))
        secondtoLastPoint = detail_points[box2]
        i = i+1

    path_line_segments.append((secondtoLastPoint, destination_point))

    path = path_line_segments
    boxes = bfs_path

    return path, boxes



def euclidean_helper (current, test):
    first_in = (current[0]-test[0])**2
    second_in = (current[1]-test[1])**2

    sum = sqrt(first_in+second_in)

    return sum

