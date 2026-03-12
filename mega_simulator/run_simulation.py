import random

from mega_simulator.entities.driver import Driver
from mega_simulator.entities.restaurant import Restaurant
from mega_simulator.entities.customer import Customer
from mega_simulator.entities.order import Order

from mega_simulator.core.simulation_engine import SimulationEngine
from mega_simulator.environment.city_graph import CityGraph

from mega_simulator.dispatch.heuristic_dispatch import assign_driver


def create_drivers(n):

    drivers = []

    for i in range(n):

        loc = (random.randint(0,100), random.randint(0,100))

        drivers.append(Driver(i, loc))

    return drivers


def create_restaurants(n):

    restaurants = []

    for i in range(n):

        loc = (random.randint(0,100), random.randint(0,100))

        restaurants.append(Restaurant(i, loc))

    return restaurants


def create_customers(n):

    customers = []

    for i in range(n):

        loc = (random.randint(0,100), random.randint(0,100))

        customers.append(Customer(i, loc))

    return customers


def main():

    city = CityGraph("Roorkee")

    drivers = create_drivers(200)

    restaurants = create_restaurants(100)

    customers = create_customers(500)

    engine = SimulationEngine(city, drivers, restaurants)

    orders = []

    for i in range(50):

        r = random.choice(restaurants)
        c = random.choice(customers)

        order = Order(i, r, c)

        assign_driver(order, drivers)

        orders.append(order)

    engine.run(100)

    print("Simulation finished")


if __name__ == "__main__":

    main()