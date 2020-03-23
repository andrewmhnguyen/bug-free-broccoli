from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """

    """Create queue and return condition"""
    queue = []

    infTaken = False

    """Track shortest distance from cells to source and already visited cells"""
    dist = {}  # cells and distance from source
    prev = {}  # visited
    dist[initial_position] = 0
    prev[initial_position] = None

    """Push first coordinate into queue"""
    source = (0, initial_position)
    heappush(queue, source)
    runningCost = 0

    """Search algorithm"""
    while len(queue) != 0:
        """Get cell at front of the queue and get its neighbors"""
        curr = heappop(queue)

        '''
        Checks if the current value is at infinity - means that all viable options have been taken and
        that no paths can be found
        '''
        if curr[0] == inf:
            infTaken = True
            break

        curr_cell = curr[1]
        neighbors = navigation_edges(graph, curr_cell)


        """Exit if the cell is the destination"""
        if curr_cell == destination:
            break

        """Calculate cost to neighbors and add them to the queue"""
        for neigh in neighbors:
            cost = dist[curr_cell] + neigh[1]
            if neigh[0] not in prev or cost < dist[neigh[0]]:
                dist[neigh[0]] = cost
                cell_pair = (cost, neigh[0])
                heappush(queue, cell_pair)
                prev[neigh[0]] = curr_cell

    """Put optimal path in list and return it"""

    if infTaken is True:
        return None

    path = []
    prev_node = destination
    while prev_node is not initial_position:
        if prev_node in dist:
            path.insert(0, prev_node)
            prev_node = prev[prev_node]
        else:
            break
    path.insert(0, initial_position)
    
    return path

def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    """Initalize dictionary for cells and distance cost"""
    all_cell_cost = {}
    all_cell_cost[initial_position] = 0

    """Set cost for walls"""
    for cells in graph.get('walls'):
        all_cell_cost[cells] = inf

    """Set cost for spaces"""
    for cells in graph.get('spaces'):
        cost = 0
        path = dijkstras_shortest_path(initial_position, cells, graph, adj)
        if path is None:
            all_cell_cost[cells] = inf
        else:
            for i in range(len(path)-1):
                cost += + calc_cost(path[i], path[i+1], graph.get('spaces')[path[i]], graph.get('spaces')[path[i+1]])
        if cells is not initial_position and cost == 0:
            all_cell_cost[cells] = inf
        else:
            all_cell_cost[cells] = cost

    """Set cost for waypoints"""
    for waypoint in graph.get('waypoints'):
        cells = graph.get('waypoints')[waypoint]
        cost = 0
        path = dijkstras_shortest_path(initial_position, cells, graph, adj)
        if path is None:
            all_cell_cost[cells] = inf
        else:
            for i in range(len(path) - 1):
                cost = cost + calc_cost(path[i], path[i + 1], graph.get('spaces')[path[i]], graph.get('spaces')[path[i + 1]])
        if cells is not initial_position and cost == 0:
            all_cell_cost[cells] = inf
        else:
            all_cell_cost[cells] = cost

    return all_cell_cost

def calc_cost(cell1, cell2, weight1, weight2):
    """See if its diagonal or not and calculate distance"""
    direction = (abs(cell1[0] - cell2[0]), abs(cell1[1] - cell2[1]))
    if direction == (1, 1):
        cost = (.5 * sqrt(2) * weight1) + (.5 * sqrt(2) * weight2)
    else:
        cost = (.5 * weight1) + (.5 * weight2)
    return cost

def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """

    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    adjCells = []
    adjCellsWeight = []

    curWeight = level.get('spaces').get(cell)
    for dir in dirs:
        neighbor = (cell[0] + dir[0], cell[1] + dir[1])
        weight = level.get('spaces').get(neighbor)
        if weight != None and curWeight != None:
            if dir[0] != 0 and dir[1] != 0:
                distCost = (.5 * sqrt(2) * weight) + (.5 * sqrt(2) * curWeight)
            else:
                distCost = (.5 * weight) + (.5 * curWeight)
        else:
            distCost = inf
        adjCellsWeight.append((neighbor, distCost))
    return adjCellsWeight

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges(level, src))
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)


    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'hanette.txt', 'a', 'b'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'hanette.csv')
