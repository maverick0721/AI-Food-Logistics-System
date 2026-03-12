class Driver:

    def __init__(self, driver_id, location):

        self.id = driver_id
        self.location = location

        self.available = True
        self.current_order = None

    def assign_order(self, order):

        self.current_order = order
        self.available = False

    def complete_order(self):

        self.current_order = None
        self.available = True