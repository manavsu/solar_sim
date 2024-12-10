import datetime


class ETOUD:

    @staticmethod
    def price(start):
        """
        :param start: Start time
        :return: cost/kWH for the next hour, From PGE website
        """
        if ETOUD.isSummer(start):
            if ETOUD.isPeak(start):
                return .38
            else:
                return .28
        else:
            if ETOUD.isPeak(start):
                return .30
            else:
                return .29

    @staticmethod
    def isPeak(start):
        """
        :param start: Start time
        :return: True if start is during peak hours, False off-peak
        """

        peak_start = datetime.datetime(hour=17, month=start.month, day=start.day, year=start.year)
        peak_end = datetime.datetime(hour=20, month=start.month, day=start.day, year=start.year)

        if peak_start <= start < peak_end:
            return True
        else:
            return False

    @staticmethod
    def isSummer(start):
        """
        :param start: Start time
        :return: True if this is the summer season, False if winter
        """
        summer_start = datetime.datetime(month=6, day=1, year=start.year)
        winter_start = datetime.datetime(month=8, day=1, year=start.year)

        if summer_start <= start < winter_start:
            return True
        else:
            return False

    @staticmethod
    def isCheap(start):
        return not ETOUD.isPeak(start)
