#!/bin/python3

from LynxDataFetcher import LynxDataFetcher

def main():
    lynx_data_fetcher = LynxDataFetcher()
    lynx_data_fetcher.get_meta_data()
    lynx_data_fetcher.set_meta_data()
    #lynx_data_fetcher.update_stock_prizes()
    lynx_data_fetcher.get_reports()
    lynx_data_fetcher.slask()

if __name__ == '__main__':
    main()