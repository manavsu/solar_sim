from Solar import *
from Battery import *


class Grid:

    def __init__(self, usage_data, plan, solar=Solar(0), battery=Battery(0), multiplier=1):
        """
        :param usage_data: Data class
        :param plan: PG&E Plan used
        :param solar: Solar object
        :param battery: Battery Object
        :param multiplier: Easily scale data usage
        """
        self.plan = plan
        self.data = usage_data.data
        self.multiplier = multiplier

        self.solar = solar
        self.battery = battery

        self.usage = None
        self.time = None

        self.cost = None
        self.production = None

    def Cost(self):
        """
        Calculate the cost for this plan without solar
        :return Array with cost for every hour
        """
        self.cost = []
        self.time = []
        self.production = []
        self.usage = []

        for data in self.data:
            start = data['START']
            usage = self.getUsage(data)
            prod = self.solar.production(start)

            self.time.append(start)
            self.usage.append(usage)
            self.production.append(prod)

            net_usage = self.batteryManager(usage, prod, start)

            self.cost.append(round(self.plan.price(start) * net_usage, 2))

        return self.cost

    def batteryManager(self, usage, prod, start):
        """
        Handles logic for battery use.
        :return: net usage after battery use
        """
        if self.battery.capacity == 0:
            return usage - prod
        else:
            if self.solar.day_production == 0:
                if self.plan.isCheap(start):
                    stored = self.battery.push(min(self.battery.availability(), self.battery.power))
                    return usage - prod + stored
                else:
                    if usage - prod > 0:
                        pulled = self.battery.pull(min(self.battery.stored(), usage - prod, self.battery.power))
                        return usage - prod - pulled
                    else:
                        return usage - prod
            else:
                if self.plan.isCheap(start):
                    pushed = self.battery.push(min(self.battery.availability(), self.battery.power, prod))
                    return usage - prod + pushed
                else:
                    pulled = self.battery.pull(min(self.battery.stored(), self.battery.power, usage))
                    return usage - prod - pulled

    def getUsage(self, data):
        return data["USAGE"] * self.multiplier

    def trueUp(self):
        """
        End of Year true, if you have a negative and balance and you created more energy than you used you get a
        credit.
        :return true cost of solar for the year.
        """
        if sum(self.cost) < 0:
            diff = sum(self.production) - sum(self.usage)
            if diff > 0:
                return -diff * .04
            else:
                return 0
        else:
            return sum(self.cost)
