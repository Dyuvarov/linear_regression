import csv
import json
import matplotlib.pyplot as plt

DB_FILE = "db"


def read_dataset(filepath):
    kms = []
    prices = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)  # skip header
        for row in reader:
            kms.append(eval(row[0]))
            prices.append(eval(row[1]))
    return kms, prices


def get_t_const():
    f = open(DB_FILE)
    data = json.load(f)
    return data['t0'], data['t1']


def set_t_const(t0, t1):
    data = {'t0': t0, 't1': t1}
    with open(DB_FILE, 'w') as outfile:
        json.dump(data, outfile)


def linear_regression(kms, prices):
    iterations = 500
    learning_rate = 0.2
    t0, t1 = get_t_const()
    loss = float('inf')
    dataset_size = len(kms)
    for i in range(iterations):
        print("iteration ", i)
        tmp_t0_sum = 0.0
        tmp_t1_sum = 0.0
        loss_sum = 0.0
        prev_loss = loss
        for km, price in zip(kms, prices):
            cur_loss = estimate_price(t0, t1, km) - price
            tmp_t0_sum += cur_loss
            tmp_t1_sum += cur_loss * km
            loss_sum += abs(cur_loss)
        tmp_t0 = t0 - learning_rate * tmp_t0_sum / dataset_size
        tmp_t1 = t1 - learning_rate * tmp_t1_sum / dataset_size
        loss = loss_sum / dataset_size
        print("loss = ", loss)
        if loss > prev_loss:
            print("Stop training. Will worsen the result")
            break
        t0 = tmp_t0
        t1 = tmp_t1
    set_t_const(t0, t1)
    return t0, t1


def estimate_price(t0, t1, km):
    return t0 + t1 * km


# min-max normalization. Scales data to [0,1] interval
def normalize(data):
    min_val = min(data)
    max_val = max(data)
    normalized = []

    for val in data:
        normalized.append((val - min_val) / (max_val - min_val))
    return normalized


def main():
    kms, prices = read_dataset("data.csv")
    normalized_kms = normalize(kms)
    normalized_prices = normalize(prices)

    # dataset graph visualisation
    # plt.plot(normalized_kms, normalized_prices, 'bo')
    # plt.show()

    t0, t1 = linear_regression(normalized_kms, normalized_prices)
    line_x = [min(normalized_kms), max(normalized_kms)]
    line_y = []
    for km in normalized_kms:
        line_y.append(estimate_price(t0, t1, km))

    # dataset with prediction function
    plt.plot(normalized_kms, normalized_prices, 'bo', normalized_kms, line_y, 'r-')
    # plt.plot(normalized_kms, normalized_prices, "bo", line_x, line_y)
    plt.xlabel("km")
    plt.ylabel("price")
    plt.show()


if __name__ == '__main__':
    main()
    # input("Press Enter to continue...")
