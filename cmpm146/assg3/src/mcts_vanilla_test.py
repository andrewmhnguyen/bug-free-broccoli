
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 500

explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either '1' or '2'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    
    if len(node.child_nodes) != 0:
        max_node_value = 0
        max_node = None
        for child in node.child_nodes:
            new_node = node.child_nodes[child]
            if new_node.visits == 0:
                node_select = 0
            else:
                if identity == board.current_player(state):
                    node_select = (new_node.wins/new_node.visits) + explore_faction*(sqrt(log(node.visits)/new_node.visits))
                else:
                    node_select = (1 - (new_node.wins/new_node.visits)) + explore_faction*(sqrt(log(node.visits)/new_node.visits))
            if node_select > max_node_value:
                max_node = new_node
        
        return max_node
    else:
        leaf_node = node
        return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #new_node.parent = node                                    # Parent node to this node
    #new_node.parent_action = node.untried_actions.pop(0)      # The move that got us to this node - "None" for the root node.

    #board.next_state(state, new_node.parent_action)

    #new_node.child_nodes = {}                                 # Action -> MCTSNode dictionary of children
    #new_node.untried_actions = board.legal_actions(state)     # Yet unexplored actions

    #new_node.wins = 0                           
    #new_node.visits = 0   

    action = node.untried_actions.pop(0)
    state = board.next_state(state, action)
    new_node = MCTSNode(node,action,board.legal_actions(state))
    node.child_nodes[new_node.parent_action] = new_node

    return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while board.legal_actions(state) != []:
        random_action = choice(board.legal_actions(state))
        state = board.next_state(state, random_action)
    return state

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node!=None:
        node.visits = node.visits + 1
        if won == True:
            node.wins = node.wins + 1
        node = node.parent

def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    
    legal = False

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state
        # Start at root
        node = root_node
        # Do MCTS - This is all you!
        won = False
        
        
        while node.untried_actions == [] and node.child_nodes != {}:
            node.visits = node.visits + 1
            node = traverse_nodes(node, board, sampled_game, identity_of_bot)
            #moves the state of the game depending on where you traversed
            if node.parent_action != None:
                sampled_game = board.next_state(state, node.parent_action)

        if node.untried_actions != []:
            node = expand_leaf(node, board, sampled_game)
            node = traverse_nodes(node, board, sampled_game, identity_of_bot)
            #moves the state of the game
            sampled_game = board.next_state(state, node.parent_action)

        sampled_game = rollout(board, sampled_game)

        point = board.points_values(sampled_game)[identity_of_bot]

        if point == 1:
            won = True
        backpropagate(node, won)

        if board.is_ended(state) == True:
            break

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    actionValue = 0
    actionTake = None
    for action in root_node.child_nodes.keys():
        test_node = root_node.child_nodes[action]
        if test_node.visits == 0:
            value = 0
        else:
            value = test_node.wins/test_node.visits
        if value > actionValue:
            actionTake = action
            actionValue = value
    if(actionTake==None):
        return choice(board.legal_actions(state))
    return actionTake
