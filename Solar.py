from scipy import stats


class Solar:
    """
    Simulates Solar panels, using efficiency * hours * production to get daily production and spreads this production
    out over a normal curve with mu 13 and sigma 2
    """

    def __init__(self, kW, efficiency=.75):
        self.day_production = efficiency * 4.9 * kW

    def production(self, start):
        """
        :param start: start time
        :return: kWh Solar production for 1 hour after start time
        """
        percent_prod = stats.norm.cdf(start.hour + 1, loc=13, scale=2) - stats.norm.cdf(start.hour, loc=13, scale=2)
        return self.day_production * percent_prod
