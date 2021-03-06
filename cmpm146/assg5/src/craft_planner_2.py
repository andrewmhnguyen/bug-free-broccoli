import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush
from math import inf

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        
        # items that are consumed with the rule -> check if there are enough 
        # looks at the consumes section in rule if it exist
        if 'Consumes' in rule:
            #loops through each item in that section
            for item, value in rule['Consumes'].items():
            # loops through each item in the list and checks the number in the state
                if state[item] < value:
                    return False
        
        #rule['Requires']
        # items that are required with the rule -> check if there is 1 
        # adds each item to a list 
        list_of_require = []
        # adds each item to a list 
        # looks at the required section in rules if it exist
        if 'Requires' in rule:
            #loops through each item in that section
            for item, value in rule['Requires'].items():
            # loops through each item in the list and checks the number in the state
                if state[item] == 0:
                    return False
        return True

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        
        # copies the state and moves it to a new one 
        next_state = State.copy(state)

        # items that are produced with the rule -> add the items to the state
        for item, value in rule['Produces'].items():
            next_state[item] += value
    
        # items that are consumed with the rule -> remove the items from the state
        if 'Consumes' in rule:
            for item, value in rule['Consumes'].items():
                next_state[item] -= value

        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        # loop through ever item in the list of required items in goal

        for item, value in goal.items():
            if state[item] < value:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state, action, prev_state, total_list):
    # Implement your heuristic here!
    tools = ['bench', 'wooden_pickaxe', 'wooden_axe', 'stone_axe', 'stone_pickaxe', 'iron_pickaxe', 'iron_axe', 'furnace']
    priority = 0
    cur_state = state.copy()

    for tool in tools:
        if state[tool] > 1:
            return inf
        elif tool in action:
            return 0

    for item in total_list:
        if cur_state[item] > total_list[item]:
            return inf

    if state['iron_pickaxe'] == 1:
        if 'stone_pickaxe' in action or 'wooden_pickaxe' in action:
            return inf
    elif state['stone_pickaxe'] == 1:
        if 'wooden_pickaxe' in action:
            return inf
        
    if state['iron_axe'] == 1:
        if 'stone_axe' in action or 'wooden_axe' in action:
            return inf
    elif state['stone_pickaxe'] == 1:
        if 'wooden_axe' in action:
            return inf
        
    for item in prev_state:
        cur_state[item] += prev_state[item]

    for item in total_list:
        priority += cur_state[item]

    return priority

def get_total_list(goal):
    things_needed = State({key: 0 for key in Crafting['Items']})
    tools = ['bench', 'wooden_pickaxe', 'wooden_axe', 'stone_axe', 'stone_pickaxe', 'iron_pickaxe', 'iron_axe', 'furnace']

    queue = []

    for item in goal:
        queue.append((item, goal[item]))

    while queue:
        item, amount = queue.pop()

        if item in tools:
            things_needed[item] = 1
        else:
            things_needed[item] += amount

        for action in Crafting['Recipes']:
            if item in Crafting['Recipes'][action]['Produces']:
                if 'Consumes' in Crafting['Recipes'][action]:
                    for consumable in Crafting['Recipes'][action]['Consumes']:
                        queue.append((consumable, Crafting['Recipes'][action]['Consumes'][consumable]))
                if 'Requires' in Crafting['Recipes'][action]:
                    for requireable in Crafting['Recipes'][action]['Requires']:
                        if things_needed[requireable] == 0:
                            queue.append((requireable, 1))
                
    return things_needed


def search(graph, state, is_goal, limit, heuristic):
    goal_list = get_total_list(Crafting['Goal'])
    start_time = time()
    queue = [(0, state)]
    cost = {}
    cost[state] = 0
    backpointers = {}
    backpointers[state] = None
    actions = {}
    actions[state] = None
    visited_states = set()
    visited_states.add(state)
    
    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while time() - start_time < limit:
        current_cost, current_state = heappop(queue)

        if is_goal(current_state):
            path = [(current_state, actions[current_state])]

            current_back_state = backpointers[current_state]
            while current_back_state is not None:
                path.insert(0,(current_back_state, actions[current_back_state]))
                current_back_state = backpointers[current_back_state]
            print('states visited: ' + str(len(visited_states)))
            print(time() - start_time, "seconds.")
            return path

        for adj_action, adj_state, adj_cost in graph(current_state):
            total_cost = current_cost + adj_cost + heuristic(adj_state, adj_action, current_state, goal_list)
            
            if (adj_state not in cost or total_cost < cost[adj_state]) and adj_state not in visited_states:
                cost[adj_state] =  total_cost
                backpointers[adj_state] = current_state
                actions[adj_state] = adj_action
                visited_states.add(adj_state)
                heappush(queue, (total_cost, adj_state))
            
    # Failed to find a path
    print(queue[0])
    print(actions[queue[0][1]])
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

    
    '''
    start_time = time()
    next_state = state
    path = []

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while time() - start_time < limit:
        goal_list = get_total_list(Crafting['Goal'])
        queue = [(0, state, None)]
        prev = {}
        cost = {}
        actions = {}
        prev[state] = None
        cost[state] = 0
        actions[state] = None

        while len(queue) != 0:
            print(time() - start_time)
            current_cost, current_state, current_action = heappop(queue)
            if is_goal(current_state) == True:
                path.append((current_state, current_action))
                current_back_node = prev[current_state]
                while current_back_node is not None:
                    path.append((current_back_node, actions[current_back_node]))
                    current_back_node = prev[current_back_node]
                print(time() - start_time, 'seconds.')
                break
            for node_action, node_state, node_cost in graph(current_state):
                new_cost = current_cost + node_cost + heuristic(node_state, node_action, current_state, goal_list)
                if node_state not in cost or node_cost < cost[node_state] and node_state not in prev:
                    cost[node_state] = new_cost
                    actions[node_state] = node_action
                    priority = new_cost + heuristic(node_state, node_action, current_state, goal_list)
                    heappush(queue, (priority, node_state, node_action))
                    prev[node_state] = current_state      
        return path
    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None
    '''
if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])
    
    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)
    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)