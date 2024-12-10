import csv
import datetime


class Data:
    """
    Read electric usage data and store it in data
    All units should be kWh
    """

    def __init__(self, file):
        """
        Read data from file and load it as an array of dictionaries.

        :param file: Name of file containing hourly electricity usage data
        :var self.data: Ordered array of dict: {USAGE: kwH used between START and END, COST: cost per kwH, START: start
                        datetime, END: end datetime}
        """

        self.data = []

        with open(file, newline='', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.data.append(self.clean(row))

    def clean(self, row):
        """
        Take row and delete unused columns and change datatype from strings to floats and datetime object for easier
        processing.

        :param row: data with unused columns and unformated data
        :return: cleaned row
        """

        row['START'] = datetime.datetime.strptime(row['DATE'] + ' ' + row['START TIME'], '%Y-%m-%d %H:%M')
        row['END'] = datetime.datetime.strptime(row['DATE'] + ' ' + row['END TIME'], '%Y-%m-%d %H:%M')
        row["USAGE"] = float(row['USAGE'])
        row['COST'] = float(row['COST'][1:])

        del row["START TIME"]
        del row["END TIME"]
        del row["DATE"]
        del row["NOTES"]
        del row["TYPE"]
        del row["UNITS"]

        return dict(row)
