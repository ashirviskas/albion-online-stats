import requests
from multiprocessing import Pool
from functools import lru_cache

DATA_URL = 'https://www.albion-online-data.com/api/v2/stats/prices/'


def format_req(item, locations=None, qualities=None):
    req_str = DATA_URL + item
    if locations is not None:
        req_str += '?locations=' + ','.join(locations)
        if qualities is not None:
            req_str = req_str + '&qualities=' + ','.join(str(q) for q in qualities)
    elif qualities is not None:
        req_str = req_str + '?qualities=' + ','.join(str(q) for q in qualities)
    return req_str


@lru_cache(512)
def read_prices(item, locations=None, qualities=None):
    if item is None:
        return None
    req_str = format_req(item, locations, qualities)
    # print(req_str)
    response = requests.get(req_str)
    return response.json()


def add_enchantment(item, enchantment):
    return item + '@' + str(enchantment)


def get_most_diffenet(all_data, num=2):
    min_sell_prices = []
    max_buy_prices = []
    for item in all_data:
        if item['sell_price_min'] != 0:
            min_sell_prices.append([item['sell_price_min'], item['city']])
        if item['buy_price_max'] != 0:
            max_buy_prices.append([item['buy_price_max'], item['city']])
    price_diffs = []
    for mbp in max_buy_prices:
        for msp in min_sell_prices:
            price_diffs.append([msp[0] - mbp[0], mbp, msp])
    print(price_diffs[:num])
    price_diffs.sort(key=lambda x: x[0])
    print(price_diffs[:num])


def get_biggest_buy_price(all_prices):
    max_price = 0
    if all_prices is None:
        return 0
    for item in all_prices:
        max_buy_price = item['buy_price_max']
        if max_buy_price > max_price:
            max_price = max_buy_price
    return max_price


def get_gear_price(gear):
    p = Pool(processes=len(gear))
    total_price = 0
    all_prices = p.map(read_prices, gear)
    p.close()
    for prices in all_prices:
        total_price += get_biggest_buy_price(prices)
    return total_price


def main():
    # all_data = read_prices('T5_2H_HOLYSTAFF_UNDEAD@1', qualities=[2])
    # print(get_biggest_buy_price(all_data))
    # get_most_diffenet(all_data)
    gear= [ None    ]
    print(get_gear_price(gear))


if __name__ == '__main__':
    main()
