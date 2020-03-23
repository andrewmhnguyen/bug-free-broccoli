import math
import sys

sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        if strongest_planet.num_ships / 2 < 25:
            return False
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    dist_check = 9999
    dist = 0
    # first_planet = state.my_planets()[0]
    # for planets in state.neutral_planets():
    #     dist = state.distance(planets.ID, first_planet.ID)
    #    if dist < dist_check:
    #        dist_check = dist
    #        weakest_planet = planets
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        if strongest_planet.num_ships>weakest_planet.num_ships:
            issue_order(state, strongest_planet.ID, weakest_planet.ID,weakest_planet.num_ships)
        else:
            issue_order(state, strongest_planet.ID, weakest_planet.ID,strongest_planet.num_ships-20)
        return



def reinforce_friendly_planet(state):
    low_planet = []

    for planet in state.my_planets():
        if planet.num_ships > 40:
            low_planet.append(planet)

    for receive in low_planet:
        for donator in state.my_planets():
            if donator.num_ships < 20:
                issue_order(state, receive.ID, donator.ID, 10)
    return


def spread_to_desirable_planet(state):
    growth_requirement = 20
    growth_check = 0
    dist_requirement = 20
    dist_check = 999999
    dist_temp = 0
    count_ships = 0
    required_ships = 0
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    if strongest_planet.num_ships / 2 < 25:
        return False
    for planet in state.neutral_planets():
        if planet.growth_rate != 0:
            growth_check = (planet.num_ships / planet.growth_rate)
        else:
            growth_check = 0
        if growth_check < growth_requirement:
            dist_planet = planet
            for myplanets in state.my_planets():
                if myplanets.num_ships - planet.num_ships >= 30:
                    dist_temp = state.distance(myplanets.ID, planet.ID)
                    if dist_temp < dist_check:
                        dist_check = dist_temp
                        source_planet = myplanets
            if dist_check < dist_requirement:
                required_ships = dist_planet.num_ships + 30
                count_ships = source_planet.num_ships - 30
                issue_order(state, source_planet.ID, dist_planet.ID, source_planet.num_ships - 30)
                required_ships = required_ships - count_ships
                if required_ships > 0:
                    count_planets = 0
                    for countplanets in state.my_planets():
                        count_planets = count_planets + 1
                    count = math.ceil(count_planets / required_ships)
                    for planets in state.my_planets():
                        issue_order(state, planets.ID, dist_planet.ID, count)
                    return
                return
    return


def defend_friendly_planet(state):

    fleets_attacking = []
    friend_planet = []

    for friend in state.my_fleets():
        friend_planet.append(friend.destination_planet)

    for enemy_fleet in state.enemy_fleets():
        planet = enemy_fleet.destination_planet
        for friendly_planet in state.my_planets():
            if planet == friendly_planet.ID:
                size_of_fleet = enemy_fleet.num_ships
                size_of_planet = friendly_planet.num_ships + (friendly_planet.growth_rate*enemy_fleet.turns_remaining)
                if size_of_fleet > size_of_planet:
                    if friendly_planet.ID not in friend_planet:
                        fleets_attacking.append(enemy_fleet)

    for fleet in fleets_attacking:
        number_of_ships = fleet.num_ships
        ships_to_send = number_of_ships / (len(state.my_planets()))
        for planet in state.my_planets():
            if planet.ID != fleet.destination_planet:
                if planet.num_ships > (ships_to_send + 10):
                    number_of_ships = number_of_ships - ships_to_send
                    issue_order(state, planet.ID, fleet.destination_planet, ships_to_send)
    return


def attack_desirable_planet(state):
    growth_requirement = 100
    growth_check = 0
    dist_requirement = 13
    dist_check = 999999
    dist_temp = 0
    count_ships = 0
    required_ships = 0
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    if strongest_planet.num_ships / 2 < 25:
        return False
    for planet in state.enemy_planets():
        if planet.growth_rate != 0:
            growth_check = (planet.num_ships / planet.growth_rate)
        if growth_check < growth_requirement:
            dist_planet = planet
            for myplanets in state.my_planets():
                if myplanets.num_ships - planet.num_ships >= 30:
                    dist_temp = state.distance(myplanets.ID, planet.ID)
                    if dist_temp < dist_check:
                        dist_check = dist_temp
                        source_planet = myplanets
            if dist_check < dist_requirement:
                required_ships = dist_planet.num_ships + 10 + dist_planet.growth_rate*state.distance(source_planet.ID, dist_planet.ID)  
                count_ships = source_planet.num_ships - 30
                issue_order(state, source_planet.ID, dist_planet.ID, source_planet.num_ships - 30)
                required_ships = required_ships - count_ships + dist_planet.growth_rate
                if required_ships > 0:
                    count_planets = 0
                    for countplanets in state.my_planets():
                        count_planets = count_planets + 1
                    count = math.ceil(count_planets / required_ships)
                    for planets in state.my_planets():
                        issue_order(state, planets.ID, dist_planet.ID, count)
                    return
    return
