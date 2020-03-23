def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
           + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
           + sum(fleet.num_ships for fleet in state.enemy_fleets())


def if_desirable_planet(state):
    growth_requirement = 20
    growth_check = 0
    dist_requirement = 20
    dist_check = 999999
    dist_temp = 0
    for planet in state.neutral_planets():
        if planet.growth_rate != 0:
            growth_check = (planet.num_ships / planet.growth_rate)
        else:
            growth_check = 0
        if growth_check < growth_requirement:
            for myplanets in state.my_planets():
                dist_temp = state.distance(myplanets.ID, planet.ID)
                if dist_temp < dist_check:
                    dist_check = dist_temp
            if dist_check < dist_requirement:
                return True
    return False


def low_count(state):
    for planet in state.my_planets():
        if planet.num_ships > 40:
            return True
    return False


def if_desirable_attack(state):
    growth_requirement = 100
    growth_check = 0
    dist_requirement = 13
    dist_check = 999999
    dist_temp = 0
    for planet in state.enemy_planets():
        if planet.growth_rate != 0:
            growth_check = (planet.num_ships / planet.growth_rate)
        else:
            growth_check = 0
        if growth_check < growth_requirement:
            for myplanets in state.my_planets():
                dist_temp = state.distance(myplanets.ID, planet.ID)
                if dist_temp < dist_check:
                    dist_check = dist_temp
            if dist_check < dist_requirement:
                return True
    return False


def enemy_attack(state):
    for enemy_fleet in state.enemy_fleets():
        planet = enemy_fleet.destination_planet
        for friendly_planet in state.my_planets():
            if planet == friendly_planet.ID:
                size_of_fleet = enemy_fleet.num_ships
                size_of_planet = friendly_planet.num_ships + (friendly_planet.growth_rate*enemy_fleet.turns_remaining)
                if size_of_fleet > size_of_planet:
                    return True
    return False
