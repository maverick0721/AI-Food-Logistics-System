import random


class DriverAgent:

    def __init__(self, driver_id, location):

        self.driver_id = driver_id
        self.location = location
        self.available = True

    def assign_order(self):

        self.available = False

    def complete_order(self, new_location):

        self.location = new_location
        self.available = True