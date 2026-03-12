class Metrics:

    def __init__(self):

        self.delivery_times = []

    def record_delivery(self, time):

        self.delivery_times.append(time)

    def avg_delivery_time(self):

        if not self.delivery_times:
            return 0

        return sum(self.delivery_times) / len(self.delivery_times)