import heapq


class EventQueue:

    def __init__(self):

        self.queue = []

    def push(self, time, event):

        heapq.heappush(self.queue, (time, event))

    def pop(self):

        return heapq.heappop(self.queue)

    def empty(self):

        return len(self.queue) == 0