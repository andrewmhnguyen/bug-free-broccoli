#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect, math

logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    neutral_planet_check2 = Check(if_desirable_planet)
    spread_action = Action(spread_to_desirable_planet)
    spread_sequence.child_nodes = [neutral_planet_check, neutral_planet_check2, spread_action]

    defend_planet = Sequence(name='Defense Strategy')
    enemy_attack_check = Check(enemy_attack)
    defend_action = Action(defend_friendly_planet)
    defend_planet.child_nodes = [enemy_attack_check, defend_action]

    optimal_offense = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    desirable_planet_check = Check(if_desirable_attack)
    best_attack = Action(attack_desirable_planet)
    optimal_offense.child_nodes = [largest_fleet_check, desirable_planet_check, best_attack]

    offense = Sequence(name='Offensive Strategy 2')
    largest_fleet_check2 = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offense.child_nodes = [largest_fleet_check2, attack]

    reinforce = Sequence(name='Reinforce')
    reinforce_check = Check(low_count)
    reinforce_action = Action(reinforce_friendly_planet)
    reinforce.child_nodes = [reinforce_check, reinforce_action]

    spread2 = Sequence(name='Spread 2')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread2.child_nodes = [neutral_planet_check, spread_action]

    root.child_nodes = [spread_sequence, offense, optimal_offense]
    #spread_sequence,defend_planet, reinforce, optimal_offense, spread2, offense

    logging.info('\n' + root.tree_to_string())
    return root


# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)


if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
