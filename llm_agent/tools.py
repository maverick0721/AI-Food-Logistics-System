from llm_agent.menu_database import restaurants


def search_restaurant(food):

    results = []

    for name, menu in restaurants.items():

        for item in menu:

            if food in item:

                results.append((name, item))

    return results