class Scheduler:

    def __init__(self):

        self.current_time = 0

    def tick(self):

        self.current_time += 1

    def now(self):

        return self.current_time