from Data import *
from ETOUD import *
from Solar import *
from grid import *
from EV2A import *
from EVB import *
electric_data = 'electric.csv'


def output():
    # print("Year cost without Solar : ", round(sum(base.Cost())))
    print("Year cost with Solar : ", round(sum(solar.Cost())), "\t EOY TrueUp : ", round(solar.trueUp()))
    # print("Year cost with Batteries :", round(sum(battery.Cost())), "Loss : ", round(battery.battery.loss))
    print("Year cost with Solar and Batteries: ", round(sum(max.Cost())), "\t EOY TrueUp : ", round(max.trueUp()))

if __name__ == '__main__':

    data = Data(electric_data)
    m = 1
    base = Grid(data, plan=ETOUD, multiplier=m)
    solar = Grid(data, solar=Solar(8.16), plan=ETOUD, multiplier=m)
    battery = Grid(data, battery=Battery(13.5, quantity=2), plan=ETOUD, multiplier=m)
    max = Grid(data, solar=Solar(8.16), plan=ETOUD, battery=Battery(13.5, quantity=2), multiplier=m)

    print("E-TOU-D")
    output()

    base = Grid(data, plan=EV2A, multiplier=m)
    solar = Grid(data, solar=Solar(8.16), plan=EV2A, multiplier=m)
    battery = Grid(data, battery=Battery(13.5, quantity=2), plan=EV2A, multiplier=m)
    max = Grid(data, solar=Solar(8.16), plan=EV2A, battery=Battery(13.5, quantity=2), multiplier=m)

    print("\nEV2-A")
    output()

    base = Grid(data, plan=EVB, multiplier=m)
    solar = Grid(data, solar=Solar(8.16), plan=EVB, multiplier=m)
    battery = Grid(data, battery=Battery(13.5, quantity=2), plan=EVB, multiplier=m)
    max = Grid(data, solar=Solar(8.16), plan=EVB, battery=Battery(13.5, quantity=2), multiplier=m)

    print("\nEVB")
    output()