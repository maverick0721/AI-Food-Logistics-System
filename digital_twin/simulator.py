from digital_twin.city_graph import CityGraph
from digital_twin.traffic_model import TrafficModel
from digital_twin.driver_agent import DriverAgent
from digital_twin.restaurant_queue import Restaurant
from digital_twin.order_generator import OrderGenerator


class DigitalTwinSimulator:

    def __init__(self):

        self.graph = CityGraph("Roorkee, India").build()

        self.traffic = TrafficModel()

        self.drivers = [

            DriverAgent(i, 0) for i in range(50)

        ]

        self.restaurant = Restaurant(1)

        self.generator = OrderGenerator()

    def step(self, hour):

        order = self.generator.generate()

        self.restaurant.add_order(order)

        order_ready, prep_time = self.restaurant.process()

        if order_ready:

            driver = self.drivers[0]

            driver.assign_order()

            speed = self.traffic.get_speed(hour)

            print("Driver delivering order at speed:", speed)