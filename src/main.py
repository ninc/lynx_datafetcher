#!/bin/python3

from BorsData import BorsData

def main():

    borsdata = BorsData()
    borsdata.print_api_key()
    borsdata.print_data()

if __name__ == '__main__':
    main()