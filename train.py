import csv
import matplotlib.pyplot as plt
import lr_math as lrm
import lr_persist as lrp

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


def linear_regression(kms, prices):
    iterations = 1000
    learning_rate = 0.1
    t0 = 0
    t1 = 0
    loss = float('inf')
    dataset_size = len(kms)
    for i in range(iterations):
        print("iteration ", i)
        tmp_t0_sum = 0.0
        tmp_t1_sum = 0.0
        loss_sum = 0.0
        prev_loss = loss
        for km, price in zip(kms, prices):
            cur_loss = lrm.estimate_price(t0, t1, km) - price
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
    lrp.set_t_const(t0, t1)
    return t0, t1


# Build graph
def visualize(t0, t1, norm_kms, kms, prices):
    norm_line_y = [lrm.estimate_price(t0, t1, min(norm_kms)), lrm.estimate_price(t0, t1, max(norm_kms))]
    denorm_line_y = lrm.denormalize(norm_line_y, min(prices), max(prices))
    denorm_line_x = [min(kms), max(kms)]

    plt.plot(kms, prices, 'go', denorm_line_x, denorm_line_y, 'r')
    plt.xlabel("km")
    plt.ylabel("price")
    plt.show()


def main():
    kms, prices = read_dataset("data.csv")
    lrp.save_data(kms, prices)

    norm_kms = lrm.normalize(kms, max(kms), min(kms))
    norm_prices = lrm.normalize(prices, max(prices), min(prices))

    t0, t1 = linear_regression(norm_kms, norm_prices)
    visualize(t0, t1, norm_kms, kms, prices)


if __name__ == '__main__':
    main()
