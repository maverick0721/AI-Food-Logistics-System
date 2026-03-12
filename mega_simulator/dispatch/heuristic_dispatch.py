def distance(a, b):

    ax, ay = a.location
    bx, by = b.restaurant.location

    return (ax - bx) ** 2 + (ay - by) ** 2


def assign_driver(order, drivers):

    available = [d for d in drivers if d.available]

    if not available:
        return None

    best_driver = min(available, key=lambda d: distance(d, order))

    best_driver.assign_order(order)

    order.driver = best_driver

    return best_driver