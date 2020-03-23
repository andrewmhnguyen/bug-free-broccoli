import json
import sys
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




def heuristic(state):
    # Implement your heuristic here!
    # a function that takes some state and returns an estimated cost

    estimated_cost = 0
    # calculating estimated cost for this state to goal

    # 'Items' contains weapons and raw materials, so have to seperate Item into a weapon list
    # because we only want to return inf if we already have a weapon. We want multiple 
    # raw materials. If we return inf if we already have raw materal then we can't make anything
    weapons = ["wooden_pickaxe", "stone_pickaxe", "iron_pickaxe", "wooden_axe", "stone_axe", "iron_axe", "bench", "furnace"]
    print("entered heuristic 137")

    def wood(state, need, tool):
        cost = 0
        #inventory = state['Item']
        #have = inventory['wood']
        have = state['wood']
        left = need - have
        if left < 0 :
            return cost
        for x in range(1,left):
            if tool == 'punch':
                cost = 4 + cost
            elif tool == 'stone_axe' or 'iron_axe':
                cost = 1 + cost
            elif tool == 'wooden_axe':
                cost = 2 + cost
            else:
                #print("wood error: need axe")
                cost = 18
                #cost = axe(state,1)
                #sys.exit() 
        return cost

    def planks(state, need, tool):
        cost = 0
        #inventory = state['Item']
        #have = inventory['plank'] 
        have = state['plank']
        while not have >= need:
            # 1 wood = 4 planks
            cost = wood(state, 1, tool) + cost + 1
            have = 4
        return cost

    def bench(state, need, tool):
        cost = 0
        #inventory = state['Item']
        plank = state['plank'] 
        while plank < 4:
            cost = planks(state, 4, tool) + cost + 1
            plank = plank+4
        return cost
    
    def stick(state, need, tool):
        cost = 0
        #inventory = state['Item']
        have = state['stick']
        while not have >= need:
            # 2 planks = 4 sticks
            cost = planks(state, 2, tool) + cost + 1
            have = 4
        return cost

    def cobble(state, need, tool):
        cost = 0
        #inventory = state['Item']
        have = state['stick']
        left = need - have
        if left < 0 :
            return cost
        for x in range(1,left):
            if tool == 'iron_pickaxe':
                cost = 1 + cost
            elif tool == 'stone_pickaxe':
                cost = 2 + cost
            elif tool == 'wooden_pickaxe':
                cost = 4 + cost
            else:
                #print("cobble error: need pickaxe")
                #cost = pickaxe(state,1)
                cost = 18
        return cost

    def furnace(state, need, tool):
        cost = 0
        #inventory = state['Item']
        cobbles = state['cobble']
        while cobbles < 8:
            cost = cobble(state,8, tool) + cost + 1
            cobbles = cobbles + 8
        return cost

    def ore(state, need, tool):
        cost = 0
        #inventory = state['Item']
        have = state['ore']
        left = need - have
        if left < 0 :
            return cost
        for x in range(1,left):
            if tool == 'iron_pickaxe':
                cost = 2 + cost
            elif tool == 'stone_pickaxe':
                cost = 4 + cost
            else:
                #print("ore error: need pickaxe")
                #cost = pickaxe(state,1)
                cost = 18
                #sys.exit() 
        return cost


    def ingot(state, need, tool):
        cost = 0
        #inventory = state['Item']
        have = state['ingot']
        left = need - have
        if left < 0 :
            return cost
        if state['furnace'] >= 1:
            for x in range(1,left):
                cost = ore(state, 1, tool) + coal(state,1,tool) + cost + 5
        else:
            for x in range(1,left):
                cost = ore(state, 1, tool) + coal(state,1,tool) + cost + 5 + furnace(state, 1, tool) 
        return cost

    def coal(state, need, tool):
        cost = 0
        #inventory = state['Item']
        have = state['coal']
        left = need - have
        if left < 0 :
            return cost
        for x in range(1,left):
            if tool == 'iron_pickaxe':
                cost = 1 + cost
            elif tool == 'stone_pickaxe':
                cost = 2 + cost
            elif tool == 'wooden_pickaxe':
                cost = 4 + cost
            else:
                #print("coal error: need pickaxe")
                #cost = pickaxe(state,1)
                cost = 18

                #sys.exit() 
        return cost
            
    def rail (state, need, tool):
        cost = 0
        #inventory = state['Item']
        rail = state['rail']
        while rail < need :
            cost = ingot(state,6,tool) + stick(state,1,tool)+ cost + 1
            rail = rail + 16
        if state['bench'] >= 1:
            return cost
        else:
            return cost + bench(state,1,tool)


    def cart (state, need, tool):
        cost = 0
        #inventory = state['Item']
        cart = state['cart']
        while cart < need:
            cost = ingot(state,5,tool)+ 1 + cost

        if state['bench'] >= 1:
            return cost
        else:
            return cost+bench(state,1,tool)

    def pickaxe(state, need):
        cost = 0
        cost = planks(state,3,'punch')+stick(state,2,'punch')+ cost + 1 + bench(state,1,'punch')
        return cost

    def axe(state, need):
        cost = 0
        cost = planks(state,3,tool)+stick(state,2,tool)+ cost + 1 + bench(state,1,tool)
        return cost


    # if a tool already exists -> don't craft it again - infinity
    # make it return infinity so it will never be selected because we want 
    # to go to the state with the lowest estimated cost
    # see if there is an Item section in state
        
    if len(weapons) >=1:
        print('point 1')
        # loop through all weapons in Item
        for product in weapons:
            print("product:")
            print(product)
            # for pickaxe
            # if we have a pickaxe already then estimated_cost = inf bc we dont need another one
            if product == "iron_pickaxe":
                if state['stone_pickaxe'] or state['wooden_pickaxe'] or state['iron_pickaxe']>=1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    #1 bench, 3 ingot, 2 stick
                    if state['iron_axe'] >= 1:
                        tool = 'iron_axe'
                    elif state['stone_axe'] >= 1:
                        tool = 'stone_axe'
                    elif state['wooden_axe'] >= 1:
                        tool = 'wooden_axe'
                    else:
                        tool = 'punch'

                    if state['bench'] >= 1:
                        estimated_cost = ingot(state,3,tool)+stick(state,2,tool)+ estimated_cost+1
                        return estimated_cost
                    else:
                        estimated_cost = ingot(state,3,tool)+stick(state,2,tool)+ estimated_cost+1 + bench(state,1,tool)
                        return estimated_cost

            if product == "stone_pickaxe":
                if state['stone_pickaxe'] or state['wooden_pickaxe'] or state['iron_pickaxe']>=1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    # 1 bench, 3 cobble, 2 stick
                    if state['iron_axe'] >= 1:
                        tool = 'iron_axe'
                    if state['stone_axe'] >= 1:
                        tool = 'stone_axe'
                    if state['wooden_axe'] >= 1:
                        tool = 'wooden_axe'
                    if state['bench'] >= 1:

                        estimated_cost = cobble(state,3,tool)+stick(state,2,tool)+1
                        return estimated_cost
                    else:
                        estimated_cost = cobble(state,3,tool)+stick(state,2,tool)+ 1 + bench(state,1,tool)
                        return estimated_cost

                    #estimated_cost = 31
            if product == "wooden_pickaxe":
                if state['stone_pickaxe'] or state['wooden_pickaxe'] or state['iron_pickaxe']>=1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    # 1 bench, 3 planks, 2 stick
                    if state['iron_axe'] >= 1:
                        tool = 'iron_axe'
                    elif state['stone_axe'] >= 1:
                        tool = 'stone_axe'
                    elif state['wooden_axe'] >= 1:
                        tool = 'wooden_axe'
                    else:
                        tool = 'punch'

                    if state['bench'] >= 1:
                        estimated_cost = planks(state,3,tool)+stick(state,2,tool)+ 1
                        return estimated_cost
                    else:
                        estimated_cost = planks(state,3,tool)+stick(state,2,tool)+ 1 + bench(state,1,tool)
                        return estimated_cost
                    #estimated_cost = 18

            # for axe
            # if we have an axe already then, we dont need other axes 
            if product == "iron_axe":
                if state['stone_axe'] or state['wooden_axe'] or state['iron_axe']>=1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    # 1 bench, 3 ingot, 2 stick
                    if state['iron_pickaxe'] >= 1:
                        tool = 'iron_pickaxe'
                    if state['stone_pickaxe'] >= 1:
                        tool = 'stone_pickaxe'
                    if state['wooden_pickaxe'] >= 1:
                        tool = 'wooden_pickaxe'
                    if state['bench'] >= 1:
                        estimated_cost = ingot(state,3,tool)+stick(state,2,tool)+ 1
                        return estimated_cost
                    else:
                        estimated_cost = ingot(state,3,tool)+stick(state,2,tool)+1 + bench(state,1,tool)
                        return estimated_cost

            if product == "stone_axe":
                if state['stone_axe'] or state['wooden_axe'] or state['iron_axe']>=1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    # 1 bench, 3 cobble, 2 stick
                    if state['iron_pickaxe'] >= 1:
                        tool = 'iron_pickaxe'
                    if state['stone_pickaxe'] >= 1:
                        tool = 'stone_pickaxe'
                    if state['wooden_pickaxe'] >= 1:
                        tool = 'wooden_pickaxe'
                    if state['bench'] >= 1:
                        estimated_cost = cobble(state,3,tool)+stick(state,2,tool)+ 1
                        return estimated_cost
                    else:
                        estimated_cost = cobble(state,3,tool)+stick(state,2,tool)+ 1 + bench(state,1,tool)
                        return estimated_cost
                    #estimated_cost = 0

            if product == "wooden_axe":
                if state['stone_axe'] or state['wooden_axe'] or state['iron_axe']>=1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    # 1 bench, 3 planks, 2 stick
                    if state['iron_pickaxe'] >= 1:
                        tool = 'iron_pickaxe'
                    if state['stone_pickaxe'] >= 1:
                        tool = 'stone_pickaxe'
                    if state['wooden_pickaxe'] >= 1:
                        tool = 'wooden_pickaxe'
                    if state['bench'] >= 1:
                        estimated_cost = planks(state,3,tool)+stick(state,2,tool)+ 1
                        return estimated_cost
                    else:
                        estimated_cost = planks(state,3,tool)+stick(state,2,tool)+ 1 + bench(state,1,tool)
                        return estimated_cost
                    #estimated_cost = 0

            # for bench
            if product == "bench":
                if state['iron_axe'] >= 1:
                    tool = 'iron_axe'
                if state['stone_axe'] >= 1:
                    tool = 'stone_axe'
                if state['wooden_axe'] >= 1:
                    tool = 'wooden_axe'
                if state['iron_pickaxe'] >= 1:
                    tool = 'iron_pickaxe'
                if state['stone_pickaxe'] >= 1:
                    tool = 'stone_pickaxe'
                if state['wooden_pickaxe'] >= 1:
                    tool = 'wooden_pickaxe'
                if state['bench'] >= 1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    estimated_cost = bench(state,1,tool)
                    return estimated_cost

            #for furnace
            if product == "furnace":
                if state['iron_axe'] >= 1:
                    tool = 'iron_axe'
                elif state['stone_axe'] >= 1:
                    tool = 'stone_axe'
                elif state['wooden_axe'] >= 1:
                    tool = 'wooden_axe'
                elif state['iron_pickaxe'] >= 1:
                    tool = 'iron_pickaxe'
                elif state['stone_pickaxe'] >= 1:
                    tool = 'stone_pickaxe'
                elif state['wooden_pickaxe'] >= 1:
                    tool = 'wooden_pickaxe'
                else:
                    tool = 'punch'
                if state['bench'] >= 1:
                    estimated_cost = inf
                    return estimated_cost
                else:
                    estimated_cost = furnace(state, 1, tool)
                    return estimated_cost

            
    return estimated_cost


def search(graph, state, is_goal, limit, heuristic):
    start_time = time()
    queue = [(0, state, None)]
    cost = {}
    cost[state] = 0
    prev = {}
    prev[state] = None
    actions = {}
    actions[state] = None
    visited = []
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
            print(time() - start_time, "seconds.")
            return path

        for node_action, node_state, node_cost in graph(current_state):
            new_cost = current_cost + node_cost 
            if (node_state not in cost or new_cost < cost[node_state]) and node_state not in visited:
                cost[node_state] =  new_cost
                actions[node_state] = node_action
                visited.append(node_state)
                priority = new_cost + heuristic(node_state)
                print(heuristic(node_state))
                heappush(queue, (priority, node_state, node_action))
                prev[node_state] = current_state
            
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
