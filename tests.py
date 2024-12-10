import unittest
from ETOUD import *
from Data import *
from Solar import *
from grid import *
from Battery import *

test_data = 'test_data.csv'

class tests(unittest.TestCase):

    def test_ETOUD_isSummer(self):
        self.assertTrue(ETOUD.isSummer(datetime.datetime(day=17, month=7, year=2020)))
        self.assertTrue(ETOUD.isSummer(datetime.datetime(day=1, month=6, year=2020)))
        self.assertFalse(ETOUD.isSummer(datetime.datetime(day=17, month=10, year=2020)))
        self.assertFalse(ETOUD.isSummer(datetime.datetime(day=1, month=10, year=2020)))

    def test_ETOUD_isPeak(self):
        self.assertTrue(ETOUD.isPeak(datetime.datetime(day=1, month=10, year=2020, hour=19)))
        self.assertTrue(ETOUD.isPeak(datetime.datetime(day=1, month=10, year=2020, hour=17)))
        self.assertFalse(ETOUD.isPeak(datetime.datetime(day=4, month=12, year=2021, hour=1)))
        self.assertFalse(ETOUD.isPeak(datetime.datetime(day=4, month=1, year=2021, hour=20)))

    def test_grid_cost(self):
        data = Data(test_data)
        tou = Grid(data, plan=ETOUD)
        self.assertEqual(tou.Cost()[0], .41)

    def test_Solar(self):
        system = Solar(8.16)
        self.assertTrue(system.production(datetime.datetime(day=4, month=1, year=2021, hour=23)) < .1)
        self.assertTrue(system.production(datetime.datetime(day=4, month=1, year=2021, hour=12)) > 5)

    def test_grid_calcSolarCost(self):
        solar = Solar(8.16)
        data = Data(test_data)
        tou = Grid(data, plan=ETOUD, solar=solar)
        self.assertEqual(tou.Cost()[0], .41)

    def test_battery(self):
        data = Data(test_data)
        tou = Grid(data, plan=ETOUD)
        low = datetime.datetime(day=4, month=1, year=2021, hour=23)
        high = datetime.datetime(day=4, month=1, year=2021, hour=18)
        self.assertEqual(tou.batteryManager(10, 0, low), 10)

        tou = Grid(data, plan=ETOUD, solar=Solar(8.16))
        self.assertEqual(tou.batteryManager(10, 20, low), -10)
        self.assertEqual(tou.batteryManager(10, 20, high), -10)

        tou = Grid(data, plan=ETOUD, battery=Battery(13.5))
        self.assertEqual(tou.batteryManager(10, 0, low), 15)
        self.assertEqual(tou.batteryManager(10, 0, high), 5.5)

        tou = Grid(data, plan=ETOUD, battery=Battery(13.5, quantity=2), solar=Solar(8.16))
        self.assertEqual(tou.batteryManager(10, 10, low), 10)
        self.assertEqual(tou.batteryManager(5, 10, high), -10)

if __name__ == '__main__':
    unittest.main()
