class SurgeModel:

    def surge_multiplier(self, orders, drivers):

        if drivers == 0:
            return 2.0

        ratio = orders / drivers

        if ratio > 2:
            return 1.8

        if ratio > 1:
            return 1.3

        return 1.0