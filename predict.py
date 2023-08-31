import sys

import lr_math as lrm
import lr_persist as lrp


def prompt_mileage():
    while 1:
        try:
            raw = input("Enter a mileage (km) as integer: ")
        except:
            print("Input error!")
            continue

        if not raw.isnumeric():
            print("Mileage must be a positive integer number!")
            continue

        try:
            parsed = int(raw)
        except:
            print("% is not a valid number!" % raw)
            continue

        return parsed


def normalize_mileage(km):
    km_min, km_max = lrp.get_mileage_min_max()
    return lrm.normalize([km], km_min, km_max)[0]


def predict_price(norm_km):
    t0, t1 = lrp.get_t_const()
    norm_price = lrm.estimate_price(t0, t1, norm_km)
    price_min, price_max = lrp.get_price_min_max()
    return lrm.denormalize([norm_price], price_min, price_max)[0]


def main():
    km = prompt_mileage()
    price = predict_price(normalize_mileage(km))

    print("Estimated price is: %.2f" % price)
    if price < 0:
        print("The seller should pay YOU if he wants to get rid of this garbage.")


if __name__ == '__main__':
    main()
