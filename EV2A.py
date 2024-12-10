import datetime


class EV2A:

    @staticmethod
    def price(start):
        """
        :param start: Start time
        :return: cost/kWH for the next hour, From PGE website
        """
        p = EV2A.Peak(start)
        if p == 0:
            return .18
        if p == 1:
            return .39
        if p == 2:
            return .50

    @staticmethod
    def Peak(start):
        """
        :param start: Start time
        :return: 0 for Off-peak, 1 for partial-peak, 2 for peak
        """

        peak_start = datetime.datetime(hour=16, month=start.month, day=start.day, year=start.year)
        peak_end = datetime.datetime(hour=21, month=start.month, day=start.day, year=start.year)

        off_peak_start = datetime.datetime(hour=0, month=start.month, day=start.day, year=start.year)
        off_peak_end = datetime.datetime(hour=15, month=start.month, day=start.day, year=start.year)

        if peak_start <= start < peak_end:
            return 2
        elif off_peak_start <= start < off_peak_end:
            return 0
        else:
            return 1

    @staticmethod
    def isCheap(start):
        return EV2A.Peak(start) == 0
