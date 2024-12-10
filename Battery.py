class Battery:
    """
    Simulate a battery object
    """

    def __init__(self, capacity, efficiency=.9, power=5, quantity=1):
        self.capacity = capacity * quantity
        self.efficiency = efficiency
        self.power = power * quantity
        self.charge = 0
        self.loss = 0

    def push(self, kwh):
        """
        Push electricity to batteries
        :param kwh: amount to push
        :return: amount pushed
        """
        assert (self.efficiency * kwh <= self.availability())
        self.charge += kwh * self.efficiency / self.capacity
        self.loss += (1 - self.efficiency) * kwh
        return kwh

    def availability(self):
        """
        :return: Storage capacity available
        """
        assert (self.charge <= 1)
        return self.capacity - self.charge * self.capacity

    def stored(self):
        """
        :return: Kwh stored in battery
        """
        assert (self.charge <= 1)
        return self.capacity * self.charge

    def pull(self, kwh):
        """

        :param kwh:
        :return:
        """
        assert (kwh <= self.charge * self.capacity)
        assert (kwh <= self.power)
        self.charge -= kwh / self.capacity
        return kwh
