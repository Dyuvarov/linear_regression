import json

DB_FILE = "db"


def save_data(kms, prices):
    f = open(DB_FILE, 'w')
    data = {'mileage_min': min(kms), 'mileage_max': max(kms), 'price_min': min(prices), 'price_max': max(prices)}
    json.dump(data, f)


def get_mileage_min_max():
    f = open(DB_FILE)
    data = json.load(f)
    return data['mileage_min'], data['mileage_max']


def get_price_min_max():
    f = open(DB_FILE)
    data = json.load(f)
    return data['price_min'], data['price_max']


def get_t_const():
    f = open(DB_FILE)
    data = json.load(f)
    return data['t0'], data['t1']


def set_t_const(t0, t1):
    f = open(DB_FILE)
    data = json.load(f)
    data['t0'] = t0
    data['t1'] = t1
    with open(DB_FILE, 'w+') as outfile:
        json.dump(data, outfile)
