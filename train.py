import csv
import matplotlib.pyplot as plt


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


def linear_regression(kms, prices):
    iterations = 100
    learning_rate = 0.1
    t0 = 0.0
    t1 = 0.0  # TODO: read t0,t1 from db
    dataset_size = len(kms)
    for i in range(iterations):
        print("iteration ", i)
        tmp_t0_sum = 0.0
        tmp_t1_sum = 0.0
        loss_sum = 0.0
        for km, price in zip(kms, prices):
            loss = estimate_price(t0, t1, km) - price
            loss_sum += abs(loss)
            tmp_t0_sum += loss
            tmp_t1_sum += loss * km
        t0 -= learning_rate * tmp_t0_sum / dataset_size
        t1 -= learning_rate * tmp_t1_sum / dataset_size
        print("loss = ", loss_sum / dataset_size)

    return t0, t1


def estimate_price(t0, t1, km):
    return t0 + t1 * km


# min-max normalization. Scales data to [0,1] interval
def normalize(data):
    min_val = min(data)
    max_val = max(data)
    normalized = []

    for val in data:
        normalized.append((val-min_val) / (max_val - min_val))
    return normalized


def main():
    kms, prices = read_dataset("data.csv")
    normalized_kms = normalize(kms)
    normalized_prices = normalize(prices)

    # dataset graph visualisation
    plt.plot(normalized_kms, normalized_prices, 'bo')
    plt.show()

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
