from mega_simulator.core.event_queue import EventQueue
from mega_simulator.core.scheduler import Scheduler


class SimulationEngine:

    def __init__(self, city, drivers, restaurants):

        self.city = city
        self.drivers = drivers
        self.restaurants = restaurants

        self.scheduler = Scheduler()
        self.events = EventQueue()

    def step(self):

        self.scheduler.tick()

        if not self.events.empty():

            time, event = self.events.pop()

            event()

    def run(self, steps):

        for _ in range(steps):

            self.step()