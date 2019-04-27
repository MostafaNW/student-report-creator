import sys
import csv
from dataquery import DataQuerier

def run():
    data_querier = DataQuerier(sys.argv[1])
    data_querier.write_report()

if __name__ == '__main__':
    run()
