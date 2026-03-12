from llm_agent.tools import search_restaurant


class FoodAgent:

    def respond(self, query):

        query = query.lower()

        results = search_restaurant(query)

        if not results:

            return "Sorry, no matching food found."

        response = "Available options:\n"

        for r in results:

            response += f"{r[1]} from {r[0]}\n"

        return response


if __name__ == "__main__":

    agent = FoodAgent()

    print(agent.respond("biryani"))