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
                if state[item] < value:
                    return False
        
        #rule['Requires']
        # items that are required with the rule -> check if there is 1 
        # looks at the required section in rules if it exist
        if 'Requires' in rule:
            #loops through each item in that section
            for item, value in rule['Requires'].items():
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


def heuristic(state, action):
    # Implement your heuristic here!

    # if there is a tool that already exists, don't make another one 
    required_items = ['bench', 'wooden_pickaxe', 'wooden_axe', 'stone_axe', 'stone_pickaxe', 'iron_pickaxe', 'iron_axe', 'furnace']
    raw_items = ['coal', 'cobble', 'ore', 'plank', 'stick', 'wood', 'ingot']
    cost = 0

    for item in required_items:
        if state[item] > 1:
            return inf
    for item in raw_items:
        if state[item] == 'ore':
            if state[item] > 3:
                return inf
        if state[item] > 8:
            return inf

    return cost

def search(graph, state, is_goal, limit, heuristic):
    start_time = time()
    queue = [(0, state, None)]

    cost = {}
    prev = {}
    actions = {}
    visited = []

    cost[state] = 0
    prev[state] = None
    actions[state] = None
    visited.append(state)

    path = []
    
    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while time() - start_time < limit:
        
        current_cost, current_state, current_action = heappop(queue)

        if is_goal(current_state) == True:
            path.append((current_state, current_action))
            current_back_node = prev[current_state]
            while current_back_node is not None:
                path.insert(0,(current_back_node, actions[current_back_node]))
                current_back_node = prev[current_back_node]
            break

        for node_action, node_state, node_cost in graph(current_state):
            new_cost = current_cost + node_cost 
            if (node_state not in cost or new_cost < cost[node_state]) and node_state not in visited:
                cost[node_state] =  new_cost
                actions[node_state] = node_action
                visited.append(node_state)
                priority = new_cost + heuristic(node_state, node_action)
                heappush(queue, (priority, node_state, node_action))
                prev[node_state] = current_state
    
    print(time() - start_time, "seconds.")
    print (len(visited))
    return path
            
    # Failed to find a path
    print(queue[0])
    print(actions[queue[0][1]])
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

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
        total_cost = 0
        for state, action in resulting_plan:

            if action:
                total_cost += Crafting['Recipes'][action]['Time']

            print('\t',state)
            print(action)

        print('[cost=' + str(total_cost) + ', len=' + str(len(resulting_plan)-1) + ']')
